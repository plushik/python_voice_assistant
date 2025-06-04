import pyttsx3
import wikipedia

engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
for voice in voices:
    if 'russian' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('volume', 1)

wikipedia.set_lang("ru")

def speak(text):
    print("Ассистент:", text)
    engine.say(text)
    engine.runAndWait()
