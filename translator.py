import googletrans
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import tempfile
import os
import time
import tkinter as tk
from tkinter import Label, Text, Button, Scrollbar
import threading

translator = Translator()

class TranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech Translator")

        self.input_text = Text(master, height=5, width=50)
        self.input_text.pack()

        self.output_label = Label(master, text="")
        self.output_label.pack()

        self.quit_button = Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

        # Create an instance of Recognizer
        self.recognizer = sr.Recognizer()

        self.thread = threading.Thread(target=self.listen_and_translate)
        self.thread.daemon = True
        self.thread.start()

    def listen_and_translate(self):
        with sr.Microphone() as source:
            print("Say something...")
            self.output_label.config(text="Listening...")

            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    user_input = self.recognizer.recognize_google(audio)

                    if user_input.lower().strip() == "stop":
                        self.output_label.config(text="Stopping the program.")
                        self.master.quit()
                        return

                    translated_result = translator.translate(user_input, src='hi', dest='en')
                    translated_text = translated_result.text

                    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
                        speak = gTTS(text=translated_text, lang='en', slow=False)
                        speak.save(temp_audio_file.name)

                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_audio_file.name)
                    pygame.mixer.music.play()

                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                    time.sleep(1)

                    try:
                        os.remove(temp_audio_file.name)
                    except PermissionError:
                        print("PermissionError: The file is still in use and cannot be deleted immediately.")
                        print("You might want to handle the deletion at a later point in your program.")

                    self.output_label.config(text=f"Translated text: {translated_text}")

                except sr.UnknownValueError:
                    self.output_label.config(text="Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.output_label.config(text=f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
