import googletrans
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import os

# print(googletrans.LANGUAGES)
translator = Translator()

# To capture audio
mic = sr.Microphone()
rec = sr.Recognizer()

with mic as source:
    inp_lang = 'hi'
    out_lang = 'en'

    print("Please speak now...")

    rec.adjust_for_ambient_noise(source, duration=0.2)

    try:
        audio = rec.listen(source)
        rec_aud = rec.recognize_google(audio)
        print(f"Recognized text: {rec_aud}")

        # Translate the recognized text
        translation = translator.translate(rec_aud, src=inp_lang, dest=out_lang)
        print(f"Translation: {translation.text}")

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
