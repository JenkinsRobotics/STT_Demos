import os
import time
import soundfile as sf
from datetime import timedelta
from faster_whisper import WhisperModel

# === Utilities ===
def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "medium.en"  # You can also use tiny.en, small.en, medium.en
MODEL_DIR = os.path.join(BASE_DIR, "models")  # Folder where models are stored
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

# === Load Model ===
print(f"Loading FasterWhisper model: {MODEL_NAME}")
model = WhisperModel(MODEL_NAME, download_root=MODEL_DIR, compute_type="auto")

# === Transcribe ===
print(f"Transcribing file: {AUDIO_FILE}")
start_time = time.time()

segment_gen, info = model.transcribe(AUDIO_FILE, beam_size=5)
segments = list(segment_gen)  # Force full evaluation here

elapsed = time.time() - start_time
print(f"Transcription completed in {elapsed:.2f} seconds")

# === Output Transcript ===
full_text = " ".join([seg.text.strip() for seg in segments])
print("\nFull Transcript:")
print(full_text)

# === Output Segment Timestamps ===
print("\nSegment Timestamps:")
for seg in segments:
    start = format_time(seg.start)
    end = format_time(seg.end)
    text = seg.text.strip()
    print(f"[{start} – {end}] {text}")