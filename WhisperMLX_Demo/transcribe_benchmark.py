import os
import time
from datetime import timedelta
import soundfile as sf
import mlx.core as mx
import mlx_whisper
from jiwer import wer

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

def sanitize_model_name(model_path: str) -> str:
    return os.path.basename(model_path).replace(".", "").replace("-", "")

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
MODEL_PATH = os.path.join(BASE_DIR, "models", "whisper-medium")
AUDIO_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.wav")
REFERENCE_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.txt")

# === Check Files ===
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")
if not os.path.exists(REFERENCE_FILE):
    raise FileNotFoundError(f"Reference transcript not found: {REFERENCE_FILE}")

# === Load Reference ===
with open(REFERENCE_FILE, encoding="utf-8") as f:
    reference_text = f.read().strip().lower()

# === Load Audio ===
audio, sr = sf.read(AUDIO_FILE)
if sr != 16000:
    raise ValueError(f"Expected 16kHz sample rate, got {sr}")
if audio.ndim > 1:
    print("Converting stereo to mono...")
    audio = audio[:, 0]

# === Transcribe ===
print(f"🔧 MLX device: {mx.default_device()}")
print(f"🎧 Transcribing using model: {MODEL_PATH}")
start_time = time.time()
result = mlx_whisper.transcribe(audio, path_or_hf_repo=MODEL_PATH)
elapsed = time.time() - start_time

# === Extract Transcript ===
generated_text = result["text"].strip().lower()
segments = result.get("segments", [])
if segments:
    formatted_text = "\n".join(seg["text"].strip() for seg in segments if seg["text"].strip())
else:
    formatted_text = result["text"].strip()

# === Compute WER ===
error = wer(reference_text, generated_text) * 100

# === Save Transcript ===
model_tag = sanitize_model_name(MODEL_PATH)
output_file = os.path.join(SAMPLES_DIR, f"jfk_moon_full__{model_tag}_mlx_transcript.txt")
with open(output_file, "w", encoding="utf-8", newline="\n") as f:
    f.write(formatted_text)
    f.write("\n\n--- Benchmark Results ---\n")
    f.write(f"Elapsed Time: {elapsed:.2f} seconds\n")
    f.write(f"Word Error Rate: {error:.2f}%\n")

print(f"📝 Transcript saved to: {output_file}")
print(f"\n📊 Benchmark Results\n  • Time Elapsed     : {elapsed:.2f} seconds\n  • Word Error Rate  : {error:.2f}%")