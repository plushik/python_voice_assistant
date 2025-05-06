import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
for voice in voices:
    if 'russian' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('volume', 1)

wikipedia.set_lang("ru")

def speak(audio):
    print("Голосовой ассистент:", audio)
    engine.say(audio)
    engine.runAndWait()

def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("Готово")

def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("Текущее время: " + Time)

def date():
    now = datetime.datetime.now()
    speak(f"Сегодня {now.day} {now.strftime('%B')} {now.year} года")

def checktime(tt):
    hour = datetime.datetime.now().hour
    if ("утро" in tt):
        if (6 <= hour < 12):
            speak("Доброе утро!")
        elif (12 <= hour < 18):
            speak("Сейчас день")
        elif (18 <= hour < 24):
            speak("Сейчас вечер")
        else:
            speak("Сейчас ночь")


def wishme():
    speak("Добро пожаловать!")
    hour = datetime.datetime.now().hour
    if (6 <= hour < 12):
        speak("Доброе утро!")
    elif (12 <= hour < 18):
        speak("Добрый день!")
    elif (18 <= hour < 24):
        speak("Добрый вечер!")
    else:
        speak("Доброй ночи!")
    speak("Я к вашим услугам. Чем могу помочь?")

def wishme_end():
    speak("Выключаюсь")
    hour = datetime.datetime.now().hour
    if (6 <= hour < 12):
        speak("Доброе утро")
    elif (12 <= hour < 18):
        speak("Добрый день")
    elif (18 <= hour < 24):
        speak("Добрый вечер")
    else:
        speak("Спокойной ночи")
    quit()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Распознаю...")
        query = r.recognize_google(audio, language='ru-RU')
    except Exception as e:
        print(e)
        speak("Повторите, пожалуйста")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("ваш_email@gmail.com", "ваш_пароль")
    server.sendmail("ваш_email@gmail.com", to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")

def cpu():
    usage = str(psutil.cpu_percent())
    speak('Использование CPU: ' + usage + '%')
    battery = psutil.sensors_battery()
    speak("Батарея: " + str(battery.percent) + '%')

def weather():
    api_key = "YOUR-API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Введите город")
    city_name = takeCommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&lang=ru"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        temp = y["temp"] - 273.15
        pressure = y["pressure"]
        humidity = y["humidity"]
        description = x["weather"][0]["description"]
        speak(f"В городе {city_name} сейчас {int(temp)} градусов, давление {pressure} гектопаскалей, влажность {humidity} процентов и {description}.")
    else:
        speak("Город не найден")

def personal():
    speak("Я — голосовой помощник, версия 0.1. Разработан студентом. Приятно познакомиться!")

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()
        if 'время' in query:
            time()
        elif 'дата' in query:
            date()
        elif 'расскажи о себе' in query or 'кто ты' in query:
            personal()
        elif 'википедия' in query:
            speak("Ищу информацию...")
            query = query.replace("википедия", "")
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        elif 'отправь почту' in query:
            try:
                speak("Что отправить?")
                content = takeCommand()
                to = 'получатель@почта.ру'
                sendEmail(to, content)
                speak("Письмо отправлено")
            except Exception as e:
                print(e)
                speak("Ошибка при отправке письма")
        elif 'поиск' in query or 'открой сайт' in query:
            speak("Что искать?")
            search = takeCommand().lower()
            wb.open_new_tab(search + '.com')
        elif 'скриншот' in query:
            screenshot()
            speak("Скриншот сохранён")
        elif 'запомни' in query:
            speak("Что я должен запомнить")
            data = takeCommand()
            speak("вы мне сказали запомнить вот это" + data)
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()
        elif 'покажи мне что ты запомнил' in query:
            remember = open('data.txt', 'r')
            speak("вы мне сказали запомнить вот это" + remember.read())
        elif 'заряд' in query or 'батарея' in query or 'процессор' in query:
            cpu()
        elif 'погода' in query or 'температура' in query:
            weather()
        elif 'пока' in query or 'выключись' in query:
            wishme_end()
