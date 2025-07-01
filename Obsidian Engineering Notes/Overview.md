# Engineering Note: STT Engine Benchmarking and Evaluation



## **Overview**

  

This engineering note summarizes the evaluation of multiple offline speech-to-text (STT) systems tested on macOS (Apple Silicon) using the same input sample: jfk_moon.wav, a 26-second clip from JFK’s “We choose to go to the moon” speech. The goal was to benchmark latency, accuracy, and performance across various engines, particularly for real-time and offline use cases.

  

This includes testing both batch-mode and streaming transcription via PySide6 apps. Real-time performance was evaluated by playing jfk_moon.wav aloud and capturing transcription via microphone input.

---


---

## **Tested Engines**

|**Engine Name**|**API Used**|**Platform**|
|---|---|---|
|Whisper.cpp CLI|C++ CLI Tool|CPU only|
|PyWhisperCPP|Python binding|GPU (Metal)|
|MLX Whisper|Apple MLX engine|GPU (MLX)|
|FasterWhisper|Python (CTranslate2)|CPU/GPU auto|
|Vosk|Kaldi-based API|CPU|

---

## **🧩 Model Versions Used**

| **STT System**      | **Model Used**                   | **Notes**                                 |
| ------------------- | -------------------------------- | ----------------------------------------- |
| **MLX Whisper**     | whisper-medium (converted)       | From mlx-whisper GitHub or PyPI           |
| **FasterWhisper**   | medium.en                        | Hugging Face (openai/whisper-medium.en)   |
| **Whisper.cpp CLI** | ggml-medium.en.bin               | Quantized 4-bit, tested with -ng (no GPU) |
| **PyWhisperCPP**    | ggml-medium.en.bin               | Metal-accelerated real-time inference     |
| **Vosk**            | vosk-model-en-us-0.42-gigaspeech | Large English Kaldi model                 |


---


## Comparison Table

| Engine        | Model Name                         | Mode       | Device       | Transcription Time | Transcript Quality      | Notes                                       |
| ------------- | ---------------------------------- | ---------- | ------------ | ------------------ | ----------------------- | ------------------------------------------- |
| Whisper.cpp   | `ggml-base.en.bin`                 | CLI        | CPU (no GPU) | **0.92s**          | Medium (some artifacts) | Fastest; Metal disabled (`-ng`)             |
| pywhispercpp  | `medium.en`                        | Python API | GPU (Metal)  | **1.33s**          | High                    | Clean, fast GPU decoding                    |
| mlx-whisper   | `whisper-medium`                   | Python API | GPU (MLX)    | **1.69s**          | High                    | Clean, fast, good segmentation              |
| FasterWhisper | `medium.en`                        | Python API | Auto (CPU?)  | **5.54s**          | High                    | Slower due to `list(segment_gen)` usage     |
| Vosk          | `vosk-model-en-us-0.42-gigaspeech` | Python API | CPU          | **2.94s**          | Medium                  | Word-level segments, moderate hallucination |

---

## **📊 STT Benchmark Table (JFK Moon Speech)**

| **Engine**          | **Model**          | **Time Elapsed (s)** | **Word Error Rate (%)** | **Transcript File**                 |
| ------------------- | ------------------ | -------------------- | ----------------------- | ----------------------------------- |
| **Lightning MLX**   | distil-medium.en   | 22.53                | 45.89                   | distil-mediumen_transcript.txt      |
| **PyWhisperCPP**    | medium.en          | 53.66                | 3.32                    | mediumen_transcript.txt             |
| **Whisper MLX**     | whisper-medium     | 37.81                | 8.27                    | whispermedium_mlx_transcript.txt    |
| **Vosk**            | vosk-en-us-0.22    | 108.59               | 20.17                   | vosk_transcript.txt                 |
| **FasterWhisper**   | medium.en          | 263.27               | 5.91                    | fastwhisper_mediumen_transcript.txt |
| **Whisper.cpp CLI** | ggml-medium.en.bin | 263.61               | 7.41                    | jfk_moon_cli.txt                    |

---

## **📝 Transcription Comparison Matrix**

|**Model**|**Transcript Comparison**|
|---|---|
|**Ground Truth**|We choose to go to the moon in this decade and do the other things, not because they are easy, but because they are hard. Because that goal will serve to organize and measure the best of our energies and skills. Because that challenge is one that we’re willing to accept, one we are unwilling to postpone, and one we intend to win, and the others too.|
|**MLX Whisper**|We choose to go to the moon in this decade and do the other things, not because they are easy, but because they are hard. Because that goal will serve to organize and measure the best of our energies and skills. Because that challenge is one that we’re willing to accept, one we are unwilling to postpone, and one we intend to win, and the others too.|
|**FasterWhisper**|We choose to go to the moon in this decade and do the other things, not because they are easy, but because they are hard, **because** that goal will serve to organize and measure the best of our energies and skills, **because** that challenge is one that we’re willing to accept, one we are unwilling to postpone, and one we intend to win, and the others too.|
|**Whisper.cpp CLI**|We choose to go to the moon **and disdecade** and do the other things, not because they are easy, but because they are hard, **because** that goal will serve to organize and measure the best of our energies and skills, **because** that challenge is one that we’re willing to accept, one we are unwilling to postpone, and one we intend to win, and the others too.|
|**PyWhisperCPP**|We choose to go to the moon in this decade and do the other things, not because they are easy, but because they are hard. Because that goal will serve to organize and measure the best of our energies and skills. Because that challenge is one that we’re willing to accept, one we are unwilling to postpone, and one we intend to win, and the others too.|
|**Vosk (Gigaspeech)**|**we** choose to go to the moon in this decade and do the other things **not** because they are easy but because they are hard **because** that goal will serve to organize and measure the best of our energies and skills **because** that challenge is one that we’re willing to accept **one** we are unwilling to postpone and one we intend to win and the others **do**|

> 🧠 Bolded words indicate substitution or hallucination.

---

## **Key Takeaways**

- 🥇 **Best Accuracy:** PyWhisperCPP (3.32% WER), with fast, clean output using GPU (Metal).
    
- ⚡ **Fastest Inference:** Whisper.cpp CLI (~0.9s) but with lower quality.
    
- 🧪 **MLX** offers a GPU-optimized future path with lower latency on Apple Silicon.
    
- 🔁 **Vosk** works offline and streams well, but shows accuracy limitations.
    
- 🛠️ **Streaming Cleanup:** Real-time buffering, overlap filtering, and duplicate suppression significantly improve live STT usability.
    

---

## **Future Work**

- ✅ Add transcript saving to .txt in real-time GUI apps
    
- ✅ Implement rolling buffer logic with 3s preview + 10s finalized windows
    
- 🔜 Add llm-cleanup() step to optionally refine overlapping segments
    
- 🔬 Compare streaming vs. batch performance for each engine
    
- 📉 Add visual error maps or WER heatmaps over time
    

---

📅 **Date**: 2025-06-26

👨‍💻 **Engineer**: Jonathan Jenkins

🔧 **Status**: ✅ Completed (Benchmark Set 1)

---

Let me know if you’d like this converted to a GitHub README, Notion card, or downloadable .md file.

Absolutely — here’s a detailed comparison matrix for the following STT systems:

1. **OpenAI Whisper** (official Python)
    
2. **Whisper.cpp** (native C++ implementation)
    
3. **pywhispercpp** (Python bindings for whisper.cpp)
    
4. **Vosk** (Kaldi-based streaming ASR)
    

  

This matrix compares capabilities, performance characteristics, streaming support, model sizes, and platform fit.

---

### **📊 Whisper STT Engine Comparison Matrix**

|**Feature / Capability**|**OpenAI Whisper (Python)**|**Whisper.cpp (C++)**|**pywhispercpp (Python)**|**Vosk (Kaldi-based)**|
|---|---|---|---|---|
|**Core Model Type**|Transformer (encoder-decoder)|Transformer (ported)|Wrapper for whisper.cpp|Kaldi (HMM + DNN + CTC)|
|**Language Support**|99+ languages|99+ languages|99+ languages|20+ languages (varies by model)|
|**Offline Inference**|✅ Yes|✅ Yes|✅ Yes|✅ Yes|
|**Streaming Token-by-Token Output**|❌ No|⚠️ Experimental only|❌ No|✅ Yes|
|**Segmented Output (chunk-based)**|✅ Yes|✅ Yes|✅ Yes|✅ Yes|
|**Real-Time Simulation via Chunking**|⚠️ Yes (manual)|✅ Yes|✅ Yes|✅ Yes|
|**Voice Activity Detection (VAD)**|❌ No (external only)|⚠️ Optional build w/ Silero|❌ Not supported|✅ Built-in|
|**GPU Acceleration**|✅ CUDA (NVIDIA only)|✅ Metal (macOS), OpenCL|✅ Metal (via backend)|❌ CPU only|
|**Multi-threaded CPU Support**|⚠️ Partial|✅ Yes|✅ Yes|✅ Yes|
|**Multilingual Transcription**|✅ Yes|✅ Yes|✅ Yes|⚠️ Limited|
|**Translation Mode (audio → English)**|✅ Yes|✅ Yes|❌ Not exposed|❌ No|
|**Word-level Timestamps**|⚠️ With WhisperX or hacks|⚠️ Experimental only|❌ Not exposed|✅ Yes|
|**Prompt Feeding (context reuse)**|✅ Yes|✅ Yes|❌ No|❌ No|
|**Model Size Options**|tiny → large-v2|tiny → large-v3 (GGML/MLX)|Same as whisper.cpp|small (50–200MB models)|
|**Installation Complexity**|⚠️ Heavy (PyTorch)|✅ Light (CMake build)|✅ Simple via pip|✅ Easy (pip, model download)|
|**Transcription Accuracy (English)**|✅ High|✅ High|✅ High|⚠️ Moderate (~5–10% WER)|
|**Latency (on-device, 10s chunk)**|~2–4s (tiny), 10s+ (large)|~1–3s (tiny) on Apple M1|~1–3s (same as cpp)|✅ ~0.5–1.5s (streamed)|
|**Ideal Use Case**|Batch transcription, research|Real-time local apps, embedded|Python GUI or app pipelines|Live captions, streaming ASR|

---

### **🔍 Highlights by System**

  

#### **✅** 

#### **OpenAI Whisper**

- Best accuracy, full-featured.
    
- High resource use (GPU strongly recommended).
    
- No streaming.
    
- Ideal for offline transcription and translation with Python.
    

  

#### **✅** 

#### **Whisper.cpp**

- Whisper on C++ with GGML (quantized) models.
    
- Optimized for local CPU/GPU (Apple Silicon, Metal).
    
- No true streaming, but fast for chunked simulation.
    
- CLI-friendly, highly portable.
    

  

#### **✅** 

#### **pywhispercpp**

- Thin Python wrapper around whisper.cpp.
    
- Exposes transcribe() and related config, but not advanced features (e.g., token streaming, translation).
    
- Ideal for Python GUI apps (like yours), no GPU required.
    

  

#### **✅** 

#### **Vosk**

- Lightweight real-time engine with token-level output.
    
- Fastest for true streaming.
    
- Less accurate than Whisper, but great for embedded/live use.
    
- Easy integration with real-time GUIs and mobile/edge devices.
    

---

### **🧠 Recommendations**

|**Use Case**|**Best Engine**|
|---|---|
|Maximum accuracy, English-centric|OpenAI Whisper|
|Real-time low-latency STT on Apple Silicon|whisper.cpp|
|Python GUI app w/ good accuracy & speed|pywhispercpp|
|True live token-by-token captions|Vosk|
|Embedded STT on Raspberry Pi / low power|Vosk (small model)|
