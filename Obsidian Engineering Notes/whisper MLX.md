
# **🔧 Engineering Log 005 – Whisper MLX STT Demo**

  

**Date:** 2025-06-26

**Component:** Whisper MLX (Apple Silicon–Optimized STT)

**Status:** ✅ Completed

**Environment:** Python 3.11.9 (via pyenv), macOS (M1 Max)

---

## **🧠 Overview**

  

This experiment evaluated [mlx-whisper](https://pypi.org/project/mlx-whisper/0.4.1/), a fully local, Apple Silicon–optimized implementation of Whisper using [MLX](https://github.com/ml-explore/mlx), designed to run fast inference via the Metal backend. Goals:

- Test real-time batch transcription of a known WAV file (jfk_moon.wav)
    
- Validate GPU (Metal) usage via MLX
    
- Measure latency vs. pywhispercpp and whisper.cpp
    
- Confirm model compatibility and segment-level timestamps
    

---

## **📦 Installation**

```
pip install mlx mlx-whisper soundfile
```

> 📌 Requires Python ≥3.9 running natively on Apple Silicon (M1/M2/M3).

> ✅ libsndfile must be available (typically preinstalled or installable via Homebrew).

---

## **🗂️ Folder Structure**

```
whisper_MLX/
├── models/
│   └── whisper-medium/
├── samples/
│   └── jfk_moon.wav
├── transcribe_file.py
```

---

## **📄 Script:** 

## **transcribe_file.py**

```
import os
import soundfile as sf
import mlx.core as mx
import mlx_whisper
import time
from datetime import timedelta

def format_time(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "whisper-medium")
AUDIO_FILE = os.path.join(BASE_DIR, "samples", "jfk_moon.wav")

print(f"MLX device: {mx.default_device()}")

if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

audio, sr = sf.read(AUDIO_FILE)
if sr != 16000:
    raise ValueError(f"Expected 16kHz sample rate, got {sr}")
if audio.ndim > 1:
    print("Converting stereo to mono...")
    audio = audio[:, 0]

print(f"Transcribing using model: {MODEL_PATH}")
start = time.time()

result = mlx_whisper.transcribe(audio, path_or_hf_repo=MODEL_PATH)

elapsed = time.time() - start
print(f"\nTranscription completed in {elapsed:.2f} seconds\n")

print("Full Transcript:")
print(result["text"].strip())

if "segments" in result:
    print("\nSegment Timestamps:")
    for seg in result["segments"]:
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        print(f"[{start} – {end}] {seg['text'].strip()}")
```

---

## **📈 Performance**

  

**Test Audio:** jfk_moon.wav (26s, 16kHz mono)

|**Model**|**Time Elapsed**|**Device**|**Transcript Quality**|**Notes**|
|---|---|---|---|---|
|whisper-medium (MLX)|**1.62s**|Device(gpu, 0)|✅ High|Fastest clean result so far|

---

## **🧪 Observations**

- ✅ **GPU detected:** mlx.core.default_device() → Device(gpu, 0)
    
- ✅ **Fast batch inference**: ~1.6s on whisper-medium model
    
- ✅ **Includes segment timestamps**
    
- ✅ **Simple Python API** – usable in pipelines or UIs
    
- ⚠️ **No streaming API yet** – not suitable for real-time UI updates
    
- 🔇 **Silent logs** – ideal for clean CLI or backend service use
    

---

## **📥 Model Download**

  

Via Hugging Face:

```
git clone https://huggingface.co/ml-explore/whisper-medium models/whisper-medium
```

This places model weights into a local folder accessible by mlx_whisper.

---

## **🧩 Integration Tips**

- Can be used in PySide or CLI apps for low-latency offline transcription
    
- Transcribe one .wav at a time; not designed for token-wise streaming
    
- Combine with VAD or mic chunker if used in session-based STT applications
    
- Output JSON result includes segments, text, and timing metadata
    

---

## **✅ Summary**

  

Whisper MLX is an **Apple-native**, GPU-accelerated implementation of Whisper that performs fast, accurate STT on macOS devices without needing external runtime engines or PyTorch. It’s ideal for local batch transcription, embedded assistants, and production setups where simplicity and performance matter.

  

> ⚠️ Not yet suitable for **real-time transcription GUIs**, but excellent for offline processing or command-triggered use cases.
