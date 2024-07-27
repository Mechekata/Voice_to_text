import speech_recognition as sr
import keyboard
import time
import threading
import tkinter as tk

entered_number = "5"

def save_number():
    global entered_number
    # Получение введенного числа
    entered_number = entry.get()
    # Сохранение числа в переменную
    saved_number.set(entered_number)

def start_speech_recognition():
    # Запуск распознавания речи в отдельном потоке
    recognition_thread = threading.Thread(target=on_button_click)
    recognition_thread.start()

def on_button_click():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # Преобразование введенного числа в целое число для использования в duration
        duration = int(entered_number)
        start_timer(duration)
        data = r.record(source, duration=duration)
        text = r.recognize_google(data, language='ru')
        keyboard.write(text)
        # try:
        #     text = r.recognize_google(data, language='ru')
        #     keyboard.write(text)
        # except sr.UnknownValueError:
        #     print("Не удалось распознать речь")
        # except sr.RequestError as e:
        #     print(f"Ошибка сервиса распознавания речи: {e}")

# Функция для привязки клавиш
def bind_hotkeys():
    keyboard.add_hotkey('ctrl+n', start_speech_recognition)

# Создание главного окна
root = tk.Tk()
root.title("Voice to text")
root.geometry("500x200")

# Метка и поле ввода для числа
label = tk.Label(root, text="Enter listening time:")
label.pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=0)
saved_number = tk.StringVar()

def start_timer(duration):
    timer_thread = threading.Thread(target=update_timer, args=(duration,))
    timer_thread.start()

def update_timer(duration):
    for remaining in range(duration, 0, -1):
        timer_label.config(text=f"Time left: {remaining} seconds")
        time.sleep(1)
    timer_label.config(text="Time is over")

# Кнопка для сохранения введенного числа
save_button = tk.Button(root, text="Save listening time", command=save_number)
save_button.pack(pady=0)

timer_label = tk.Label(root, text="")
timer_label.pack(pady=5)

label = tk.Label(root, text="=============================================")
label.pack(pady=2.5)

# Кнопка для начала распознавания речи
start_button = tk.Button(root, text="Enable speech recognition", command=start_speech_recognition)
start_button.pack(pady=5)
label = tk.Label(root, text="You can also press the key combination ctrl+n to enable speech recognition")
label.pack(pady=0)

bind_hotkeys()

root.mainloop()
