from .nodes import analyse_meeting_node, send_email_node, save_report_node
from langgraph.graph import StateGraph, END
from .state import MeetingState

def create_meeting_agent(llm):
    workflow= StateGraph(MeetingState)

    workflow.add_node("meeting_analyse", analyse_meeting_node)
    workflow.add_node("email_send", send_email_node)
    workflow.add_node("save_report", save_report_node)

    workflow.set_entry_point("meeting_analyse")

    workflow.add_edge("meeting_analyse", "save_report")
    workflow.add_edge("save_report", "email_send")
    workflow.add_edge("email_send", END)

    app= workflow.compile()

    return app

