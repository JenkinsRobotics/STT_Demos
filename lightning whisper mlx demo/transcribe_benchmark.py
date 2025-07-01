import os
import time
from datetime import timedelta
from lightning_whisper_mlx import LightningWhisperMLX
from jiwer import wer

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
AUDIO_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.wav")
REFERENCE_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_full.txt")
MODEL_NAME = "distil-medium.en"
QUANTIZATION = None
BATCH_SIZE = 12

# === Check Files ===
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")
if not os.path.exists(REFERENCE_FILE):
    raise FileNotFoundError(f"Reference transcript not found: {REFERENCE_FILE}")

# === Load Reference Transcript ===
with open(REFERENCE_FILE, encoding="utf-8") as f:
    reference_text = f.read().strip().lower()

# === Initialize Model ===
print(f"🔧 Loading Lightning Whisper MLX model: {MODEL_NAME} (quant={QUANTIZATION})")
whisper = LightningWhisperMLX(model=MODEL_NAME, batch_size=BATCH_SIZE, quant=QUANTIZATION)

# === Transcribe ===
print(f"🎧 Transcribing: {AUDIO_FILE}")
start_time = time.time()
result = whisper.transcribe(audio_path=AUDIO_FILE)
elapsed = time.time() - start_time

# === Extract Transcript ===
generated_text = result["text"].strip().lower()

# === Format Transcript (prefer segments if available) ===
segments = result.get("segments", [])
if segments and isinstance(segments[0], dict):
    formatted_text = "\n".join(seg.get("text", "").strip() for seg in segments if seg.get("text"))
elif segments and isinstance(segments[0], str):
    formatted_text = "\n".join(seg.strip() for seg in segments if seg.strip())
else:
    formatted_text = result["text"].strip()

# === Compute Word Error Rate ===
error = wer(reference_text, generated_text) * 100

# === Save Transcript Output ===
output_file = os.path.join(
    SAMPLES_DIR,
    f"jfk_moon_full__{MODEL_NAME.replace('.', '')}_transcript.txt"
)
with open(output_file, "w", encoding="utf-8", newline="\n") as f:
    f.write(formatted_text)
    f.write("\n\n--- Benchmark Results ---\n")
    f.write(f"Elapsed Time: {elapsed:.2f} seconds\n")
    f.write(f"Word Error Rate: {error:.2f}%\n")

print(f"📝 Transcript saved to: {output_file}")

# === Print Results ===
print("\n📊 Benchmark Results")
print(f"  • Time Elapsed     : {elapsed:.2f} seconds")
print(f"  • Word Error Rate  : {error:.2f}%")

# === Preview Output ===
print("\n📝 Transcript Preview:")
for line in formatted_text.splitlines()[:10]:
    print("  ", line)