# FROM latonaio/pylib-lite:latest
FROM latonaio/l4t:latest

ENV POSITION=Runtime \
    SERVICE=capture-audio-from-mic \
    AION_HOME="/var/lib/aion" \
    SOURCE="pa_stable_v190600_20161030.tgz"

# Setup Directoties
RUN mkdir ${AION_HOME}
RUN mkdir -p ${AION_HOME}/$POSITION/$SERVICE
RUN mkdir -p ${AION_HOME}/Data/${SERVICE}_1
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/

RUN apt update && apt-get install -y wget tar usbutils
RUN apt update && apt-get install -y alsa alsa-oss
RUN apt update && apt-get install -y libasound2-dev portaudio19-dev python3-pyaudio python-pyaudio
    # wget http://www.portaudio.com/archives/${SOURCE} && \
    # tar xvf ${SOURCE} && cd portaudio && ./configure && make && make install && \
    # rm -rf portaudio ${SOURCE}
ADD . .

RUN cd portaudio && ./configure && make install
RUN pip3 install pyaudio
RUN python3 setup.py install

CMD ["/bin/sh", "docker-entrypoint.sh"]
