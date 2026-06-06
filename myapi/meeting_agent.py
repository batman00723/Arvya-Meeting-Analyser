from ninja_extra import ControllerBase, api_controller, http_post
from myapi.agent.llm import LLMService
from backend.config import settings
from myapi.agent.graph import create_meeting_agent
import logging
from myapi.models import MeetingReport
from ninja import Schema

llm= LLMService()
meeting_agent= create_meeting_agent(llm= llm)

class MeetingRequest(Schema):
    transcript: str

@api_controller("/analyse", tags= ['Chatbot'])
class ChatOperationController(ControllerBase):
    @http_post("/receptionist")
    def agent(self, request, payload: MeetingRequest):
        print("starting to call agent")

        initial_state = {
            "transcript": payload.transcript,
            "result": None,
            "status": "pending"
        }

        try: 
            final_state= meeting_agent.invoke(initial_state)
            response= final_state.get("result")
            print("Agent Ran Successfully.")

            analysis = final_state["result"]
            MeetingReport.objects.create(
                transcript= payload.transcript,
                analysis=analysis.model_dump()
            )

            return {
                "analysis": response
            }
        
        except Exception as e:
            logger= logging.getLogger(__name__)
            logger.error(f"Agent Execution Error: {str(e)}", exc_info= True)

            return {
                "message": "Agent Execution Falied",
                "details": str(e) if settings.debug else "Internal Server Error"
            }
        


