import os
import time
from datetime import timedelta
from lightning_whisper_mlx import LightningWhisperMLX

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FILE = os.path.join(BASE_DIR, "samples", "jfk_moon.wav")
MODEL_NAME = "distil-medium.en"  # You can try: tiny.en, base.en, small.en, medium.en, large-v3
QUANTIZATION = None  # Options: "4bit", "8bit", or None
BATCH_SIZE = 12

# === Check Audio ===
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

# === Initialize Model ===
print(f"Loading Lightning Whisper MLX model: {MODEL_NAME} (quant={QUANTIZATION})")
whisper = LightningWhisperMLX(model=MODEL_NAME, batch_size=BATCH_SIZE, quant=QUANTIZATION)

# === Transcribe ===
print(f"Transcribing file: {AUDIO_FILE}")
start_time = time.time()

result = whisper.transcribe(audio_path=AUDIO_FILE)

elapsed = time.time() - start_time
print(f"Transcription completed in {elapsed:.2f} seconds")

# === Output Transcript ===
print("\nFull Transcript:")
print(result["text"].strip())

# === Output Segment Timestamps ===
segments = result.get("segments", [])
if segments:
    print("\nSegment Timestamps:")
    for seg in segments:
        if isinstance(seg, dict):
            start = format_time(seg.get("start", 0))
            end = format_time(seg.get("end", 0))
            text = seg.get("text", "").strip()
            print(f"[{start} – {end}] {text}")