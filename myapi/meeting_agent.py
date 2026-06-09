from ninja_extra import ControllerBase, api_controller, http_post
from myapi.agent.llm import LLMService
from backend.config import settings
from myapi.agent.graph import create_meeting_agent
import logging
from myapi.models import MeetingReport
from ninja import Schema


from myapi.services.transcript_processor import process_transcript

llm= LLMService()
meeting_agent= create_meeting_agent(llm= llm)

class MeetingRequest(Schema):
    transcript: str

@api_controller("/analyse", tags= ['Transcript → Report'])
class ChatOperationController(ControllerBase):
    @http_post("/receptionist")
    def agent(self, request, payload: MeetingRequest):
        print("starting to call agent")

        try:
            response = process_transcript(payload.transcript)

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
        


