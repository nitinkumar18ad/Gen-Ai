from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
import os
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage


# ---------------- STATE ----------------
class State(TypedDict):
    messages: Annotated[list, add_messages]


# ---------------- TOOL ----------------
@tool
def run_command(cmd: str) -> str:
    """Executes a command on the user machine and returns output."""
    
    # ❌ os.system only returns exit code
    # ✅ Use os.popen to capture actual output
    try:
        output = os.popen(cmd).read()
        return output if output else "Command executed (no output)."
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------- LLM ----------------
llm = init_chat_model(
    model_provider="openai",
    model="gpt-4-turbo"   # make sure API supports this
)

# Bind tools
llm_with_tool = llm.bind_tools([run_command])


# ---------------- CHATBOT NODE ----------------
def chatbot(state: State):

    system_prompt = SystemMessage(
        content="""
You are an AI assistant named "Personal Agent".
- Always introduce yourself as Personal Agent when starting a conversation.
- When asked your name, always reply: "I am Personal Agent".
- Occasionally refer to yourself as Personal Agent in responses.
"""
    )

    # invoke model with tool support
    response = llm_with_tool.invoke(
        [system_prompt] + state["messages"]
    )

    return {"messages": [response]}


# ---------------- TOOL NODE ----------------
tool_node = ToolNode(tools=[run_command])


# ---------------- GRAPH ----------------
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

# conditionally go to tools if needed
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)


# Compile graph
graph = graph_builder.compile()


# Optional: with memory/checkpointer
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)