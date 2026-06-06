from .nodes import analyse_meeting_node, send_email_node
from langgraph.graph import StateGraph, END
from functools import partial
from .state import MeetingState
# from backend.config import settings
#from psycopg_pool import ConnectionPool
# from langgraph.checkpoint.postgres import PostgresSaver


# DB_URL = settings.db_url.get_secret_value()

# _pool = ConnectionPool(
#     conninfo=DB_URL,
#     max_size=10,
#     open= True,
#     kwargs={"autocommit": True, "prepare_threshold": 0, "connect_timeout": 20} 
# )

# memory = PostgresSaver(_pool)
# memory.setup()

def create_meeting_agent(llm):
    workflow= StateGraph(MeetingState)

    workflow.add_node("meeting_analyse", analyse_meeting_node)
    workflow.add_node("email_send", send_email_node)

    workflow.set_entry_point("meeting_analyse")

    workflow.add_edge("meeting_analyse", "email_send")
    workflow.add_edge("email_send", END)

    app= workflow.compile()

    return app

