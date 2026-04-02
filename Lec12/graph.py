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
    try:
        output = os.popen(cmd).read()
        return output if output else "Command executed (no output)."
    except Exception as e:
        return f"Error: {str(e)}"


# ---------------- LLM ----------------
llm = init_chat_model(
    model_provider="openai",
    model="gpt-4o-mini"   # ✅ better for tool calling
)

llm_with_tool = llm.bind_tools([run_command])


# ---------------- CHATBOT NODE ----------------
def chatbot(state: State):

    system_prompt = SystemMessage(
        content="""
You are Personal Agent, a voice-controlled AI assistant.

RULES:
- Always introduce yourself as Personal Agent.
- If user asks to run system commands (like 'list files', 'check python version'),
  you MUST use the run_command tool.
- Convert natural language into correct terminal commands.
- After executing, summarize the output briefly.
- Keep responses short for voice output.
"""
    )

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

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)


# ---------------- CREATE GRAPH ----------------
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)