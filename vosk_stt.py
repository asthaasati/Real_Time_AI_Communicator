import sounddevice as sd
import wave
from vosk import Model, KaldiRecognizer
import json

def record_audio(filename="audio/input.wav", duration=5, samplerate=16000):
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

def transcribe_audio(filename="audio/input.wav"):
    model = Model("model")
    wf = wave.open(filename, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    result = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result += res.get("text", "") + " "

    final_res = json.loads(rec.FinalResult())
    result += final_res.get("text", "")
    return result.strip()
