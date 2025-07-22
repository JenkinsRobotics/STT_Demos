#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Realtime microphone transcription using pywhispercpp.

This version captures audio from your microphone, buffers it,
and sends segments to whisper.cpp for transcription in a separate process.
"""
import argparse
import logging
from multiprocessing import Process
import numpy as np
import pywhispercpp.constants as constants
import sounddevice as sd
from pywhispercpp.model import Model
import importlib.metadata
import os # Added for os.getpid() in logging

__version__ = importlib.metadata.version('pywhispercpp')

__header__ = f"""
========================================================
PyWhisperCpp Microphone Livestream Transcription
Version: {__version__}
========================================================
"""

# Configure logging for better visibility
# You can change the level to logging.WARNING or logging.ERROR to suppress
# some of the detailed pywhispercpp/ggml output if it's too verbose.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class LiveStream:
    """
    LiveStream class adapted for microphone input.

    Captures audio from a specified input device (microphone),
    buffers it for a set duration, and then transcribes the
    audio segment using whisper.cpp in a separate process.
    """

    def __init__(self,
                 input_device: int = None,
                 model='medium.en',
                 block_size: int = 1024,
                 transcription_buffer_duration_seconds: int = 5,
                 n_threads: int = -1,
                 **kwargs_for_whisper_params):
        """
        :param input_device: The ID of the microphone input device.
                             Leave as None to use the default system input device.
        :param model: whisper.cpp model (e.g., 'tiny.en', 'base', 'small').
        :param block_size: The number of frames passed to the sounddevice callback at a time.
                           Smaller blocks mean lower latency but higher CPU usage.
        :param transcription_buffer_duration_seconds: The duration (in seconds) of audio to
                                                      accumulate before triggering a transcription.
        :param n_threads: Number of threads for whisper.cpp inference. Default to -1 (auto).
        :param kwargs_for_whisper_params: Any other whisper.cpp specific parameters that map to whisper_full_params.
        """
        self.input_device = input_device
        self.block_size = block_size
        self.transcription_buffer_duration_seconds = transcription_buffer_duration_seconds

        self.channels = 1
        self.samplerate = constants.WHISPER_SAMPLE_RATE

        self.audio_data = np.array([], dtype=np.float32)

        self.model_name = model
        self.n_threads = n_threads
        self.kwargs_for_whisper_params = kwargs_for_whisper_params

    @staticmethod
    def _transcribe_process(model_name: str, n_threads: int, kwargs_for_whisper_params: dict, audio_segment: np.ndarray):
        """
        Target function for the multiprocessing Process.
        This function runs in a separate process and initializes its own
        pywhispercpp Model instance to perform transcription.
        """
        logging.info(f"Process {os.getpid()}: Initializing Whisper model '{model_name}'...")
        transcriber_model = Model(model_name,
                                  n_threads=n_threads,
                                  **kwargs_for_whisper_params)
        
        logging.info(f"Process {os.getpid()}: Transcribing audio segment of {len(audio_segment) / constants.WHISPER_SAMPLE_RATE:.2f} seconds...")
        
        # Perform the transcription and capture the result
        result = transcriber_model.transcribe(audio_segment)
        
        # --- NEW: Print the transcription result clearly ---
        print("\n" + "="*50)
        print(f"[{os.getpid()}] TRANSCRIBED: {result}")
        print("="*50 + "\n")
        # --- END NEW ---


    def _input_audio_callback(self, indata, frames, time, status):
        """
        Callback function for the sounddevice InputStream.
        This function is called repeatedly with new audio data from the microphone.
        """
        if status:
            logging.warning(f"Audio callback status: {status}")

        current_audio_segment = indata.flatten()
        self.audio_data = np.append(self.audio_data, current_audio_segment)

        target_samples = int(self.samplerate * self.transcription_buffer_duration_seconds)

        if self.audio_data.size >= target_samples:
            logging.info(f"Accumulated {self.audio_data.size} samples ({self.audio_data.size / self.samplerate:.2f}s). Triggering transcription...")
            audio_for_process = self.audio_data.copy()
            
            p = Process(target=LiveStream._transcribe_process,
                        args=(self.model_name, self.n_threads, self.kwargs_for_whisper_params, audio_for_process))
            p.start()
            
            self.audio_data = np.array([], dtype=np.float32)

    def start(self):
        """
        Starts the microphone audio input stream and transcription process.
        """
        logging.info("Starting microphone input for transcription...")

        try:
            with sd.InputStream(
                device=self.input_device,
                samplerate=self.samplerate,
                blocksize=self.block_size,
                channels=self.channels,
                dtype='float32',
                callback=self._input_audio_callback
            ) as in_stream:
                device_id_to_query = self.input_device if self.input_device is not None else sd.default.device[0]
                device_info = sd.query_devices(device_id_to_query)
                device_name = device_info['name']
                hostapi_name = sd.query_hostapis(device_info['hostapi'])['name']

                logging.info(f'Listening on input device: "{device_name}" (Host API: "{hostapi_name}")')
                logging.info(f'Sample Rate: {self.samplerate} Hz, Block Size: {self.block_size} frames')
                logging.info(f'Transcription triggered approximately every {self.transcription_buffer_duration_seconds} seconds of audio.')
                logging.info('Press Ctrl+C to stop.')

                while True:
                    sd.sleep(1000)
        except KeyboardInterrupt:
            logging.info("Transcription stopped by user.")
        except Exception as e:
            logging.error(f"Error starting audio stream: {e}")
            logging.error("Please check if the input device is correctly specified and available.")
            logging.error("You can list available devices using: python your_script_name.py --list-devices")

    @staticmethod
    def available_devices():
        """Lists all available audio input and output devices."""
        return sd.query_devices()

def _main():
    print(__header__)
    parser = argparse.ArgumentParser(
        description="Realtime microphone transcription using pywhispercpp.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-m', '--model', default='tiny.en', type=str,
        help="Whisper.cpp model to use (e.g., 'tiny.en', 'base', 'small', 'medium', 'large').\n"
             "Default: %(default)s"
    )
    parser.add_argument(
        '-nt', '--n_threads', type=int, default=3,
        help="Number of threads for whisper.cpp inference. Default: %(default)s"
    )
    parser.add_argument(
        '-id', '--input_device', type=int, default=None,
        help="The ID of the input device (microphone).\n"
             "Leave as None to use the system's default input device.\n"
             "Use --list-devices to see available device IDs."
    )
    parser.add_argument(
        '-bls', '--block_size', type=int, default=1024,
        help="Block size (number of frames) for sounddevice input stream.\n"
             "Smaller blocks reduce latency but may increase CPU usage. Default: %(default)s"
    )
    parser.add_argument(
        '-tbds', '--transcription_buffer_duration_seconds', type=int, default=5,
        help="Duration (in seconds) of audio to accumulate before triggering transcription.\n"
             "Adjust based on desired responsiveness and transcription accuracy. Default: %(default)s"
    )
    parser.add_argument(
        '--list-devices', action='store_true',
        help='List available audio input and output devices and exit.'
    )

    args = parser.parse_args()

    if args.list_devices:
        print("\nAvailable Audio Devices:")
        devices = LiveStream.available_devices()
        if not devices:
            print("No audio devices found.")
        else:
            for i, dev in enumerate(devices):
                print(f"  {i}: {dev['name']} (Input Channels: {dev['max_input_channels']}, Output Channels: {dev['max_output_channels']})")
        return

    ls = LiveStream(
        input_device=args.input_device,
        model=args.model,
        block_size=args.block_size,
        transcription_buffer_duration_seconds=args.transcription_buffer_duration_seconds,
        n_threads=args.n_threads
    )
    ls.start()


if __name__ == '__main__':
    _main()