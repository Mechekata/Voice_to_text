from speech_recognition import Microphone, Recognizer
from keyboard import write, add_hotkey
from time import sleep
from threading import Thread
import pyglet
from tkinter import Label, Entry, StringVar, Tk, Button

entered_number = "5"

sound1 = pyglet.media.load('on.mp3', streaming=False)
sound2 = pyglet.media.load('off.mp3', streaming=False)

def save_number():
    global entered_number
    # Получение введенного числа
    entered_number = entry.get()
    # Сохранение числа в переменную
    saved_number.set(entered_number)

def start_speech_recognition():
    # Запуск распознавания речи в отдельном потоке
    recognition_thread = Thread(target=on_button_click)
    recognition_thread.start()

def on_button_click():
    r = Recognizer()
    with Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # Преобразование введенного числа в целое число для использования в duration
        duration = int(entered_number)
        start_timer(duration)
        sound1.play()
        data = r.record(source, duration=duration)
        text = r.recognize_google(data, language='ru')
        sound2.play()
        write(text)
        # try:
        #     text = r.recognize_google(data, language='ru')
        #     keyboard.write(text)
        # except sr.UnknownValueError:
        #     print("Не удалось распознать речь")
        # except sr.RequestError as e:
        #     print(f"Ошибка сервиса распознавания речи: {e}")

# Функция для привязки клавиш
def bind_hotkeys():
    add_hotkey('ctrl+f6', start_speech_recognition)

# Создание главного окна
root = Tk()
root.title("Voice to text")
root.geometry("500x200")

# Метка и поле ввода для числа
label = Label(root, text="Enter listening time (in seconds):")
label.pack(pady=5)
entry = Entry(root)
entry.pack(pady=0)
saved_number = StringVar()

def start_timer(duration):
    timer_thread = Thread(target=update_timer, args=(duration,))
    timer_thread.start()

def update_timer(duration):
    for remaining in range(duration, 0, -1):
        timer_label.config(text=f"Time left: {remaining} seconds")
        sleep(1)
    timer_label.config(text="Time is over")

# Кнопка для сохранения введенного числа
save_button = Button(root, text="Save listening time", command=save_number)
save_button.pack(pady=0)

timer_label = Label(root, text="")
timer_label.pack(pady=5)

label = Label(root, text="=============================================")
label.pack(pady=2.5)

# Кнопка для начала распознавания речи
start_button = Button(root, text="Enable speech recognition", command=start_speech_recognition)
start_button.pack(pady=5)
label = Label(root, text="You can also press the key combination ctrl+f6 to enable speech recognition")
label.pack(pady=0)

bind_hotkeys()
root.mainloop()
