# run_wisper_cli.py
import subprocess, os
import time

# === CONFIGURATION ===
MODEL_NAME = "ggml-base.en.bin"  # You can swap this for tiny.en, small.en, etc.
USE_DEBUG_MODE = True           # Toggle this to True to print internal Whisper logs
SUPPRESS_FFMPEG_OUTPUT = True    # Set False to show ffmpeg conversion logs (e.g., codec info)

# === PATH SETUP ===
whisper_bin = os.path.abspath("whisper.cpp/build/bin/whisper-cli")
model_path = os.path.abspath(f"models/{MODEL_NAME}")
input_mp3 = os.path.abspath("samples/JFKwechoosemoonspeech.mp3")
converted_wav = os.path.abspath("samples/JFKwechoosemoonspeech.wav")
output_path = os.path.abspath("transcript_moon")  # No extension; Whisper adds .txt

# === STEP 1: Convert MP3 to WAV ===
print("🔄 Converting MP3 to WAV (16kHz mono)...")
ffmpeg_cmd = [
    "ffmpeg", "-y", "-i", input_mp3,
    "-ar", "16000", "-ac", "1", converted_wav
]
subprocess.run(
    ffmpeg_cmd,
    capture_output=SUPPRESS_FFMPEG_OUTPUT,
    check=True
)

# === STEP 2: Transcribe WAV using Whisper.cpp CLI ===
cmd = [
    whisper_bin,
    "-m", model_path,
    "-f", converted_wav,
    "-t", "4",          # Use 4 threads (adjust for your CPU)
    "-ng",              # Disable GPU/Metal (safe fallback for Apple Silicon)
    "-otxt",            # Output plain text
    "-of", output_path  # Output file base name (e.g., transcript_moon.txt)
]
if USE_DEBUG_MODE:
    cmd.append("--debug-mode")  # Show model load, inference timings, etc.

print("\n🚀 Running Whisper CLI...")
print(" ".join(cmd))

# === TIMING START ===
start_time = time.time()

try:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    elapsed = time.time() - start_time
    print(f"\n⏱️ Transcription completed in {elapsed:.2f} seconds")

    if USE_DEBUG_MODE:
        print("----- WHISPER DEBUG OUTPUT -----")
        print(result.stdout or result.stderr)

except subprocess.CalledProcessError as e:
    print("❌ Whisper CLI failed:")
    print(e.stderr)
    exit(1)

# === STEP 3: Load and print transcript ===
txt_file = output_path + ".txt"
if os.path.exists(txt_file):
    print("\n✅ Transcript saved to:", txt_file)
    with open(txt_file) as f:
        print("----- TRANSCRIPT CONTENT -----")
        print(f.read())
else:
    print("❌ Transcript not found.")