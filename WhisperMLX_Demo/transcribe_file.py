import os
import soundfile as sf
import mlx.core as mx
import mlx_whisper
import time
from datetime import timedelta

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "whisper-medium")
AUDIO_FILE = os.path.join(BASE_DIR, "samples", "jfk_moon.wav")

# === Device Info ===
print(f"MLX device: {mx.default_device()}")

# === Load and Prepare Audio ===
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

audio, sr = sf.read(AUDIO_FILE)
if sr != 16000:
    raise ValueError(f"Expected 16kHz sample rate, got {sr}")
if audio.ndim > 1:
    print("Converting stereo to mono...")
    audio = audio[:, 0]

# === Transcribe ===
print(f"Transcribing using model: {MODEL_PATH}")
start_time = time.time()

result = mlx_whisper.transcribe(audio, path_or_hf_repo=MODEL_PATH)

elapsed = time.time() - start_time
print(f"Transcription completed in {elapsed:.2f} seconds")

# === Output Transcript ===
print("\nFull Transcript:")
print(result["text"].strip())

# === Output Segment Timestamps ===
if "segments" in result:
    print("\nSegment Timestamps:")
    for seg in result["segments"]:
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        text = seg["text"].strip()
        print(f"[{start} – {end}] {text}")