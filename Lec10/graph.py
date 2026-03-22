from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal


class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool


def detect_query(state: State):
    user_message = state.get("user_message")  # ✅ fixed key

    # Dummy logic (replace with OpenAI later)
    if "code" in user_message.lower():
        state["is_coding_question"] = True
    else:
        state["is_coding_question"] = False

    return state


def route_edge(state: State) -> Literal["solve_coding_question", "solve_simple_question"]:
    is_coding_question = state.get("is_coding_question")  # ✅ fixed key

    if is_coding_question:
        return "solve_coding_question"
    else:
        return "solve_simple_question"


def solve_coding_question(state: State):
    user_message = state.get("user_message")

    # OpenAI call (future)
    state["ai_message"] = "Here is your coding question answer"

    return state


def solve_simple_question(state: State):
    user_message = state.get("user_message")

    # OpenAI call (future)
    state["ai_message"] = "Please ask a coding question"

    return state


# Build Graph
graph_builder = StateGraph(State)

graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)

graph_builder.add_edge(START, "detect_query")

# ✅ correct conditional routing
graph_builder.add_conditional_edges("detect_query", route_edge)

# ✅ correct edges
graph_builder.add_edge("solve_coding_question", END)
graph_builder.add_edge("solve_simple_question", END)

graph = graph_builder.compile()


def call_graph():
    state = {
        "user_message": "Hey there! How are you",
        "ai_message": "",
        "is_coding_question": False,  # ✅ fixed
    }

    result = graph.invoke(state)

    print("Final Result:", result)


call_graph()