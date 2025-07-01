# **Engineering Note: FasterWhisper STT GUI Test**

  

**Project Name:** **Whisper STT Standalone GUI Test**
**Focus:** Streaming Speech-to-Text Evaluation
**Log:** 004
**Date:** 2025-06-24
**Status:** ✅ Completed

  

> #AIAudio #STT #Whisper #FasterWhisper

---

### **🎯 Objective**
 

Evaluate the performance and responsiveness of the **faster-whisper** engine (based on CTranslate2) within a real-time PySide6 GUI STT app. Assess its viability for offline, always-on speech agents and compare its usability and accuracy to Whisper.cpp and Vosk.

---

### **📦 Model Details**

- **Library:** [faster-whisper](https://github.com/guillaumekln/faster-whisper)    
- **Engine:** CTranslate2
- **License:** MIT
- **Model Used (default):** tiny.en (153 MB)
- **Model Source:** [Hugging Face](https://huggingface.co/Systran/faster-whisper-tiny.en)

---

### **📁 Model Setup**

  

A script is provided to download all models:

```
python download_all_fasterwhisper_models.py
```

Example structure:

```
project/
├── whisperstt_demo.py
├── download_all_fasterwhisper_models.py
└── models/
    ├── tiny.en/
    ├── base/
    └── medium/
```

Each folder contains:

- model.bin
    
- config.json
    
- tokenizer.json
    
- vocabulary.txt
    

---

### **🧠 Available Models**

|**Model**|**Size**|**Notes**|
|---|---|---|
|tiny|~75 MB|Fastest, lowest accuracy|
|tiny.en|~153 MB|English-only, better accuracy|
|base|~142 MB|Multi-language|
|medium|~1.5 GB|High accuracy|
|large-v3|~2.9 GB|Best accuracy, slowest|

✅ **Recommended for real-time CPU:** tiny.en or base

---

### **🛠 Installation**

```
pip install faster-whisper sounddevice numpy scipy PySide6
```

Optional (for VAD):

```
pip install onnxruntime
```

---

### **⚙️ Backend Config (macOS)**

|**Device**|**Backend**|**Supported**|**Notes**|
|---|---|---|---|
|CPU|int8/f32|✅ Yes|Works well with compute_type="int8"|
|GPU|Metal (MPS)|❌ No|Not supported yet|

---

### **🖥 GUI Features**

- Real-time microphone input
    
- Automatic chunking (~1.5s)
    
- Volume meter
    
- Display of current + final transcript
    
- Transcript export to .txt
    

---

### **📈 Performance (Tiny.en + CPU)**

|**Metric**|**Value**|
|---|---|
|Chunk size|~1.5s|
|Latency|~1.2–1.6s per chunk|
|Accuracy|High|
|CPU Usage|Moderate|
|Real-time|🟡 Partial (delayed)|

---

### **🚫 Limitations**

- Not true token-by-token streaming
    
- Each audio chunk is processed as a full segment
    
- GUI may delay under high load without threading optimizations
    
- MPS / GPU acceleration not available on macOS yet
    

---

### **✅ Strengths**

- Excellent accuracy with tiny.en
    
- Fast CPU-only inference
    
- Simple to integrate into PySide6 GUI
    
- Good for offline agents or robotic use cases
    

---

### **🧪 Future Work**

- Implement true streaming (e.g., rolling window buffer logic)
    
- Add Whisper.cpp or MLX for GPU acceleration
    
- Add LLM-based transcript cleanup post-processor
    
- Improve overlap-debouncing and phrase deduplication
    
- Enable real-time word-level alignment (if possible)
    

---

### **🧾 Summary**

  

FasterWhisper delivers accurate STT via an optimized CTranslate2 backend. While not a true token streamer, it performs well in low-latency offline GUI scenarios. It is an excellent balance of accuracy and speed on CPU-only macOS systems.

  