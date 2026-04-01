from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
import os
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage



class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def run_command(cmd:str):
    """Takes command line prompt and excutes it's on user machine and returns the output of the command.
    Eample: run_command(cmd="ls") where ls is the command  to list the files.
    """
    result = os.system(command=cmd)
    return result


llm = init_chat_model(model_provider="openai", model="gpt-4-turbo")
llm_with_tool = llm.bind_tools([run_command])

def chatbot(state: State):
    system_prompt = SystemMessage(content="""
You are an AI assistant named "Personal Agent".
- Always introduce yourself as Personal Agent when starting a conversation.
- When asked your name, always reply: "I am Personal Agent".
- Occasionally refer to yourself as Personal Agent in responses.
""")
    message = llm.invoke([system_prompt]+ state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}  # ✅ Fixed: "messages" not "message"


tool_node = ToolNode(tools=[])

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)


graph = graph_builder.compile()

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)