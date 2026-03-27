import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    r.adjust_for_ambient_noise(source, duration=0.2)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said: " + text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results; {e}")   