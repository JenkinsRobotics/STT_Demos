#!/usr/bin/env python3

# Prerequisites: https://alphacephei.com/vosk/install
# Install Python dependencies: pip install vosk sounddevice
# Example usage: python test_microphone.py -m en-us

import argparse
import queue
import sys
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()

# === Path Configuration ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """Called from a separate thread for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# === Argument Parsing (device list first) ===
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-l", "--list-devices", action="store_true", help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    sys.exit(0)

# === Main Argument Parser ===
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser]
)
parser.add_argument("-f", "--filename", type=str, metavar="FILENAME", help="audio file to store recording to")
parser.add_argument("-d", "--device", type=int_or_str, help="input device (numeric ID or substring)")
parser.add_argument("-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument("-m", "--model", type=str, help="model subfolder name, e.g. en-us or vosk-model-en-us-0.22")
args = parser.parse_args(remaining)

try:
    # Determine sample rate if not specified
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        args.samplerate = int(device_info["default_samplerate"])

    # Load model from local folder
    model_name = args.model or "vosk-model-en-us-0.42-gigaspeech"
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        print(f"❌ Model folder not found: {model_path}")
        sys.exit(1)

    model = Model(model_path=model_path)

    # Setup optional WAV output
    dump_fn = open(args.filename, "wb") if args.filename else None

    # Start microphone input
    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                           dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("🎤 Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(rec.PartialResult())
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\n✅ Done")
    sys.exit(0)
except Exception as e:
    sys.exit(f"{type(e).__name__}: {str(e)}")