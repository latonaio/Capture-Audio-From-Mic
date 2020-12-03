#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

# from StatusJsonPythonModule import StatusJsonRest
from datetime import datetime
import pyaudio
import os
import sys
import wave
from datetime import datetime as dt


class CaptureAudioFromMic():
    OUTPUT_DIR = "file/output"
    # sampling_rate = 44100
    # sampling_rate = 48000
    sampling_rate = 32000
    chunk = 4096
    # rec_time = 300
    rec_time = 30
    ch = 1
    fmt = pyaudio.paInt16

    def __init__(self, device_index):
        print(">>> Initialized Audio Device")
        self.device_index = device_index
        self.audio = pyaudio.PyAudio()

        if self.audio.get_device_count() - 1 < device_index:
            print(">>> Error: this device is not exist")
            sys.exit(1)
        print(self.audio.get_device_info_by_index(device_index))

        currentPath =\
            os.path.dirname(os.path.join(os.getcwd(),  __file__))
        self.outputPath = os.path.join(currentPath, self.OUTPUT_DIR)

        os.makedirs(self.outputPath, exist_ok=True)

    def output_wave_file(self):
        print(">>> start opening stream")
        self.stream = self.audio.open(
            format=self.fmt, channels=self.ch, rate=self.sampling_rate,
            input=True, input_device_index=self.device_index,
            frames_per_buffer=self.chunk)
        print(">>> finish opening stream")

        frames = []
        audio_range = int(self.sampling_rate / self.chunk * self.rec_time)
        for i in range(0, audio_range):
            data = self.stream.read(self.chunk)
            frames.append(data)
            
        now_time = datetime.now().strftime("%Y%m%d%H%M%S")+"000"
        outputFileName = now_time + ".wav"
        outputFilePath = os.path.join(self.outputPath, outputFileName)

        with wave.open(outputFilePath, 'wb') as wav:
            wav.setnchannels(self.ch)
            wav.setsampwidth(self.audio.get_sample_size(self.fmt))
            wav.setframerate(self.sampling_rate)
            wav.writeframes(b''.join(frames))

        self.stream.close()
        self.stream.stop_stream()

        return outputFilePath

def main():
    # read status json file
    argv = sys.argv
    if len(argv) != 2:
        device_index = 24
    else:
        device_index = int(argv[1])

    # statusObj = StatusJsonRest.StatusJsonRest(os.getcwd(), __file__)
    # statusObj.initializeInputStatusJson()

    statusObj.setNextService(
        "SpeechToTextByStreaming",
        "/home/latona/poseidon/Runtime/speech-to-text-by-streaming",
        "python", "main.py")

    print(">>> start audio recording")
    while True:
        # statusObj.initializeOutputStatusJson()
        # statusObj.copyToOutputJsonFromInputJson()

        # Edge
        #statusObj.setNextService(
        #    "SpeechToText",
        #    "/home/latona/poseidon/Runtime/voice-to-text/SpeechToText",
        #    "python", "main.py")

        # Cloud
        #statusObj.setNextService(
        #    "SpeechToTextByStreaming",
        #    "/home/latona/athena/Runtime/speech-to-text-by-streaming",
        #    "python", "main.py", "athena")

        outputFilePath = captureObj.output_wave_file()

        # statusObj.setOutputFileData(outputFilePath, "file", "audio-wav-mono")
        # statusObj.setMetadataValue('file_name', outputFilePath)
        # statusObj.outputJsonFile()
        print("> Success: output audio (path: {})".format(outputFilePath))


if __name__ == "__main__":
    main()
