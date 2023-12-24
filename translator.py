import googletrans
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import tempfile
import os
import time

translator = Translator()

# To capture audio
mic = sr.Microphone()
rec = sr.Recognizer()

while True:
    with mic as source:
        inp_lang = 'hi'
        out_lang = 'en'

        print("Please speak now...")

        rec.adjust_for_ambient_noise(source, duration=0.2)

        audio = rec.listen(source)

        try:
            rec_aud = rec.recognize_google(audio)
            print("Here is the audio input: " + rec_aud)


            if rec_aud.lower() == "stop":
                print("Stopping the program.")
                break

            to_translate = translator.translate(rec_aud, src=inp_lang, dest=out_lang)
            translated_text = to_translate.text
            print("The translated text is: ", translated_text)

            with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
                speak = gTTS(text=translated_text, lang=out_lang, slow=False)
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

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
