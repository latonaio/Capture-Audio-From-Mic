# Capture-Audio-From-Mic
Capture-Audio-From-Micは、音声録音ツールです。aion-core 上での動作を前提としています。  

## 概要
Capture-Audio-From-Micは、ホストに接続された録音デバイスを認識し、これから受取ったストリーミング音声データをwavファイルに変換します。  
`PyAudio`および`portaudio`が入っています。PyAudioは、`requirements.txt` にダウンロードするべきバージョンが記載されています。
  
## 起動方法
このリポジトリをクローンし、以下のコマンドよりサービスを起動してください。

```
$ cd ~/path/to/capture-audio-from-mic
$ bash docker-build.sh
```
  
## 動作環境
Capture-Audio-From-Micは、aion-core 上での動作を前提としており、下記動作環境が必要となります。
  
-　ARM CPU搭載のデバイス(NVIDIA Jetson シリーズ等)  
-　OS: Linux Ubuntu OS  
-　CPU: ARM64  
-　Kubernetes  
-　AION のリソース  
  
  
最低限スペック  
- CPU: 2 core  
- memory: 4 GB  

## Input  
 USBで接続されたUSBマイク  
 1pod につき1台のマイクが接続可能です。  
 理論上は、podの数だけ増やすことができます。
  
## Output  
 - wavファイル
 - Kanban  
コンテナ上でのwavファイルの出力先は
`/var/lib/aion/Data/capture-audio-from-mic_1` です。  
k8sへのデプロイ時にこのパスに対応したマウントディレクトリを指定する必要があります。  

### サンプリングレート  
　 固定値でデフォルト `32000`  
   ソースの中に書き込むことができます。

### 録音時間
　 固定値でデフォルト`60秒`  
   ソースの中に書き込むことができます。
  