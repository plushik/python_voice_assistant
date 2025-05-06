import datetime
import psutil
import pyautogui
import wikipedia
import smtplib
import webbrowser as wb
import requests
from config import speak

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Текущее время: {now}")

def tell_date():
    now = datetime.datetime.now()
    speak(f"Сегодня {now.day} {now.strftime('%B')} {now.year} года")

def battery_info():
    usage = psutil.cpu_percent()
    battery = psutil.sensors_battery()
    speak(f"Использование процессора: {usage}%")
    speak(f"Заряд батареи: {battery.percent}%")

def take_screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")
    speak("Скриншот сохранён")

def send_email(to_address, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("ваш_email@gmail.com", "ваш_пароль")
        server.sendmail("ваш_email@gmail.com", to_address, content)
        server.quit()
        speak("Письмо отправлено.")
    except Exception as e:
        print(e)
        speak("Не удалось отправить письмо.")

def get_weather(city_name):
    api_key = "YOUR_API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"appid": api_key, "q": city_name, "lang": "ru", "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["cod"] != "404":
        weather = data["weather"][0]["description"]
        temp = int(data["main"]["temp"])
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        speak(f"В городе {city_name} сейчас {temp} градусов, давление {pressure} гПа, влажность {humidity}%, {weather}.")
    else:
        speak("Город не найден.")
