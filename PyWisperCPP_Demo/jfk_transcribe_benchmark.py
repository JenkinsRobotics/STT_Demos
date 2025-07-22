import os
import time
from datetime import timedelta
from pywhispercpp.model import Model
from jiwer import wer
import re

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

def clean_transcript(text: str) -> str:
    # Remove tags like [applause], (laughter), etc.
    text = re.sub(r"\[.*?\]|\(.*?\)", "", text)
    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
AUDIO_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.wav")
REFERENCE_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.txt")
MODEL_NAME = "medium.en" # Change to "large-v3" or "medium.en

# === Check Files ===
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")
if not os.path.exists(REFERENCE_FILE):
    raise FileNotFoundError(f"Reference transcript not found: {REFERENCE_FILE}")

# === Load Reference Transcript ===
with open(REFERENCE_FILE, encoding="utf-8") as f:
    reference_text = f.read().strip()

# === Load Model ===
print(f"🔧 Loading Whisper.cpp model: {MODEL_NAME}")
model = Model(MODEL_NAME)

# === Transcribe ===
print(f"🎧 Transcribing: {AUDIO_FILE}")
start_time = time.time()
result = model.transcribe(AUDIO_FILE)
elapsed = time.time() - start_time

# === Extract and Format Transcript ===
if isinstance(result, str):
    raw_generated = result.strip()
    formatted_text = raw_generated
elif isinstance(result, list):
    raw_generated = " ".join(seg.text.strip() for seg in result)
    formatted_text = "\n".join(seg.text.strip() for seg in result if seg.text.strip())
else:
    raise TypeError("Unexpected transcription result format")

# === Compute WER (cleaned comparison) ===
cleaned_ref = clean_transcript(reference_text)
cleaned_gen = clean_transcript(raw_generated)
error = wer(cleaned_ref, cleaned_gen) * 100

# === Save Output ===
output_file = os.path.join(
    SAMPLES_DIR, f"jfk_moon_full__{MODEL_NAME.replace('.', '')}_transcript.txt"
)
with open(output_file, "w", encoding="utf-8", newline="\n") as f:
    f.write(formatted_text)
    f.write("\n\n--- Benchmark Results ---\n")
    f.write(f"Elapsed Time: {elapsed:.2f} seconds\n")
    f.write(f"Word Error Rate: {error:.2f}%\n")

print(f"Transcript saved to: {output_file}")

# === Print Summary ===
print("\nBenchmark Results")
print(f"  • Time Elapsed     : {elapsed:.2f} seconds")
print(f"  • Word Error Rate  : {error:.2f}%")

