import speech_recognition as sr
import pyttsx3
from langgraph.checkpoint.mongodb import MongoDBSaver
from graph import create_chat_graph
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = "mongodb://localhost:27017/"
config = {"configurable": {"thread_id": "1"}}

# 🔊 Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("\n🔊 Speaking:", text)
    engine.say(text)
    engine.runAndWait()


def main():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)

        r = sr.Recognizer()

        while True:  # ✅ continuous assistant
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    r.pause_threshold = 2

                    print("\n🎤 Say something (or say 'exit'):")
                    audio = r.listen(source)

                    print("Processing...")
                    sst = r.recognize_google(audio).lower()

                    print("You said:", sst)

                    # ✅ exit condition
                    if "exit" in sst:
                        speak("Goodbye!")
                        break

                    final_response = ""

                    for event in graph.stream(
                        {"messages": [{"role": "user", "content": sst}]},
                        config,
                        stream_mode="values"
                    ):
                        if "messages" in event:
                            msg = event["messages"][-1]
                            msg.pretty_print()

                            # capture final assistant response
                            if hasattr(msg, "content"):
                                final_response = msg.content

                    # 🗣 Speak only important part
                    if final_response:
                        speak(final_response[:300])  # limit speech length

            except Exception as e:
                print("Error:", e)
                speak("Sorry, I didn't catch that.")


if __name__ == "__main__":
    main()