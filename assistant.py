import os
import wikipedia
from config import speak
from functions import *
import speech_recognition as sr

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Я слушаю...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='ru-RU')
        print("Вы сказали:", query)
        return query.lower()
    except Exception as e:
        speak("Повторите, пожалуйста.")
        return "None"

def handle_query(query):
    if 'время' in query:
        tell_time()
    elif 'дата' in query:
        tell_date()
    elif 'википедия' in query:
        speak("Ищу в Википедии...")
        query = query.replace("википедия", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except:
            speak("Информация не найдена.")
    elif 'отправь почту' in query:
        speak("Что отправить?")
        content = take_command()
        send_email("получатель@почта.ру", content)
    elif 'поиск' in query or 'открой сайт' in query:
        speak("Что искать?")
        search = take_command()
        wb.open_new_tab(search + ".com")
    elif 'скриншот' in query:
        take_screenshot()
    elif 'заряд' in query or 'батарея' in query or 'процессор' in query:
        battery_info()
    elif 'погода' in query:
        speak("Какой город?")
        city = take_command()
        get_weather(city)
    elif 'запомни' in query:
        speak("Что запомнить?")
        data = take_command()
        with open('data.txt', 'w', encoding='utf-8') as f:
            f.write(data)
        speak("Запомнил.")
    elif 'покажи что ты запомнил' in query:
        with open('data.txt', 'r', encoding='utf-8') as f:
            speak("Вы сказали мне запомнить: " + f.read())
    elif 'выход' in query or 'пока' in query:
        speak("До встречи!")
        return False
    else:
        speak("Команда не распознана.")
    return True
