import pyttsx3
engine = pyttsx3.init()
text = input("Enter the text you want to convert to speech: ")

engine.say(text)
engine.runAndWait()

engine.save_to_file(text, "output_audio.mp3")
engine.runAndWait()

print("Text has been spoken and saved as 'output_audio.mp3'")