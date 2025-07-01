import os
import time
from pywhispercpp.model import Model

# Load model (tiny, base.en, medium.en, etc.)
model = Model("medium.en")

# Path to audio file
wav_path = os.path.abspath("samples/JFKwechoosemoonspeech.wav")

# Start timer
start_time = time.time()

# Transcribe
result = model.transcribe(wav_path)

# End timer
elapsed = time.time() - start_time

# Output
print(f"\nTranscription completed in {elapsed:.2f} seconds\n")
print("Transcript:")

# Handle both str and list-of-Segment return types
if isinstance(result, str):
    print(result.strip())
else:
    print(" ".join(seg.text.strip() for seg in result))