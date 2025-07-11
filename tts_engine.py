from gtts import gTTS
from pydub import AudioSegment
import os

def speak(text, filename="audio/output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
