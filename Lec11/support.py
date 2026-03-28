from graph import graph, create_chat_graph
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()
MONGODB_URI = "mongodb://localhost:27017/"
config = {"configurable": {"thread_id": "1"}}

def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer=checkpointer)

        state = graph_with_mongo.get_state(config=config)
        for messages in state.values['messages']:
            messages.pretty_print()
        
        last_message = state.values['messages'][-1]
init()