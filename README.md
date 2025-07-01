## Jenkins Robotics  
# STT_Demos – Local Speech Recognition Showcase  

<!-- This is commented out. -->

## Project Information  

Project Status : <mark style="background-color: green"> &nbsp; ACTIVE &nbsp;</mark>  
Code Status : <mark style="background-color: green"> &nbsp; STABLE &nbsp;</mark>  
Development Status : <mark style="background-color: orange"> &nbsp; ONGOING &nbsp;</mark>  

&nbsp;  
## General Information  

This project is a growing collection of local/offline STT (Speech-to-Text) demos used to benchmark and explore different open-source speech recognition engines. Designed for robotics and voice interface applications, each demo includes either a real-time or batch processing interface for fast testing and integration.  

Goals include:
- [x] Evaluate transcription speed and accuracy  
- [x] Compare real-time vs batch models  
- [x] Support macOS (Apple Silicon) with MPS where applicable  
- [x] Build a foundation for full-duplex speech interaction  
- [x] Integrate with TTS_Demos in future agents  
- [x] Add transcript benchmarking + WER tools  
- [x] Measure latency, duplication, and streaming fidelity  

<!--  
&nbsp;  
## WATCH DEMOS ON YOUTUBE  

Watch the demo playlist and future voice tests on YouTube.  

[![image alt text](http://img.youtube.com/vi/w-qWbZ5-IQw/0.jpg)](https://youtube.com/playlist?list=PLNTKXZ4hgP_jekZOWw05JcJtyseCdSsIV "YouTube")  
-->

&nbsp;  
## Support  

Like our work? Consider supporting Jenkins Robotics!  

Subscribe ➔ https://www.youtube.com/@Jenkins_Robotics   <br>  
Patreon ➔ https://www.patreon.com/JenkinsRobotics  <br>  
Venmo ➔ https://venmo.com/u/JenkinsRobotics  <br>  

&nbsp;  
## Table of Contents  

**[STT Engines Included](#stt-engines-included)**<br>  
**[Installation Instructions](#installation-instructions)**<br>  
**[CLI + Real-Time App Summaries](#cli--real-time-app-summaries)**<br>  
**[Next Steps](#next-steps)**<br>  
**[Licenses and Credits](#licenses-and-credits)**<br>  

&nbsp;  
## STT Engines Included  

| Engine         | Interface     | Offline? | Notes |
|----------------|---------------|----------|-------|
| Vosk           | Real-time     | ✅ Yes   | Fast, lightweight, low-memory CPU STT |
| FasterWhisper  | Real-time     | ✅ Yes   | CTranslate2-backed Whisper. High accuracy, CPU-only on Mac |
| Whisper.cpp    | CLI + GUI     | ✅ Yes   | Metal/ANE-accelerated C++ engine for macOS |
| pywhispercpp   | Python API    | ✅ Yes   | Metal-accelerated Python bindings for Whisper.cpp |
| Whisper MLX    | File          | ✅ Yes   | GPU-accelerated MLX backend for macOS |
| RealTimeSTT    | Real-time     | ✅ Yes   | Lightweight real-time demo |
| SpeechRecSTT   | Real-time     | ✅ Yes   | Uses Python’s SpeechRecognition/pocketsphinx |

&nbsp;  
## Installation Instructions  

Clone this repo and install dependencies for each STT demo as needed. For macOS (Apple Silicon recommended):  

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To run a demo:  
```bash
python whisper_stt.py         # Whisper offline
python vosk_stt.py            # Vosk-based
python real_time_stt.py       # Stream + print live transcript
python speechrec_stt.py       # SpeechRecognition (pocketsphinx)
```

To run Whisper.cpp CLI-based GUI:  
```bash
python whisper_gui_app.py     # Runs rolling 10s inference using whisper.cpp
```

&nbsp;  
## CLI + Real-Time App Summaries  

- **whisper_gui_app.py**  
  Uses Whisper.cpp via CLI, transcribes 10s rolling mic buffers. Shows final, clean transcript and saves to `.txt`.

- **whisper_stt.py**  
  Runs FasterWhisper (CTranslate2) on CPU. GUI with volume meter and chunked partial/final transcript view.

- **vosk_stt.py**  
  Lightweight Kaldi-based transcription. Fast and accurate. CPU only.

- **pywhispercpp_demo.py**  
  GPU-accelerated via Metal. Uses pywhispercpp binding and simple file-based API.

- **mlx_whisper_stt.py**  
  Apple MLX version of Whisper. Fast file-based inference with `whisper-medium` model.

- **real_time_stt.py**  
  Basic microphone streaming demo. Updates in real time.

- **speechrec_stt.py**  
  Fully offline. Uses pocketsphinx via SpeechRecognition for basic commands.

&nbsp;  
## Next Steps  

- Add real-time MLX streaming demo  
- Add Whisper.cpp streaming support (token-by-token if available)  
- Integrate LLM to clean up repetitive transcripts  
- Export transcripts + benchmark against ground truth  
- Build full-duplex loop with TTS_Demos + interrupt handling  

&nbsp;  
## Links  

SUPPORT US ►  

Subscribe ➔ https://www.youtube.com/@Jenkins_Robotics<br>
Patreon ➔ https://www.patreon.com/JenkinsRobotics  <br>
Venmo ➔ https://venmo.com/u/JenkinsRobotics <br>

FOLLOW US ►

Discord ➔ https://discord.gg/sAnE5pRVyT <br>
Patreon ➔ https://www.patreon.com/JenkinsRobotics <br>
Twitter ➔ https://twitter.com/jenkinsrobotics  <br>
Instagram  ➔ https://www.instagram.com/jenkinsrobotics/ <br>
Facebook ➔ https://www.facebook.com/jenkinsrobotics/  <br>
GitHub  ➔ https://jenkinsrobotics.github.io <br>

&nbsp;  
## Licenses and Credits  

All third-party models and libraries retain their original licenses. This repo is intended for R&D, robotics, and AI voice assistant prototyping.  

© Jenkins Robotics 2025