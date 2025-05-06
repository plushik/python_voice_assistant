import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread
from config import speak
from assistant import take_command, handle_query

BG_COLOR = "#D2C6E2"

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("500x700")
        self.root.configure(bg=BG_COLOR)
        self.entry = tk.StringVar()
        self.stop_flag = False

        self.create_widgets()

    def create_widgets(self):
        img = Image.open("wallpaper.jpg").resize((500, 300))
        self.bg_photo = ImageTk.PhotoImage(img)
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.pack()

        heading = tk.Label(self.root, text="Голосовой ассистент", font=("Arial", 20, "bold"), bg=BG_COLOR)
        heading.pack(pady=10)

        name_frame = tk.Frame(self.root, bg=BG_COLOR)
        name_frame.pack()
        tk.Label(name_frame, text="Введите имя:", font=("Arial", 12), bg=BG_COLOR).pack(side=tk.LEFT)
        tk.Entry(name_frame, textvariable=self.entry, width=30).pack()

        self.button = tk.Button(self.root, text="Запустить", command=self.toggle_assistant, font=("Arial", 14))
        self.button.pack(pady=20)

    def toggle_assistant(self):
        if not self.stop_flag:
            self.stop_flag = True
            self.button.config(text="Остановить")
            Thread(target=self.run_assistant).start()
        else:
            self.stop_flag = False
            self.button.config(text="Запустить")

    def run_assistant(self):
        speak(f"Здравствуйте, {self.entry.get()}!")
        while self.stop_flag:
            query = take_command()
            if query == "None":
                continue
            if not handle_query(query):
                self.stop_flag = False
                self.button.config(text="Запустить")
                break
