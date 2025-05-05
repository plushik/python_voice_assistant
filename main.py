import os
import subprocess
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser

class VoiceAssistant:
    def __init__(self):
        # Инициализация голосового движка
        self.engine = pyttsx3.init(driverName='sapi5')
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Настройки приложений
        self.app_paths = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'browser': 'chrome.exe'
        }
        
        # Веб-сайты
        self.websites = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'stack overflow': 'https://stackoverflow.com'
        }

    def speak(self, text):
        """Синтез речи с использованием pyttsx3"""
        self.engine.say(text)
        self.engine.runAndWait()

    def greet(self):
        """Приветствие в зависимости от времени суток"""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        
        self.speak(f"{greeting} How can I assist you today?")
        print(f"System: {greeting} How can I assist you today?")

    def get_time(self):
        """Озвучивание текущего времени"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
        print(f"Current time: {current_time}")

    def listen(self):
        """Распознавание голосовых команд"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"User command: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("Could not understand audio, please try again")
            return ""
        except sr.RequestError:
            self.speak("Speech service unavailable")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def open_website(self, site):
        """Открытие веб-сайтов"""
        if site in self.websites:
            wb.open_new_tab(self.websites[site])
            self.speak(f"Opening {site}")
        else:
            self.speak("Website not configured")

    def launch_app(self, app_name):
        """Запуск приложений"""
        try:
            if app_name in self.app_paths:
                subprocess.Popen(self.app_paths[app_name])
                self.speak(f"Starting {app_name}")
            else:
                self.speak("Application not found in my database")
        except Exception as e:
            print(f"Error launching app: {e}")
            self.speak("Failed to launch application")

    def process_command(self, command):
        """Обработка команд"""
        if not command:
            return

        if 'time' in command:
            self.get_time()
            
        elif 'open' in command:
            if 'website' in command or 'browser' in command:
                for site in self.websites:
                    if site in command:
                        self.open_website(site)
                        return
                self.speak("Which website should I open?")
            else:
                for app in self.app_paths:
                    if app in command:
                        self.launch_app(app)
                        return
                self.speak("Which application should I open?")

        elif 'exit' in command or 'quit' in command:
            self.speak("Goodbye!")
            exit()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.greet()
    
    while True:
        command = assistant.listen()
        assistant.process_command(command)