import mlx_whisper
import numpy as np
import sounddevice as sd

# Record 5 seconds of audio
samplerate = 16000
duration = 5
print("🎤 Speak now...")
audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
sd.wait()
audio = audio.flatten()

# Transcribe
result = mlx_whisper.transcribe(audio, path_or_hf_repo="models/whisper-tiny")
print("📄 Transcript:", result["text"])