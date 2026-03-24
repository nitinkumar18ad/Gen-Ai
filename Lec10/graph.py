from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Schema
# -------------------------------
class DetectCallResponse(BaseModel):
    is_question_ai: bool


client = wrap_openai(OpenAI())


# -------------------------------
# State
# -------------------------------
class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool


# -------------------------------
# Detect Query
# -------------------------------
def detect_query(state: State):
    user_message = state.get("user_message", "")

    SYSTEM_PROMPT = """
    You are an AI assistant.
    Detect whether the user query is a coding-related question.

    Return ONLY:
    { "is_question_ai": true } OR { "is_question_ai": false }
    """

    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",   # ✅ FIXED MODEL
        response_format=DetectCallResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    parsed = result.choices[0].message.parsed
    print("Parsed:", parsed)

    # ✅ Use LLM output instead of dummy logic
    state["is_coding_question"] = parsed.is_question_ai

    return state


# -------------------------------
# Routing
# -------------------------------
def route_edge(state: State) -> Literal["solve_coding_question", "solve_simple_question"]:
    if state.get("is_coding_question"):
        return "solve_coding_question"
    return "solve_simple_question"


# -------------------------------
# Nodes
# -------------------------------
def solve_coding_question(state: State):
    state["ai_message"] = "Here is your coding question answer"
    return state


def solve_simple_question(state: State):
    state["ai_message:-"] = "Please ask a coding question"
    return state


# -------------------------------
# Graph
# -------------------------------
graph_builder = StateGraph(State)

graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)

graph_builder.add_edge(START, "detect_query")

graph_builder.add_conditional_edges("detect_query", route_edge)

graph_builder.add_edge("solve_coding_question", END)
graph_builder.add_edge("solve_simple_question", END)

graph = graph_builder.compile()


# -------------------------------
# Run
# -------------------------------
def call_graph():
    state = {
        "user_message": "Can you explain pydentic in python?",
        "ai_message": "",
        "is_coding_question": False,
    }

    result = graph.invoke(state)
    print("Final Result:", result)


call_graph()