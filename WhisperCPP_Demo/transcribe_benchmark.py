# benchmark_whisper_cli.py
import subprocess, os, time
from jiwer import wer

# === CONFIGURATION ===
MODEL_NAME = "ggml-medium.en.bin"  # Use any available whisper.cpp model
USE_DEBUG_MODE = False
THREADS = "4"
USE_GPU = False  # Set to True if using Metal/GPU is desired

# === PATHS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_FILE = os.path.join(SAMPLES_DIR, "jfk_moon_cli")

INPUT_AUDIO = os.path.join(SAMPLES_DIR, "jfk_moon_full.wav")
REFERENCE_TRANSCRIPT = os.path.join(SAMPLES_DIR, "jfk_moon_full.txt")
MODEL_PATH = os.path.join(MODELS_DIR, MODEL_NAME)
WHISPER_BIN = os.path.join(BASE_DIR, "whisper.cpp", "build", "bin", "whisper-cli")

# === VERIFY INPUT ===
if not os.path.exists(INPUT_AUDIO):
    raise FileNotFoundError("Missing input audio file")
if not os.path.exists(REFERENCE_TRANSCRIPT):
    raise FileNotFoundError("Missing reference transcript file")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Missing model binary")
if not os.path.exists(WHISPER_BIN):
    raise FileNotFoundError("Missing whisper-cli binary")

# === RUN WHISPER.CPP CLI ===
cmd = [
    WHISPER_BIN,
    "-m", MODEL_PATH,
    "-f", INPUT_AUDIO,
    "-t", THREADS,
    "-otxt",
    "-of", OUTPUT_FILE
]
if not USE_GPU:
    cmd.append("-ng")
if USE_DEBUG_MODE:
    cmd.append("--debug-mode")

print("🚀 Running whisper.cpp CLI...")
start = time.time()
subprocess.run(cmd, check=True)
elapsed = time.time() - start

# === LOAD AND COMPARE ===
transcript_path = OUTPUT_FILE + ".txt"
if not os.path.exists(transcript_path):
    raise RuntimeError("Transcription output not found.")

with open(transcript_path, encoding="utf-8") as f:
    hypothesis = f.read().strip().lower()

with open(REFERENCE_TRANSCRIPT, encoding="utf-8") as f:
    reference = f.read().strip().lower()

error = wer(reference, hypothesis) * 100

# === APPEND BENCHMARK TO OUTPUT FILE ===
with open(transcript_path, "a", encoding="utf-8") as f:
    f.write("\n\n--- Benchmark Results ---\n")
    f.write(f"Elapsed Time: {elapsed:.2f} seconds\n")
    f.write(f"Word Error Rate: {error:.2f}%\n")

print("\n✅ Benchmark Complete")
print(f"  • Time Elapsed     : {elapsed:.2f} seconds")
print(f"  • Word Error Rate  : {error:.2f}%")
print(f"  • Transcript File  : {transcript_path}")