#!/usr/bin/env python3

"""
Vosk Benchmark Transcriber
--------------------------
Transcribes a WAV file using a local Vosk model and computes Word Error Rate (WER)
against a reference transcript. Saves formatted output and benchmark stats.

Requirements:
- vosk
- jiwer
"""

import os
import time
import wave
import json
from datetime import timedelta
from vosk import Model, KaldiRecognizer
from jiwer import wer

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

def clean_text(text: str) -> str:
    """Normalize and trim whitespace."""
    return " ".join(text.strip().split()).lower()

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
MODEL_DIR = os.path.join(BASE_DIR, "models", "vosk-model-en-us-0.42-gigaspeech")
AUDIO_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.wav")
REFERENCE_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.txt")
OUTPUT_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full__vosk_transcript.txt")

# === File Checks ===
for path, label in [(MODEL_DIR, "Vosk model"), (AUDIO_FILE, "Audio file"), (REFERENCE_FILE, "Reference transcript")]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ {label} not found: {path}")

# === Load Reference Text ===
with open(REFERENCE_FILE, encoding="utf-8") as f:
    reference_text = clean_text(f.read())

# === Load Audio ===
with wave.open(AUDIO_FILE, "rb") as wf:
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio must be mono, 16-bit, 16kHz WAV format.")

    print(f"🔧 Loading Vosk model: {MODEL_DIR}")
    model = Model(MODEL_DIR)
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    print(f"🎧 Starting transcription: {os.path.basename(AUDIO_FILE)}")
    start_time = time.time()

    segments = []
    transcript_lines = []

    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = clean_text(result.get("text", ""))
            if text:
                transcript_lines.append(text)
                segments.append(result)

    # Final flush
    final = json.loads(recognizer.FinalResult())
    final_text = clean_text(final.get("text", ""))
    if final_text:
        transcript_lines.append(final_text)
        segments.append(final)

    elapsed = time.time() - start_time

# === Format Output ===
full_transcript = "\n".join(transcript_lines)
full_text_flat = " ".join(transcript_lines)
error_rate = wer(reference_text, full_text_flat) * 100

# === Save Results ===
with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write(full_transcript)
    f.write("\n\n--- Benchmark Results ---\n")
    f.write(f"Elapsed Time   : {elapsed:.2f} seconds\n")
    f.write(f"Word Error Rate: {error_rate:.2f}%\n")

# === Final Report ===
print(f"✅ Transcript saved: {OUTPUT_FILE}")
print("\n📊 Benchmark Summary")
print(f"  • Time Elapsed     : {elapsed:.2f} seconds")
print(f"  • Word Error Rate  : {error_rate:.2f}%")
print("\n📝 Transcript Preview:")
for line in transcript_lines[:10]:
    print("  ", line)