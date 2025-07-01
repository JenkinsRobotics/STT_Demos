# **Engineering Note: Whisper STT – Python Binding with pywhispercpp**

  

**Project Name:** Whisper STT – Python Binding with pywhispercpp
**Log ID:** 005
**Date:** 2025-06-25
**Status:** ✅ Completed

**Tags:** #STT #Whisper #WhisperCpp #Python #OfflineAI #MetalGPU #RealTime

---

### **🔧 Objective**

  

Evaluate and integrate the pywhispercpp Python wrapper for Whisper.cpp to enable fast, offline speech-to-text inference with Metal GPU acceleration on Apple Silicon. Assess viability for use in local real-time transcription pipelines and GUI-based STT tools.

---

### **🗂️ Summary**

|**Item**|**Details**|
|---|---|
|**Wrapper Used**|[pywhispercpp](https://github.com/absadiki/pywhispercpp)|
|**Platform**|macOS (Apple Silicon – M1 Max)|
|**Python Version**|3.11.9|
|**GPU Acceleration**|✅ Metal (confirmed in logs)|
|**Transcription Mode**|✅ File input🟡 Real-time preview via audio queues|
|**Use Case**|Offline, low-latency STT in GUI or CLI tools|

---

### **📦 Installation**

```
pip uninstall whispercpp  # If previously installed
pip install pywhispercpp
```

No manual CMake, model download, or whisper.cpp build steps required — all handled via pip.

---

### **📁 Model Handling**

  

Models are automatically downloaded to:

```
~/Library/Application Support/pywhispercpp/models/
```

Supported models include:

- tiny, tiny.en
    
- base, base.en
    
- small, medium, large
    

---

### **🧪 Example Usage (Batch)**

```
from pywhispercpp.model import Model

model = Model(model_name="tiny.en")
text = model.transcribe("jfk_moon.wav")
print(text)
```

✅ Output includes progress updates and confirms Metal GPU usage:

```
whisper_default_buffer_type: using device Metal (Apple M1 Max)
Progress: 100%
```

---

### **🖥 GUI Integration**

  

A real-time GUI app was implemented using pywhispercpp, PySide6, and sounddevice. Key features:

- Mic input + volume meter
    
- Partial + final transcript display
    
- 3-second and 10-second rolling audio buffers
    
- Export transcript to .txt
    
- Streamed inference with overlap de-duplication logic
    

  

> ⚠️ PySide6 UI updates must be handled in the main thread to avoid segmentation faults or QTextDocument errors.

---

### **🧠 Real-Time Observations**

- While not truly token-streaming, pywhispercpp handles 3s and 10s rolling window buffers well.
    
- Best performance achieved by segmenting audio and extracting the center portion (50%) to append final text.
    
- For long sessions (20+ mins), stable behavior was maintained using memory-efficient buffers.
    
- Duplication filtering was partially implemented; LLM-based cleanup was proposed for future improvement.
    

---

### **🗑️ Legacy Cleanup**

  

You can safely delete if transitioning to pywhispercpp fully:

- whisper.cpp/
    
- models/ (unless manually managed for Whisper.cpp CLI)
    

---

### **✅ Summary**

  

pywhispercpp is a powerful and easy-to-integrate wrapper for Whisper.cpp. It offers:

- 🧠 High transcription quality
    
- ⚡ Fast Metal-accelerated decoding on Apple Silicon
    
- 🖥 GUI-ready for PySide6 integration
    
- 📡 Partial support for real-time streaming via chunked buffers
    

  

It is now a top candidate for offline STT systems where Whisper accuracy and responsiveness are required without cloud dependencies.
