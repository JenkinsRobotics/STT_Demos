import os
import time
from datetime import timedelta
from faster_whisper import WhisperModel
from jiwer import wer

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
MODEL_NAME = "medium.en"  # e.g., tiny.en, small.en, medium.en
MODEL_DIR = os.path.join(BASE_DIR, "models")
AUDIO_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.wav")
REFERENCE_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.txt")
OUTPUT_FILE = os.path.join(SAMPLES_DIR, f"jfk_moon_full__{MODEL_NAME.replace('.', '')}_fastwhisper_transcript.txt")

# === Check Files ===
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")
if not os.path.exists(REFERENCE_FILE):
    raise FileNotFoundError(f"Reference transcript not found: {REFERENCE_FILE}")

# === Load Reference Transcript ===
with open(REFERENCE_FILE, encoding="utf-8") as f:
    reference_text = f.read().strip().lower()

# === Load Model ===
print(f"🔧 Loading FasterWhisper model: {MODEL_NAME}")
model = WhisperModel(MODEL_NAME, download_root=MODEL_DIR, compute_type="auto")

# === Transcribe ===
print(f"🎧 Transcribing: {AUDIO_FILE}")
start_time = time.time()
segment_gen, _info = model.transcribe(AUDIO_FILE, beam_size=5)
segments = list(segment_gen)
elapsed = time.time() - start_time

# === Extract + Format Transcript ===
generated_text = " ".join([seg.text.strip().lower() for seg in segments])
formatted_text = "\n".join([seg.text.strip() for seg in segments if seg.text.strip()])

# === Compute Word Error Rate ===
error = wer(reference_text, generated_text) * 100

# === Save Transcript Output ===
with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write(formatted_text)
    f.write("\n\n--- Benchmark Results ---\n")
    f.write(f"Elapsed Time: {elapsed:.2f} seconds\n")
    f.write(f"Word Error Rate: {error:.2f}%\n")

# === Done ===
print(f"📝 Transcript saved to: {OUTPUT_FILE}")
print("\n📊 Benchmark Results")
print(f"  • Time Elapsed     : {elapsed:.2f} seconds")
print(f"  • Word Error Rate  : {error:.2f}%")
print("\n📝 Transcript Preview:")
for line in formatted_text.splitlines()[:10]:
    print("  ", line)