# Голосовой ассистент на Python с графическим интерфейсом

## Функции

- Распознавание речи (на русском)
- Озвучивание ответов с помощью pyttsx3
- Сообщение текущего времени и даты
- Поиск в Wikipedia
- Получение прогноза погоды
- Создание скриншотов
- Информация о заряде батареи и загрузке процессора
- Запоминание заметок
- Отправка email (по желанию)
- Открытие сайтов и карт
- GUI на Tkinter

---

## Установка

Клонируй или скачай репозиторий:

   ```bash
   git clone https://github.com/plushik/python_voice_assistant
   cd python_voice_assistant

## Установка зависимостей

   pip install -r requirements.txt

## Запуск файла

   python main.py

## Для запуска на Windows двойным кликом

   bat
      @echo off
      cd /d %~dp0
      echo Запуск голосового ассистента...
      python main.py
      pause