from gtts import gTTS
from playsound import playsound
import os

count = 1

while True:
    text = input("Enter text (type 'exit' to quit): ")

    if text.lower() == "exit":
        print("Exiting program...")
        break

    filename = f"output_audio_{count}.mp3"

    # Convert text to speech
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    # Play the audio
    playsound(filename)

    print(f"Saved and played: {filename}")
    count += 1