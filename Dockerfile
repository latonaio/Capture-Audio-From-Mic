# syntax = docker/dockerfile:experimental
FROM nvcr.io/nvidia/l4t-base:r32.3.1

# Install Dependencies
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
    build-essential \
    make \
    cmake \
    curl \
    git \
    g++ \
    gcc \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgtk-3-dev \
    libssl-dev \
    libgtk-3-dev \
    libcurl4-openssl-dev \
    libgirepository1.0-dev \
    libmysqlclient-dev \
    zlib1g-dev \
    python-pip \
    python3-pip \
    python3-dev \
    tzdata \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# for japanese
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

# Dependencies about mysqlclient
RUN git clone https://github.com/edenhill/librdkafka && \
    cd librdkafka && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd ../ && \
    rm -rf librdkafka

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
RUN git config --global url."git@bitbucket.org:".insteadOf "https://bitbucket.org/"
RUN --mount=type=secret,id=ssh,target=/root/.ssh/id_rsa ssh-keyscan -t rsa bitbucket.org >> /root/.ssh/known_hosts \
  && pip3 install -U git+ssh://git@bitbucket.org/latonaio/AION-related-python-library.git
    # wget http://www.portaudio.com/archives/${SOURCE} && \
    # tar xvf ${SOURCE} && cd portaudio && ./configure && make && make install && \
    # rm -rf portaudio ${SOURCE}
ADD . .

RUN cd portaudio && ./configure && make install
RUN pip3 install pyaudio
RUN python3 setup.py install

CMD ["/bin/sh", "docker-entrypoint.sh"]
