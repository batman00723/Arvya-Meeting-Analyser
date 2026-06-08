from myapi.agent.llm import LLMService
from myapi.agent.graph import create_meeting_agent

llm = LLMService()
meeting_agent = create_meeting_agent(llm=llm)


def process_transcript(transcript: str):

    initial_state = {
        "transcript": transcript,
        "result": None,
        "status": "pending"
    }

    final_state = meeting_agent.invoke(initial_state)

    return final_state.get("result")