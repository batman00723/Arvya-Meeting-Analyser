from myapi.rag_pipeline.llm import LLMService
from pydantic import BaseModel, Field
from .state import ReceptionistState
from backend.config import settings
from langchain_cerebras import ChatCerebras
from myapi.rag_pipeline.llm import LLMService
from langgraph.graph import END
from myapi.rag_pipeline.embedding import EmbeddingService
from myapi.rag_pipeline.retrieval_Service import HybridRetrievalRerankService
from langchain_core.messages import SystemMessage, HumanMessage, trim_messages, ToolMessage, AIMessage
from typing import Optional
from myapi.agent.cal_service import CalService      
from myapi.agent.email_service import send_emergency_alert


class RouteResponse(BaseModel):
    intent: str = Field(
        description="Categorize the user's query into: 'faq', 'booking', 'emergency', or 'nonsense'."
    )
    confidence: float = Field(
        description="A score between 0.0 and 1.0 reflecting how sure you are of this intent."
    )

trimmer= trim_messages(
    max_tokens= 500,
    strategy="last",
    token_counter=len,
    include_system=False,
    start_on="human",
)

def router_node(state: ReceptionistState):

    message_history= trimmer.invoke(state["messages"])
    query= state["query"]

    print(f"Past Messages Count: {len(message_history)}")
    print(f"{message_history}")

    if not message_history:
        return {"query": query }
    
    system_instruction = """
        You are a Dental Receptionist Router. Your goal is to map the user's LATEST request to the correct internal department.

        DEPARTMENTS:
        - 'emergency': Use ONLY if the user reports pain, swelling, bleeding, or a broken tooth or something fatal or life threatning.
        - 'booking': Use if the user wants to schedule, change, or cancel an appointment, OR if they are providing details (like a date/time) requested by the assistant.
        - 'faq': Use for questions about pricing, insurance, location, or "how" procedures work, dental questions.
        - 'nonsense': Use for ambigious chats with low confidence i.e less than 0.6, greetings ("Hi"),  or off-topic chat.

        RULES:
        1. If the request is ambiguous or you are less than 70 percent sure, 
        provide a low confidence score.
        2. If a user asks a question AND wants to book (e.g., "How much is it and can I come Friday?"), select 'booking'.
        3. CONTEXT: Look at the history. If the last AI message asked for a date and the user says "Friday," that is a 'booking' intent.
    """
    
    message_for_llm= [SystemMessage(content= system_instruction)] + message_history
    if not message_history or message_history[-1].content != query:
        message_for_llm.append(HumanMessage(content=f"User's current request: {query}"))


    try:
        structured_llm = llm.model.with_structured_output(RouteResponse)
        response = structured_llm.invoke(message_for_llm)
        intent = response.intent
        print(intent)
        print(response.confidence)
        if response.confidence < 0.6:
            intent= "nonsense" 
    except Exception as e:
        print(f"Router Error: {e}")
        intent = "faq"
    
    return{
        "intent": intent,
        "query": query
    }



def routing_logic(state: ReceptionistState):
    intent= state["intent"]
    if intent == "emergency":
        return "emergency_escalation"
    elif intent == "faq":
        return "knowledge_base"
    elif intent == "booking":
        return "appointment_manager"
    else:
        return "refusal_node"


llm = LLMService()
embedder = EmbeddingService()
hybrid_retrieval= HybridRetrievalRerankService()


def faq_node(state: ReceptionistState):
    current_intent= state["intent"]
    print(current_intent)
    print("FAQ Node Activated")
    query= state["query"]

    query_vector= embedder.get_embedding(query)

    top_chunks= hybrid_retrieval.get_hybrid_reranked_content(query= query, query_vector= query_vector)

    print("Top chunks found: Sending them to LLM")

    content_chunks = "\n\n".join([c.chunk for c in top_chunks])

    system_prompt = SystemMessage(content=f"""
        You are the AI booking and information assistant for Caps and Crowns Dental Clinic.

        Your job is to:
        - Answer clinic-related questions
        - Assist with basic dental service information

        Your tone should be:
        - Professional
        - Calm
        - Reassuring
        - Concise
        
        Answer in 1–2 short sentences maximum. Be blunt and direct.

        Do not sound overly robotic or overly casual.
        Do NOT attempt medical diagnosis.

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
        - politely say I don't know
                                  
    
        Before ending the conversation ask:
        "Is there anything else I can help you with today?"
        If no:
        "Thank you for choosing Caps and Crowns Dental Clinic. Have a wonderful day!"
    
                                  
        USER QUERY:
        {query}
        
        CONTEXT:
        {content_chunks}

        """
        )
    
    response= llm.invoke([system_prompt]).content
    
    return{
        "messages": [AIMessage(content= response)],
        "clinic_response": response
    }



def refusal_node(state: ReceptionistState):
    print("Refusal Node Activated")
    response = (
        "I'm sorry, I'm not quite sure how to help with that. "
        "I can help you book an appointment, check our location, or answer dental questions. "
        "What can I do for you?"
    )
    
    return {
        "messages": [AIMessage(content=response)],
        "clinic_response": response
    }
    
from datetime import datetime, timedelta
import pytz
import dateparser

class BookingExtraction(BaseModel):
    date_phrase: Optional[str] = Field(
        default= None,
        description= "Raw date phrase exactly as user said it. Example: tomorrow, next Friday may 20"
    )
    time_phrase: Optional[str]= Field(
        default= None,
        description= "Raw time phrase as exactly as user said it. Example: 2pm, 10:30 pm"
    )
    service: Optional[str] = Field(
        default=None,
        description="Dental service requested by user"
    )

from datetime import datetime
import pytz
import dateparser


def booking_node(state: ReceptionistState):
    print("Booking Node Activated")
    tz_ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(tz=tz_ist)

    current_booking = state.get("booking_data") or {}
    query = state["query"]

    structured_llm = llm.model.with_structured_output(
        BookingExtraction

    )
    system_prompt = f"""
    You are a data extraction system.

    Extract:
    - date phrase
    - time phrase
    - service

    Rules:
    - Return raw phrases only
    - Do not calculate dates
    - If value missing return null
    - Do not infer generic booking phrases as dates

    Existing Booking Data:
    {current_booking}

    User Query:
    {query}
    """

    extraction = structured_llm.invoke(system_prompt)

    print("Raw Extracted Booking Data")
    print(extraction)

    def clean(value):

        if not value:
            return None

        value = value.strip().lower()
        invalid = {
            "",
            "null",
            "none",
            "unknown",
            "n/a",
        }
        return None if value in invalid else value

    raw_date = clean(extraction.date_phrase)
    raw_time = clean(extraction.time_phrase)
    raw_service = clean(extraction.service)

    effective_date = raw_date or current_booking.get("date")
    effective_time = raw_time or current_booking.get("time")
    effective_service = (
        raw_service or current_booking.get("service")
    )

    updated_booking = {
        "date": effective_date,
        "time": effective_time,
        "service": effective_service,
        "utc_time": current_booking.get("utc_time"),
    }

    if effective_date and effective_time:

        combined_text = (
            f"{effective_date} {effective_time}"
        )

        parsed_dt = dateparser.parse(
            combined_text,
            settings={
                "PREFER_DATES_FROM": "future",
                "RELATIVE_BASE": now_ist,
                "TIMEZONE": "Asia/Kolkata",
                "RETURN_AS_TIMEZONE_AWARE": True,
            },
        )

        if parsed_dt:

            updated_booking["date"] = (
                parsed_dt.strftime("%Y-%m-%d")
            )
            updated_booking["time"] = (
                parsed_dt.strftime("%H:%M")
            )
            utc_dt = parsed_dt.astimezone(
                pytz.utc
            )
            updated_booking["utc_time"] = (
                utc_dt.strftime(
                    "%Y-%m-%dT%H:%M:%S.000Z"
                )
            )

            print("IST:", parsed_dt)

            print(
                "UTC:",
                updated_booking["utc_time"]
            )
        else:

            print("Date parsing failed")

    return {
        "booking_data": updated_booking
    }

def booking_validate_node(state: ReceptionistState):
    print("Booking Validation Node Activated")

    booking = state.get("booking_data") or {}
    
    missing = []

    if not booking.get("date"):
        missing.append("date")
    if not booking.get("time"):
        missing.append("time")
    if not booking.get("service"):
        missing.append("service")
    print("BOOKING STATE INSIDE VALIDATION")
    print(booking)

    return {
        "missing_booking_fields": missing
    }

def booking_validation_router(state: ReceptionistState):
    missing= state.get("missing_booking_fields", [])

    if missing:
        return "booking_followup"
    
    return "check_availability"

def booking_followup_node(state: ReceptionistState):
    missing= state.get("missing_booking_fields", [])

    prompt_map = {
        "date": "What day would you like to come in?",
        "time": "What time works best for you?",
        "service": "What service are you lookinf for? Cleaning, Root Canal, Genral Consultation"
    }

    response_text= prompt_map[missing[0]]

    return {
        "messages": [AIMessage(content= response_text)],
        "clinic_response": response_text
    }


def check_availabiity_node(state: ReceptionistState):
    print("check availability node activated")
    cal= CalService()
    booking= state["booking_data"]
    print("BOOKING TIME:", booking["time"])


    try:
        print(booking["date"])
        available_slots= cal.get_slots(booking["date"])
        print("AVAILABLE SLOTS:", available_slots)
        is_available = any(booking["utc_time"] == slot["time"] for slot in available_slots)

        if is_available:
            cal.create_booking(booking, {"phone": state.get("user_phone", "000000")})
            final_message= f"Done! Your booking is officially confirmed for {booking['time']} on {booking['date']}. See you then!"
            return {"clinic_response": final_message, "intent": "confirmed"}
        else:
            # MVP Naive fail message will change it later and add neaerest slots available instead of hard slots
            fail_message= """This time slot is not available try these slots 9:00 AM 9:50 AM 10:40 AM 11:30 AM 12:20 PM 1:10 PM 2:00 PM 2:50 PM 3:40 PM"""
            return {"clinic_response": fail_message, "intent": "booking"}
    except Exception as e:
        # If api is down then manual entry by human receptionist.
        error_message= "There is technical glitch, but I have informed your booking details to my supervisor he will handle and send you conformation messge soon.."
        print(e)
        return {"clinic_response": error_message, "intent": "emergency"}
    

# For MVP only email service later will more channel alerts.
def emergency_node(state: ReceptionistState):
    print("Emergency Node activated")
    phone= state.get("user_phone", "No Phone provided")
    issue= state.get("query", "No issue provided")

    send_emergency_alert(patient_phone= phone,
                         patient_issue= issue)

    emergency_message= (
        "I have notified an urgent alert to my Supervisor they will handle this critical situation." \
        "They will call you immediately. If it is life threatning," \
        "Please call 911 or go to nearest emergency room now."
    )

    return {
        "messages": [AIMessage(content=emergency_message)],
        "clinic_response": emergency_message
    }