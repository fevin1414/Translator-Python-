import googletrans
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import os

# print(googletrans.LANGUAGES)
translator = Translator()

print(translator.detect("Bonjour, comment tu appelle?"))
print(translator.detect("Kon'nichiwa, genkidesuka"))