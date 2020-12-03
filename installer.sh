#!/bin/bash

# if in arm, pip install cant exec.
wget http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar xvf pa_stable_v190600_20161030.tgz
cd portaudio
./configure
make -j8
sudo make install
sudo pip3 install pyaudio
rm -r portaudio pa_stable_v190600_20161030.tgz

