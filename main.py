#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

from StatusJsonPythonModule import StatusJsonRest
from datetime import datetime
import pyaudio
import os
import sys
import wave
from datetime import datetime as dt
from aion.logger_library.LoggerClient import LoggerClient
from six.moves import queue

log = LoggerClient("CaptureAudioFromMic")

OUTPUT_DIR = "file/output"
RATE = 16000
CHUNK = int(RATE / 1)

class AudioStreaming():
    def __init__(self, rate, chunk, device_index):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self._device_index = device_index
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        if self._audio_interface.get_device_count() - 1 < self._device_index:
            log.print("this device is not exist", 1)
            return None
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
            input_device_index=self._device_index,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

    def output_wave_file(self, audio_data, output_path):
        date = datetime.now()
        now_time_for_file_name = date.strftime("%Y%m%d%H%M%S%f")[:-3]
        now_time_for_metadata = date.isoformat()

        output_file_name = now_time_for_file_name + ".wav"
        output_file_path = os.path.join(output_path, output_file_name)

        with wave.open(output_file_path, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self._rate)
            wav.writeframes(audio_data)

        return (output_file_path, now_time_for_metadata)

@log.function_log
def main():
    # read status json file
    argv = sys.argv
    if len(argv) != 2:
        device_index = 0
    else:
        device_index = int(argv[1])

    current_path=\
        os.path.dirname(os.path.join(os.getcwd(),  __file__))
    output_path = os.path.join(current_path, OUTPUT_DIR)
    os.makedirs(output_path, exist_ok=True)

    statusObj = StatusJsonRest.StatusJsonRest(os.getcwd(), __file__)
    statusObj.initializeStatusJson()

    statusObj.setNextService(
        "SpeechToTextByStreaming",
        "/home/latona/poseidon/Runtime/speech-to-text-by-streaming",
        "python", "main.py")

    print(">>> start audio recording")
    with AudioStreaming(RATE, CHUNK, device_index) as stream:
        stream_generator = stream.generator()
        for audio_data in stream_generator:
            statusObj.resetOutputJsonFile()

            output_file_path, timestamp = stream.output_wave_file(audio_data, output_path)

            statusObj.setOutputFileData(output_file_path, "file", "audio-wav-mono")
            statusObj.setMetadataValue("timestamp", timestamp)
            statusObj.outputJsonFile()
            log.print("> Success: output audio (path: {}, time:{})"
                .format(output_file_path, timestamp))

if __name__ == "__main__":
    main()
