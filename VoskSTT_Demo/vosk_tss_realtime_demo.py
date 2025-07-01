"""
VoskSTTDemo.py — Simple Offline STT GUI using Vosk + PySide6
Author: [Your Name]
Date: 2025-06-25

Description:
A lightweight desktop app for live speech-to-text transcription using the Vosk engine.
Features include:
- Real-time microphone capture and transcription
- QTextEdit display styled like printed paragraphs
- Model selector with auto-detection from local `models/` folder
- Export and clear functions
- Volume meter and live partial text

Requirements:
- vosk
- sounddevice
- numpy, scipy
- PySide6
"""

import sys
import os
import queue
import json
import threading
import numpy as np
import scipy.signal
import sounddevice as sd

from vosk import Model, KaldiRecognizer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QProgressBar, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QTextOption


class VoskSTTDemo(QWidget):
    # Qt signals for thread-safe UI updates
    new_text = Signal(str)
    new_partial = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🗣️ Vosk STT - Simple Demo")
        self.resize(600, 560)

        # Audio and model variables
        self.device_index = None
        self.input_samplerate = 16000
        self.q = queue.Queue()
        self.running = False
        self.model_path = None
        self.transcript_log = []
        self.current_volume = 0

        # Initialize UI
        self.init_ui()

        # Signal connections
        self.new_text.connect(self.add_transcript)
        self.new_partial.connect(self.update_partial)

        # GUI refresh timer (volume meter and status)
        self.gui_timer = QTimer(self)
        self.gui_timer.setInterval(200)
        self.gui_timer.timeout.connect(self.update_gui)
        self.gui_timer.start()

    def init_ui(self):
        layout = QVBoxLayout()

        # Model selector
        self.model_selector = QComboBox()
        self.model_selector.addItem("🔍 Choose model...")
        self.model_selector.currentIndexChanged.connect(self.on_model_selected)

        # Status label and volume meter
        self.status_label = QLabel("🔴 Status: Not Listening")
        self.volume_meter = QProgressBar()
        self.volume_meter.setRange(0, 100)
        self.volume_meter.setTextVisible(False)

        # Live partial transcript
        self.partial_label = QLabel("📝 Speaking: ")
        self.partial_label.setStyleSheet("font-style: italic; color: #666;")
        self.partial_label.setWordWrap(True)

        # Main transcript display (book-style)
        self.transcript_box = QTextEdit()
        self.transcript_box.setReadOnly(True)
        self.transcript_box.setWordWrapMode(QTextOption.WordWrap)
        self.transcript_box.setStyleSheet("font-family: serif; font-size: 14px; padding: 8px;")

        # Control buttons
        self.button_start = QPushButton("▶️ Start")
        self.button_stop = QPushButton("⏹️ Stop")
        self.button_clear = QPushButton("🧹 Clear")
        self.button_export = QPushButton("💾 Export")

        self.button_start.clicked.connect(self.start_listening)
        self.button_stop.clicked.connect(self.stop_listening)
        self.button_clear.clicked.connect(self.clear_transcript)
        self.button_export.clicked.connect(self.export_transcript)

        # Layout assembly
        button_row = QHBoxLayout()
        button_row.addWidget(self.button_start)
        button_row.addWidget(self.button_stop)
        button_row.addWidget(self.button_clear)
        button_row.addWidget(self.button_export)

        layout.addWidget(self.model_selector)
        layout.addWidget(self.status_label)
        layout.addWidget(self.volume_meter)
        layout.addWidget(self.transcript_box)
        layout.addWidget(self.partial_label)
        layout.addLayout(button_row)

        self.setLayout(layout)
        self.populate_model_list()

    def populate_model_list(self):
        """Scan 'models/' folder and populate the dropdown."""
        base_dir = "models"
        if not os.path.exists(base_dir):
            return
        for name in os.listdir(base_dir):
            full = os.path.join(base_dir, name)
            if os.path.isdir(full) and os.path.exists(os.path.join(full, "conf")):
                self.model_selector.addItem(name, full)
        if self.model_selector.count() > 1:
            self.model_selector.setCurrentIndex(1)

    def on_model_selected(self, index):
        """Trigger model loading when a model is selected."""
        if index == 0:
            path = QFileDialog.getExistingDirectory(self, "Select Vosk Model Folder")
            if path:
                self.model_path = path
                self.load_model()
                name = os.path.basename(path)
                self.model_selector.insertItem(1, name, path)
                self.model_selector.setCurrentIndex(1)
        else:
            self.model_path = self.model_selector.itemData(index)
            self.load_model()

    def load_model(self):
        """Load the selected Vosk model."""
        try:
            print(f"[STT] Loading model: {self.model_path}")
            self.model = Model(self.model_path)
            self.rec = KaldiRecognizer(self.model, 16000)
            self.status_label.setText(f"✅ Model Loaded: {os.path.basename(self.model_path)}")
        except Exception as e:
            self.status_label.setText("❌ Failed to load model")
            print(f"[STT] ERROR: {e}")

    def update_gui(self):
        """Update status and volume meter."""
        self.status_label.setText(
            f"🟢 Listening ({os.path.basename(self.model_path)})" if self.running else "🔴 Not Listening"
        )
        self.volume_meter.setValue(min(int(self.current_volume * 100), 100))

    def start_listening(self):
        """Start audio capture thread."""
        if self.running or not hasattr(self, "model"):
            return
        self.running = True

        if self.device_index is None:
            self.device_index = sd.default.device[0]

        info = sd.query_devices(self.device_index, 'input')
        self.input_samplerate = int(info['default_samplerate'])

        threading.Thread(target=self.listen_loop, daemon=True).start()

    def stop_listening(self):
        """Stop audio thread."""
        self.running = False

    def listen_loop(self):
        """Main STT audio loop."""
        def audio_callback(indata, frames, time, status):
            if status:
                print("[Audio]", status)
            self.q.put(indata.copy())
            self.current_volume = min(np.linalg.norm(indata), 1.0)

        try:
            with sd.InputStream(
                samplerate=self.input_samplerate,
                blocksize=int(self.input_samplerate * 0.1),
                dtype='float32',
                channels=1,
                device=self.device_index,
                callback=audio_callback
            ):
                while self.running:
                    indata = self.q.get()
                    resampled = scipy.signal.resample(
                        indata[:, 0],
                        int(len(indata) * 16000 / self.input_samplerate)
                    )
                    samples = np.int16(resampled * 32767).tobytes()
                    if self.rec.AcceptWaveform(samples):
                        result = json.loads(self.rec.Result())
                        self.new_text.emit(result.get("text", ""))
                    else:
                        partial = json.loads(self.rec.PartialResult()).get("partial", "")
                        self.new_partial.emit(partial)
        except Exception as e:
            print("[STT] ERROR:", e)

    def add_transcript(self, text):
        """Append final transcript text as paragraph."""
        if not text:
            return
        self.transcript_log.append(text)
        self.transcript_box.append(text + "\n")

    def update_partial(self, partial):
        """Update live partial transcript below the main box."""
        self.partial_label.setText(f"📝 Speaking: {partial}")

    def clear_transcript(self):
        """Clear transcript log and UI."""
        self.transcript_log.clear()
        self.transcript_box.clear()
        self.partial_label.setText("📝 Speaking: ")

    def export_transcript(self):
        """Export transcript to .txt file."""
        if not self.transcript_log:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Transcript", "transcript.txt", "Text Files (*.txt)")
        if path:
            with open(path, "w") as f:
                f.write("\n\n".join(self.transcript_log))
            print(f"[STT] Transcript saved to {path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoskSTTDemo()
    window.show()
    sys.exit(app.exec())