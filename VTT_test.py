from speech_recognition import Microphone, Recognizer
from time import sleep
from threading import Thread
from tkinter import Label, Entry, StringVar, Tk, Button, Toplevel, Checkbutton, OptionMenu
from keyboard import add_hotkey, unhook_all_hotkeys, write

entered_number = "5"
hotkey_combination = "ctrl+f6"


def save_number():
    global entered_number
    entered_number = entry.get()
    saved_number.set(entered_number)


def start_speech_recognition():
    recognition_thread = Thread(target=on_button_click)
    recognition_thread.start()


def on_button_click():
    r = Recognizer()
    with Microphone() as source:
        r.adjust_for_ambient_noise(source)
        try:
            duration = int(entered_number)
            start_timer(duration)
        except ValueError:
            print("Ошибка: введите число!")
            return
        data = r.record(source, duration=duration)
        text = r.recognize_google(data, language='ru')
        write(text)


def start_timer(duration):
    timer_thread = Thread(target=update_timer, args=(duration,))
    timer_thread.start()


def update_timer(duration):
    for remaining in range(duration, 0, -1):
        timer_label.config(text=f"Time left: {remaining} seconds")
        sleep(1)
    timer_label.config(text="Time is over")


def setings_window():
    global hotkey_combination
    hotkey_window = Toplevel(root)
    hotkey_window.title("Hotkey Settings")
    hotkey_window.geometry("300x200")

    Label(hotkey_window, text="Enter new hotkey:").pack(pady=5)
    hotkey_entry = Entry(hotkey_window)
    hotkey_entry.pack(pady=5)
    hotkey_entry.insert(0, hotkey_combination)

    def save_hotkey():
        global hotkey_combination
        unhook_all_hotkeys()  # Remove previous hotkeys
        hotkey_combination = hotkey_entry.get()
        add_hotkey(hotkey_combination, start_speech_recognition)
        print(f"New hotkey set: {hotkey_combination}")

    Button(hotkey_window, text="Save Hotkey", command=save_hotkey).pack(pady=5)
    Checkbutton(hotkey_window, text="On/Off Sound").pack(pady=20)


root = Tk()
root.title("Voice to Text")
root.geometry("400x300")

Label(root, text="Enter listening time (in seconds):").pack(pady=5)
entry = Entry(root)
entry.pack(pady=0)
saved_number = StringVar()

save_button = Button(root, text="Save listening time", command=save_number)
save_button.pack(pady=0)

timer_label = Label(root, text="")
timer_label.pack(pady=5)

Label(root, text=45 * "=").pack(pady=2.5)

start_button = Button(root, text="Enable speech recognition", command=start_speech_recognition)
start_button.pack(pady=5)
Label(root, text="You can also press a hotkey to enable speech recognition,\n and change it in settings.").pack(pady=2.5)

setings_button = Button(root, text="Settings", command=setings_window)
setings_button.pack(pady=5)

add_hotkey(hotkey_combination, start_speech_recognition)
root.mainloop()
