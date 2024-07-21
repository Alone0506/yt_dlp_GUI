# Video Downloader

<p align="center">

<img src="https://img.shields.io/badge/made%20by-Alone-blue.svg" >

<img src="https://img.shields.io/badge/python-3.11.9-green.svg">
  
<img src="https://img.shields.io/badge/license-GPL3.0-green.svg">
 
<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" >

</p>

![image](https://github.com/user-attachments/assets/6da709e7-0c95-41a3-9fa5-38bb2322fdf9)
- 支援 Youttube, Twitch, CNN, Bilibili...等各大網站, 詳細網站: [Supported sites](https://github.com/yt-dlp/yt-dlp/blob/2024.07.16/supportedsites.md).
- 支援解析度無上限, 720p, 1080p, 2k, 4k, 8k...等都可以.
- 會自動幫你選擇最優質的Video & Audio 格式, 直接無腦下載!
- 支援下載時自動轉換成mp4, m4v, mkv, webm, avi...等常見的格式
- 也可自行根據fps, resolution, filesize, protocol, vcodec, acodec等下載自己需要的格式.
![image](https://github.com/user-attachments/assets/9e24ff40-d984-43e8-a48a-0c21957c58c2)

---
- 如果想下載CC字幕也可以一併下載, 原生字幕或機翻字幕都可以.
- 支援等json3, srv1, srv2, srv3, ttml, vtt等常見字幕格式, 並且可一次選擇多種字幕下載.
![image](https://github.com/user-attachments/assets/a718e73d-991e-4c9d-b076-1522322a300c)

---

- 如果想要更改影片格式或進行簡單的編輯, 也有提供Resize, Flip, Rotate, Change Extension等功能.
- 影片編輯時也提供預覽圖可以預覽.
![image](https://hackmd.io/_uploads/BkntCSqOA.png)

## Download
可以在[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Alone/video_downloader)](https://github.com/Alone/video_downloader/releases/latest)下載預先編譯好的版本.

解壓縮後檔案結構:
```tex
|-video_downloader
|    |_ _internal
|       ffmpeg
|       video_downloader.exe
|
```
執行`video_downloader.exe`即可.

## Usage
#### Download Video
1. 執行video_downloader.exe
2. 在step1的地方貼上網址後按下"Get Information"按鈕
3. (可選)想下載影片的話就按下"Choose Video Source"按鈕, 選完後你的選擇的ID會出現在下方, 不選擇的話預設會是最佳的畫質/音質.
4. (可選)想下載字幕的話就按下"Choose Subtitles"按鈕選擇想要的字幕, 選完後結果會出現在下方.
5. 選擇存放位置與格式後點擊"下載"即可

***有些影片受限於編碼模式, 無法及時轉換成指定的格式, 請下載後到Convert頁面轉換格式**

#### Convert Video
1. 執行video_downloader.exe
2. 選擇影片檔案, 副檔名支援mp4, m4v, mkv, webm, avi, mov, wmv, flv, asf, avchd, vob共11種格式.
3. (可選) 選擇Resize, Flip或Rotate來編輯影片, 對比圖會顯示於下方
4. 選擇檔案格式
5. 選擇存放位置後點擊"Convert"按鈕即可.

## Q&A
▶ 出現 `Could not find QtWebEngineProcess.exe`錯誤: 確保exe上的路徑皆為英文.
▶ 出現 `ERROR: Postprocessing: Conversion failed!`: 因影片的編碼格式不支援, 所以無法在合併聲音與影像時轉檔, 可以嘗試先以mp4或webm格式下載後再到Convert頁面轉檔.

## Issue
如果有遇到問題可以到[Issue](https://github.com/Alone0506/video_downloader/issues)提出問題.
