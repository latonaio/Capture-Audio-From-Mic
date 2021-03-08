# Capture-Audio-From-Mic
Capture-Audio-From-Micは、音声録音ツールです。docker上での動作を前提としています。
## 概要
Capture-Audio-From-Micは、ホストに接続された録音デバイスを認識し、これから受取ったストリーミング音声データをwavファイルに変換します。

## 起動方法
このリポジトリをクローンし、以下のコマンドよりサービスを起動してください。

```
$ cd /path/to/capture-audio-from-mic
$ bash docker-build.sh
```

## 動作環境
Capture-Audio-From-Micは、kubernetes上での動作を前提としています。
```
OS: Linux
Kubernetes

最低限スペック
CPU: 2 core
memory: 4 GB
```
## Input

## Output