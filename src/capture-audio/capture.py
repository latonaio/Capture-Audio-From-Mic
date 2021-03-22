#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

# from StatusJsonPythonModule import StatusJsonRest
from datetime import datetime
import os
import sys
import wave
import pyaudio
import time
from threading import (Event, Thread)

from aion.logger import lprint
from .mysql import MysqlManager

OUTPUT_DIR = "/var/lib/aion/Data/capture-audio-from-mic_1"


class CaptureAudioFromMic():
    # sampling_rate = 44100
    # sampling_rate = 48000
    # sampling_rate = 32000
    fmt = pyaudio.paInt16

    def __init__(self, device_index, sampling_rate=44100,
                 chunk=8192, ch=1, rec_time=60):
        lprint(">>> Initialized Audio Device")
        self.device_index = device_index
        self.sampling_rate = sampling_rate
        self.chunk = chunk
        self.ch = 1
        self.rec_time = rec_time
        self.audio = pyaudio.PyAudio()
        self.frame = []
        self.event = Event()
        self.is_stream_open = False
        self.recording = False

        if self.audio.get_device_count() - 1 < device_index:
            lprint(self.audio.get_device_count(), device_index)
            lprint(">>> Error: this device is not exist")
            sys.exit(1)
        audio_info = self.audio.get_device_info_by_index(device_index)
        lprint(audio_info)

        self.outputPath = OUTPUT_DIR
        os.makedirs(self.outputPath, exist_ok=True)

    def output_wave_file(self):
        lprint(">>> start opening stream")
        self.stream = self.audio.open(
            format=self.fmt, channels=self.ch, rate=self.sampling_rate,
            input=True, input_device_index=self.device_index,
            frames_per_buffer=self.chunk)
        lprint(">>> finish opening stream")

        frames = []
        audio_range = int(self.sampling_rate / self.chunk * self.rec_time)
        for i in range(0, audio_range):
            data = self.stream.read(self.chunk)
            frames.append(data)

        now_time = datetime.now().strftime("%Y%m%d%H%M%S") + "000"
        outputFileName = now_time + ".wav"
        outputFilePath = os.path.join(self.outputPath, outputFileName)

        with wave.open(outputFilePath, 'wb') as wav:
            wav.setnchannels(self.ch)
            # ビット数
            wav.setsampwidth(self.audio.get_sample_size(self.fmt))
            # サンプリング周波数
            wav.setframerate(self.sampling_rate)
            wav.writeframes(b''.join(frames))

        self.stream.stop_stream()
        self.stream.close()

        return outputFilePath

    def open_stream(self):
        self.stream = self.audio.open(
            format=self.fmt, channels=self.ch, rate=self.sampling_rate,
            input=True, input_device_index=self.device_index,
            frames_per_buffer=self.chunk, stream_callback=self.callback)

    def callback(self, in_data, frame_count, time_info, status):
        if self.recording is True:
            self.frame.append(in_data)
            return in_data, pyaudio.paContinue
        elif self.recording is False:
            return None, pyaudio.paContinue
        else:
            return None, pyaudio.paContinue

    def start_recoding(self):
        # initialize frame
        # self.frame = []
        # self.stream.start_stream()
        # self.event.clear()
        # lprint("recording...")
        # while not self.event.wait(timeout=0):
        #     data = self.stream.read(self.chunk)
        #     self.frame.append(data)
        self.recording = True
        self.stream.start_stream()
        lprint("record start")

    def complete_recording(self, activity_id):
        lprint("stop recording....")
        # 複数マイク間の同期を取るために、録音停止信号受信から5秒間のバッファを持たせる
        time.sleep(5)
        self.recording = False
        self.stream.stop_stream()
        output_file_name = str(activity_id) + "_" + str(self.device_index) + ".wav"
        output_file_path = os.path.join(self.outputPath, output_file_name)
        with wave.open(output_file_path, 'wb') as wav:
            wav.setnchannels(self.ch)
            # ビット数
            wav.setsampwidth(self.audio.get_sample_size(self.fmt))
            # サンプリング周波数
            wav.setframerate(self.sampling_rate)
            wav.writeframes(b''.join(self.frame))
        lprint("recording complete.record file output to ", output_file_path)
        return self.audio.get_sample_size(self.fmt), self.sampling_rate, output_file_path


def main():
    # read status json file
    argv = sys.argv
    if len(argv) != 2:
        device_index = 24
    else:
        device_index = int(argv[1])

    captureObj = CaptureAudioFromMic(device_index)

    print(">>> start audio recording")
    while True:
        outputFilePath = captureObj.output_wave_file()

        print("> Success: output audio (path: {})".format(outputFilePath))


if __name__ == "__main__":
    main()
