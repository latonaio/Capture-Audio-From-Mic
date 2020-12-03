#!/usr/bin/env python3

import pyaudio
p = pyaudio.PyAudio()

for index in range(0, p.get_device_count()):
    print(p. get_device_info_by_index(index))
