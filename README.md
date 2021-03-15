# Capture-Audio-From-Mic
Capture-Audio-From-Micは、音声録音ツールです。aion-core 上での動作を前提としています。  

## 概要
Capture-Audio-From-Micは、ホストに接続された録音デバイスを認識し、これから受取ったストリーミング音声データをwavファイルに変換します。  
主に使用するモジュール、ライブラリーとして、`PyAudio`および`portaudio`が入っています。PyAudioは、`requirements.txt` にダウンロードするべきバージョンが記載されています。  
Capture-Audio-From-Micには、通常のjobとして実行されるmain_without_kanbanと、pod上で運用することを前提としているmain_with_kanban_multipleが含まれています。

## 録音設定
### main_without_kanban   

| パラメーター名    | 設定値 | 
| :---------------: | :--------------: | 
| sampling_rate(Hz) | 32000            | 
| chunk             | 4096             | 
| rec_time(sec)     | 60               | 

### main_with_kanban_multiple  

| パラメーター名    | 設定値 | 
| :---------------: | :--------------: | 
| sampling_rate(Hz) | 32000            | 
| chunk             | 8192             | 

※ … main_with_kanban_multipleでは、kanbanによって送られる開始信号によって録音が始まり、終了信号によって録音が終了します。

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
main_without_kanbanは、通常のjobとして実行することが可能です。
main_with_kanban_multipleは、kanbanから指示をデータとして受取り、録音を実行します。
### データフォーマット
録音開始: `status:0`  
録音停止: `status:1`
  
## Output  
 - wavファイル
 - output_kanban
コンテナ上では`/var/lib/aion/Data/capture-audio-from-mic_1` へwavファイルが出力されます。  
k8sへのデプロイ時にこのパスに対応したマウントディレクトリを指定する必要があります。  
