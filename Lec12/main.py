import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
from graph import create_chat_graph
from dotenv import load_dotenv


load_dotenv()

MONGODB_URI = "mongodb://localhost:27017/"
config = {"configurable": {"thread_id": "1"}}

def main():
    # Keep the checkpointer context alive for the entire execution
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source) 
            print("Say something!")
            audio = r.listen(source)

            print("Processing audio...")
            sst = r.recognize_google(audio)

            print("you said :-", sst)
            
            # Now using graph INSIDE the with block
            for event in graph.stream(
                {"messages": [{"role":"user","content": sst}]},
                config,
                stream_mode="values"
            ):
                if "messages" in event:
                    event["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()