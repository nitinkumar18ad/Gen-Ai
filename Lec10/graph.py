from typing_extensions import TypedDict

class State(TypedDict):
    user_message:str
    is_coding_question: bool


