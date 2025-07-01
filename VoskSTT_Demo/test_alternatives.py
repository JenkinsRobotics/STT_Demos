#!/usr/bin/env python3

"""
=====================================================================
 Vosk Offline STT - WAV Transcription with Alternatives + Word Timing
=====================================================================

Set a default filename below or pass one via command line.
"""

import wave
import sys
import json
import os
from vosk import Model, KaldiRecognizer, SetLogLevel

# === Logging ===
SetLogLevel(0)

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DEFAULT_MODEL_NAME = "vosk-model-en-us-0.22"
DEFAULT_AUDIO_NAME = "jfk_moon.wav"

# === WAV File Selection ===
# You can set the test filename here:
WAV_FILENAME = os.path.join(BASE_DIR, "samples", DEFAULT_AUDIO_NAME)

# Allow CLI override
if len(sys.argv) == 2:
    WAV_FILENAME = sys.argv[1]
    print(f"📂 Using provided audio file: {WAV_FILENAME}")
else:
    print(f"📂 Using default audio file: {WAV_FILENAME}")

if not os.path.exists(WAV_FILENAME):
    print(f"❌ File not found: {WAV_FILENAME}")
    sys.exit(1)

# === Check WAV Format ===
wf = wave.open(WAV_FILENAME, "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("❌ Audio file must be WAV format mono PCM.")
    sys.exit(1)

# === Load Model ===
model_path = os.path.join(MODELS_DIR, DEFAULT_MODEL_NAME)
if not os.path.exists(model_path):
    print(f"❌ Model not found at: {model_path}")
    sys.exit(1)

model = Model(model_path=model_path)

# === Initialize Recognizer ===
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetMaxAlternatives(10)
rec.SetWords(True)

# === Transcribe ===
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(json.loads(rec.Result()))
    else:
        print(json.loads(rec.PartialResult()))

print(json.loads(rec.FinalResult()))