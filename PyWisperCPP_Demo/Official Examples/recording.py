#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple example showcasing how to use pywhispercpp to transcribe a recording.
"""
import logging
import sounddevice as sd
import pywhispercpp.constants
from pywhispercpp.model import Model
import importlib.metadata


__version__ = importlib.metadata.version('pywhispercpp')

__header__ = f"""
===================================================================
PyWhisperCpp
A simple example of transcribing a recording, based on whisper.cpp
Version: {__version__}               
===================================================================
"""


class Recording:
    """
    Recording class

    Example usage
    ```python
    from pywhispercpp.examples.recording import Recording

    myrec = Recording(5)
    myrec.start()
    ```
    """
    def __init__(self,
                 duration: int,
                 model: str = 'medium.en',
                 **model_params):
        self.duration = duration
        self.sample_rate = pywhispercpp.constants.WHISPER_SAMPLE_RATE
        self.channels = 1
        self.pwcpp_model = Model(model, print_realtime=True, **model_params)

    def start(self):
        logging.info(f"Start recording for {self.duration}s ...")
        recording = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=self.channels)
        sd.wait()
        logging.info('Duration finished')
        res = self.pwcpp_model.transcribe(recording)
        self.pwcpp_model.print_timings()


def _main():
    print(__header__)
    # Set your desired duration and model here
    duration = 5  # seconds
    model = 'tiny.en'  # or any other model you want

    myrec = Recording(duration=duration, model=model)
    myrec.start()


if __name__ == '__main__':
    _main()