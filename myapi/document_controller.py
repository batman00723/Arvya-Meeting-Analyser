from ninja_extra import ControllerBase, api_controller, http_post, http_get
from ninja import File, UploadedFile, Form
from django.shortcuts import get_object_or_404
from django.db import transaction
from .schemas import DocumentIn, DocumentOut
from myapi.rag_pipeline.docs_processing import document_processing
from .models import Document, DocumentChunk
from myapi.rag_pipeline.docs_processing import document_processing
from myapi.rag_pipeline.llm import LLMService
from myapi.rag_pipeline.embedding import EmbeddingService
from myapi.rag_pipeline.file_type_validator import detect_file_type
from backend.config import settings
from pgvector.django import CosineDistance
from myapi.rag_pipeline.retrieval_Service import HybridRetrievalRerankService
from myapi.agent.graph import create_receptionist_agent
import logging
from langchain_core.messages import HumanMessage


llm= LLMService()

receptionist_agent= create_receptionist_agent(llm= llm)

embedder= EmbeddingService()
hybrid_retrieval= HybridRetrievalRerankService()

@api_controller("/documents", tags= ['docs'])
class DocumentOperationController(ControllerBase):


    @http_post("/", response= DocumentOut)
    def upload_docs(self, request, data: Form[DocumentIn], docs: File[UploadedFile]):
        
        file_type= detect_file_type(docs)
        
        with transaction.atomic():
            payload= data.model_dump()

            document= Document.objects.create(
                                              status= "PROCESSING",
                                              document= docs,
                                              file_type= file_type,
                                              **payload
                                              )
            
            # Processing
            document_processing(document.id)
            
        return document
    
    @http_get("/status")
    def document_processing_status(self, request, doc_id: int):
        document= Document.objects.get(id= doc_id)
        return {
            "doc_id": document.id,
            "doc_name": document.doc_name,
            "status": document.status
        }




@api_controller("/query", tags= ['Chatbot'])
class ChatOperationController(ControllerBase):
    @http_get("/query")
    def ask_query(self, request, query:str):
        query_vector= embedder.get_embedding(query)

        top_chunks= hybrid_retrieval.get_hybrid_reranked_content(query= query, query_vector= query_vector)

        print("Top chunks found: Sending them to LLM")

        content_chunks = "\n\n".join([c.chunk for c in top_chunks])
        
        # This is the "System Prompt" that gives the AI its personality
        prompt = f"""
        # ROLE
        You are the AI booking and information assistant for Caps and Crowns Dental Clinic.

        Your job is to:
        - Help users book appointments
        - Answer clinic-related questions
        - Assist with basic dental service information
        - Escalate emergencies or complex situations to a human staff member

        Your tone should be:
        - Professional
        - Calm
        - Friendly
        - Reassuring
        - Concise

        Do not sound overly robotic or overly casual.

        ---

        # CRITICAL SAFETY RULES

        If the user mentions ANY of the following:
        - severe pain
        - swelling
        - heavy bleeding
        - knocked-out tooth
        - difficulty breathing
        - trauma/injury
        - severe infection symptoms

        Immediately invoke:
        transfer_to_human

        Do NOT attempt medical diagnosis.

        If you are uncertain or the request falls outside clinic knowledge:
        invoke:
        transfer_to_human

        ---

        # KNOWLEDGE BASE

        You have access to the Caps and Crowns Dental Clinic knowledge base.

        Use it to answer questions related to:
        - Dental cleanings
        - Consultations and exams
        - Crowns and caps
        - Fillings
        - Root canals
        - Teeth whitening
        - Cosmetic dentistry
        - Emergency dental visits
        - Insurance and payment information
        - Office hours
        - Clinic location
        - Appointment policies
        - Post-treatment instructions

        Only answer using the provided clinic knowledge.

        If information is unavailable:
        - do not guess
        - do not hallucinate
        - politely escalate using transfer_to_human

        ---

        # BOOKING RULES

        Appointment slots are 30 minutes.

        When helping a patient book an appointment:

        1. Ask for their name
        2. Ask the reason for the visit
        3. Confirm the phone number
        4. Ask preferred day/time
        5. Invoke:
        check_availability_cal
        6. If available:
        invoke:
        book_appointment_cal
        7. Confirm the booking clearly

        Never ask for email addresses.

        Use:
        mail@example.com

        for all booking email fields silently.

        Use the user's phone number by default:
        {{user_number}}

        Current time:
        {{current_time_America/New_York}}

        Use it for all scheduling logic.

        ---

        # CONVERSATION RULES

        - Keep responses concise
        - Avoid long paragraphs
        - Ask clear questions
        - Avoid asking too many questions at once
        - Interpret spelling mistakes naturally
        - Do not repeat information unnecessarily
        - Stay focused on clinic-related topics

        ---

        # AVAILABILITY FLOW

        When a patient requests a time:

        Invoke:
        check_availability_cal

        If unavailable:

        Politely offer up to 3 nearby alternatives.

        Example:
        "That time is already booked, but I do have availability around 2 PM, 3:30 PM, or 4 PM."

        ---

        # BOOKING CONFIRMATION

        After successful booking:

        "You're all set, [name]! Your appointment at Caps and Crowns Dental Clinic is booked for [day/time]. We look forward to seeing you."

        ---

        # HUMAN ESCALATION

        If:
        - the user requests a real person
        - the system cannot answer confidently
        - booking fails
        - the issue is urgent or complex

        Respond:
        "One moment while I connect you with a member of our team."

        Then invoke:
        transfer_to_human

        ---

        # CLOSING

        Before ending the conversation ask:

        "Is there anything else I can help you with today?"

        If no:

        "Thank you for choosing Caps and Crowns Dental Clinic. Have a wonderful day!"

        Then invoke:
        end_chat

        USER QUERY: 
        {query}
        
        RESUME CONTEXT:
        {content_chunks}
        """
        answer= llm.invoke(prompt).content
        print(f"Query: {query} ANSWER: {answer}")

        return {
            "answer": answer
        }
    
    @http_get("/receptionist")
    def agent(self, request, query: str, phone: str):
        print("starting to call agent")

        session_id = phone
        config= {"configurable": {"thread_id": session_id}}

        initial_state = {
            "query": query,
            "user_phone": phone,
            "messages": [HumanMessage(content=query)],
        }

        try: 
            final_state= receptionist_agent.invoke(initial_state, config= config)
            response= final_state.get("clinic_response")
            booking_data= final_state.get("booking_data")
            print("Agent Ran Successfully.")


            return {
                "response": response,
                "booking_data": booking_data
            }
        
        except Exception as e:
            logger= logging.getLogger(__name__)
            logger.error(f"Agent Execution Error: {str(e)}", exc_info= True)

            return {
                "message": "There is problem while running Agent",
                "deatils": str(e) if settings.debug else "Internal Server Error"
            }
        


    



    

