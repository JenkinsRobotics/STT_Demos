# **Engineering Note: Vosk STT Standalone GUI Test**

  

**Project Name:** Vosk STT Standalone GUI Test

**Focus:** Local Speech-to-Text Evaluation

**Log:** 003

**Date:** 2025-06-24

**Status:** ✅ Completed

**Tags:** #AIAudio #STT #OfflineVoice #Kaldi

---

### **🔍** 

### **Current Objective**

  

Evaluate the **accuracy**, **responsiveness**, and **usability** of **Vosk STT** in a self-contained **PySide6 GUI** application on **macOS**.

Target use case: always-on local agents, real-time transcription display, and low-latency offline performance.

---

### **🧠** 

### **Model Information**

- **Library:** Vosk
    
- **Version:** 0.3.45
    
- **Primary Model:** vosk-model-small-en-us-0.15 (40 MB)
    
- **High-Accuracy Models Tested:**
    
    - vosk-model-en-us-0.22 (1.8 GB)
        
    - vosk-model-en-us-0.42-gigaspeech (2.3 GB)
        
    
- **Developer:** Alpha Cephei
    
- **License:** Apache 2.0
    
- **GitHub:** [alphacep/vosk-api](https://github.com/alphacep/vosk-api)
    

---

### **📦** 

### **Installation**

```
pip install vosk sounddevice scipy numpy PySide6
```

Model downloads available at:

🔗 https://alphacephei.com/vosk/models

---

### **📈** 

### **Supported English Models**

|**Model**|**Size**|**WER (LibriSpeech)**|**Use Case**|
|---|---|---|---|
|vosk-model-small-en-us-0.15|40 MB|~9.85%|Lightweight, real-time, embedded|
|vosk-model-en-us-0.22|1.8 GB|~5.69%|High accuracy, general-purpose|
|vosk-model-en-us-0.22-lgraph|128 MB|~7.82%|Language graph decoding|
|vosk-model-en-us-0.42-gigaspeech|2.3 GB|~5.64%|Best for clean, long-form audio|

✅ **Recommendation:** Use 0.22 or gigaspeech for best accuracy. Use 0.15 for fast, embedded usage.

---

### **🖥️** 

### **GUI App Features**

- 🎙️ Microphone-based real-time transcription
    
- 📝 Final and partial result handling
    
- 📄 Paragraph-style transcript view
    
- 📊 Voice volume meter
    
- 💾 Transcript export to .txt
    
- 🧠 Model selector via local models/ folder
    

---

### **⚙️** 

### **How It Works**

- Captures audio via sounddevice
    
- Resamples to 16 kHz
    
- Streams input through KaldiRecognizer
    
- Updates live label with .PartialResult()
    
- Appends finalized text with .Result()
    
- All updates run in the **main event loop** (no threading required)
    

---

### **⏱️** 

### **Example Results**

|**Model**|**Latency**|**Accuracy**|
|---|---|---|
|Small (0.15)|~0.5–0.8 sec|~90–95%|
|Full (0.22)|~0.9–1.2 sec|~97%+|

---

### **🧠** 

### **Backend & Performance**

|**Device**|**Backend**|**Supported**|**Performance**|
|---|---|---|---|
|CPU|int16|✅ Yes|⚡ Real-time (0.5–1.0s)|
|GPU / Metal|N/A|❌ No|Not supported|
|ANE (Apple)|N/A|❌ No|Not available|

✅ Works well on **Apple Silicon** using native **Python 3.11+** or via Rosetta.

---

### **🛠️** 

### **Usage Instructions**

```
python voskstt_demo.py
```

Steps:

1. Select or confirm model path
    
2. Click ▶️ Start
    
3. Speak into the mic
    
4. View live partial + confirmed transcripts
    
5. Click 💾 to export transcript to .txt
    

---

### **🧪** 

### **Performance Notes**

- .PartialResult() ensures smooth real-time feedback
    
- No memory leaks observed in extended (30+ min) sessions
    
- Robust in moderate background noise
    
- Automatically resumes after pauses or dropped input
    

---

### **🧩** 

### **Future Enhancements**

- 🔇 Add optional **VAD** (silence detection)
    
- ⏱️ Enable **word-level timestamps**
    
- ⚖️ Add **side-by-side comparison** with Whisper.cpp
    
- 📈 Include audio waveform or spectrogram view
    
- 🧑‍🤝‍🧑 Enable **offline speaker segmentation** using Kaldi
    

---

### **📂** 

### **Official Example Directory**

  

🔗 GitHub: [vosk-api/python/example](https://github.com/alphacep/vosk-api/tree/master/python/example)

|**File**|**Purpose**|**Notes**|
|---|---|---|
|test_microphone.py|🎤 Real-time mic transcription|Shows live partial + final text|
|test_simple.py|🧾 Basic WAV file transcription|Simplest offline example|
|test_words.py|🧩 Word-by-word output with timing|Use for subtitles (SRT/VTT)|
|test_word_timestamps.py|⏱️ Start/end time per word|Useful for UI alignment|
|test_audio.py|🧼 Raw audio buffer transcription|Good for non-mic input pipelines|
|test_speaker.py|🧑‍🤝‍🧑 Speaker diarization (multi-speaker)|Needs speaker model|
|test_server.py|🌐 WebSocket-based live transcription server|For web or network apps|

---

### **🧪** 

### **Recommended Workflow to Explore Vosk**

  

**1. Clone + Setup**

```
git clone https://github.com/alphacep/vosk-api
cd vosk-api/python/example
pip install vosk sounddevice
```

**2. Download a Model**

- 🔹 [Small (40MB)](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
    
- 🔹 [Large (180MB)](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip)
    

```
unzip vosk-model-small-en-us-0.15.zip -d model
```

**3. Run the Demo**

```
python test_microphone.py
```

- "partial": interim live result
    
- "text": finalized output
    

---

### **🔍** 

### **Vosk Transcription API – Core Logic**

  

All scripts use the same core API built around KaldiRecognizer.

|**Function**|**Purpose**|**Common In**|
|---|---|---|
|rec.AcceptWaveform(data)|Ingests audio and checks if ready|All scripts|
|rec.Result()|Returns finalized JSON output|Files + Mic|
|rec.PartialResult()|Returns partial (interim) text|Real-time/mic|
|rec.FinalResult()|Returns final text at end of stream|WAV/file demos|
|rec.SetWords(True)|Enables word-level timestamps|Subtitles/word UI|
|rec.SetMaxAlternatives(N)|Allows N-best hypotheses|Alternatives demo|
|rec.SetGrammar(...)|Restrict output to a grammar list|Command mode|

**Decoder loop used in all scripts:**

```
if rec.AcceptWaveform(data):
    print(rec.Result())
else:
    print(rec.PartialResult())
```

---

### **🧠** 

### **Script Comparison**

|**Use Case**|**Input Type**|**Output Type**|**Extras Used**|
|---|---|---|---|
|test_microphone.py|Live Mic|Partial + Final|PartialResult(), Result()|
|test_simple.py|WAV File|Final Only|Result(), FinalResult()|
|test_words.py|WAV File|Final + Word Times|SetWords(True)|
|test_alternatives.py|WAV File|N-best + Word Times|SetWords(True), SetMaxAlternatives()|
|test_grammar.py|WAV File|Constrained Phrases|SetGrammar(...)|

---

### **✅** 

### **Summary**

  

Vosk is a fast, fully offline transcription engine built for local-first applications. With consistent APIs, open licensing, and CPU-only design, it’s ideal for embedded systems, Raspberry Pi, macOS desktops, or privacy-centric tools.

  

The official examples make it easy to experiment with mic input, WAV files, timestamps, and speaker diarization. Combined with a simple PySide6 GUI, it becomes a reliable, low-latency transcription tool.

---

**Engineer:** Jonathan Jenkins

**Log Status:** ✅ Completed

**Final Notes:** Vosk is a solid, stable, and practical STT solution for real-time local agents, with flexible APIs and broad deployment options.
