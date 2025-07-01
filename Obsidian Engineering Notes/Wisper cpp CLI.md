
# **Engineering Note 006 – Whisper.cpp STT Standalone GUI Test**

  

**Project Name:** Whisper.cpp STT Standalone GUI Test

**Focus:** GPU-Accelerated Local STT (Metal/CoreML on macOS)

**Log ID:** 006

**Date:** 2025-06-25

**Status:** ✅ Completed

**Tags:** #STT #Whisper #WhisperCPP #OfflineAI #MetalGPU #CLI

---

### **🔧 Objective**

  

Evaluate the performance and latency of **Whisper.cpp**, an optimized C++ port of OpenAI’s Whisper model, on Apple Silicon using **Metal (GPU)** or **CoreML** acceleration. This test uses **direct CLI invocation** (not the Python bindings) in combination with a standalone GUI built in Python (PySide6). Focus areas include transcription speed, segment overlap control, and usability for offline real-time assistants.

---

### **🛠️ Engine Details**

|**Component**|**Description**|
|---|---|
|Engine|[Whisper.cpp](https://github.com/ggerganov/whisper.cpp) (by Georgi Gerganov)|
|Language|C++|
|License|MIT|
|Acceleration|✅ Metal (macOS GPU), ✅ CoreML (Apple Neural Engine)|
|Invocation Mode|❗ CLI only (no Python bindings used in this test)|

---

### **📦 Setup and Build (macOS – Apple Silicon)**

  

#### **1. Prerequisites**

```
xcode-select --install
brew install cmake ffmpeg
```

#### **2. Clone and Build Whisper.cpp**

```
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
mkdir build && cd build
cmake .. -DGGML_METAL=ON
make -j
```

This builds the Metal-accelerated whisper-cli binary at:

```
whisper.cpp/build/bin/whisper-cli
```

---

### **📁 Folder Structure**

```
WHISPERCPP_GUI_DEMO/
├── whisper.cpp/               # Local clone + build of whisper.cpp
├── models/                    # e.g., ggml-medium.en.bin
├── samples/                   # e.g., JFK_moon_full.wav
├── run_whisper_cli.py        # Python script to drive CLI transcription
├── whisper_gui_app.py        # PySide6-based GUI for live transcription
├── transcripts/              # Saved .txt results from real-time STT
```

---

### **🎙️ Live Transcription App (GUI)**

- Input: 10-second rolling audio buffer via sounddevice
    
- Whisper.cpp CLI invoked from Python
    
- Final transcripts appended to scrollable text window
    
- Option to save output to .txt for benchmarking
    
- No multithreading required — avoids Qt thread violations
    
- Segment overlap suppressed via custom debounce filtering
    

---

### **⚙️ Audio Processing**

- Audio chunked in 10s WAV files (16kHz mono)
    
- Converted using scipy and stored in a temporary location
    
- Transcribed via subprocess call to CLI:
    

```
./whisper-cli -m models/ggml-medium.en.bin -f tmp_clip.wav -ng -otxt
```

-   
    
- Only the **center 50%** of each transcript is extracted for final output to reduce duplication and maintain context accuracy.
    

---

### **🧪 Performance Benchmarks**

  

**Test Audio**: JFK “We choose the moon” full speech (~3 min)

|**Metric**|**Value**|
|---|---|
|Inference mode|Whisper CLI (Metal)|
|Model used|ggml-medium.en.bin|
|Chunk size|10 seconds|
|Inference latency|~0.9–1.2s per chunk|
|Avg time per segment|~1.5s total (incl. CLI call)|
|Accuracy (WER, JFK test)|~3.3%|

---

### **✅ Transcription Flow**

1. 10s audio chunk recorded
    
2. Saved as temp WAV file
    
3. Whisper.cpp CLI transcribes to .txt
    
4. Middle 50% of text extracted
    
5. Appends cleanly to transcript display
    
6. Optional .txt export after run
    

---

### **Known Issues**

- ❌ Whisper CLI cannot stream tokens (chunk-based only)
    
- ❌ Long transcriptions may show repetition if segment overlap isn’t filtered
    
- ⚠️ GUI can crash if Qt objects are updated from background threads (fixed with single-thread approach)
    

---

### **🗃️ Transcript Benchmarking**

  

Transcripts can be saved and later compared to reference text using a separate benchmark tool (benchmark_transcript.py) which computes WER, duplicate segments, and alignment quality.

---

### **🧠 Future Enhancements**

- Real-time word-by-word streaming via whisper.cpp token-level output (if supported in future)
    
- Smarter VAD-based chunking instead of fixed 10s buffers
    
- Integrate LLM-based transcript cleaner for deduplication and fluency
    
- GUI voice control + TTS feedback (backchanneling)
    

---

### **Summary**

  

Whisper.cpp CLI with Metal acceleration delivers near-real-time transcription performance on Apple Silicon using local models and a simple chunking system. The GUI demo app shows reliable operation and transcript quality suitable for live agents and assistant applications — all fully offline.

---

**Status:** ✅ Completed

**Engineer:** Jonathan Jenkins

**Date:** 2025-06-25

  

