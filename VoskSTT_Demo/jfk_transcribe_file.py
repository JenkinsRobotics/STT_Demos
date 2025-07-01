import os
import time
import soundfile as sf
from datetime import timedelta
from vosk import Model, KaldiRecognizer
import json

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models", "vosk-model-en-us-0.42-gigaspeech")
AUDIO_FILE = os.path.join(BASE_DIR, "samples", "jfk_moon.wav")

# === Load and Prepare Audio ===
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

audio, sr = sf.read(AUDIO_FILE)
if sr != 16000:
    raise ValueError(f"Expected 16kHz sample rate, got {sr}")
if audio.ndim > 1:
    print("Converting stereo to mono...")
    audio = audio[:, 0]

# Convert to 16-bit PCM bytes
pcm_data = (audio * 32767).astype("int16").tobytes()

# === Load Model ===
print(f"Loading Vosk model from: {MODEL_DIR}")
model = Model(MODEL_DIR)
rec = KaldiRecognizer(model, sr)
rec.SetWords(True)

# === Transcribe ===
print(f"Transcribing file: {AUDIO_FILE}")
start_time = time.time()

rec.AcceptWaveform(pcm_data)
result = json.loads(rec.FinalResult())

elapsed = time.time() - start_time
print(f"Transcription completed in {elapsed:.2f} seconds")

# === Output Transcript ===
print("\nFull Transcript:")
print(result.get("text", "").strip())

# === Output Segment Timestamps ===
print("\nSegment Timestamps:")
for word in result.get("result", []):
    start = format_time(word["start"])
    end = format_time(word["end"])
    text = word["word"]
    print(f"[{start} – {end}] {text}")