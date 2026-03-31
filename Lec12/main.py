import speech_recognition as sr

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

        print("Sphinx thinks you said " + r.recognize_google(audio))

main()