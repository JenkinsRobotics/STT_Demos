#!/usr/bin/env python3

"""
==============================================================
 Vosk Offline STT - WAV File Transcription (Word-Level Output)
==============================================================
"""

import wave
import sys
import os
from vosk import Model, KaldiRecognizer, SetLogLevel

# === Logging ===
SetLogLevel(0)

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DEFAULT_MODEL_NAME = "vosk-model-en-us-0.22"

# === Input File ===
if len(sys.argv) != 2:
    print("Usage: python transcribe_file.py path/to/audio.wav")
    sys.exit(1)

wav_path = sys.argv[1]

if not os.path.exists(wav_path):
    print(f"❌ File not found: {wav_path}")
    sys.exit(1)

# === Open WAV File ===
wf = wave.open(wav_path, "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("❌ Audio file must be WAV format mono PCM.")
    sys.exit(1)

# === Load Model ===
model_path = os.path.join(MODELS_DIR, DEFAULT_MODEL_NAME)
if not os.path.exists(model_path):
    print(f"❌ Model not found at: {model_path}")
    sys.exit(1)

model = Model(model_path=model_path)

# === Recognizer Setup ===
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)
rec.SetPartialWords(True)

# === Transcription Loop ===
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())