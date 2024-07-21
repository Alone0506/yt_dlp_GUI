Video Downloader
<p align="center">
<img src="https://img.shields.io/badge/made%20by-Alone-blue.svg">
<img src="https://img.shields.io/badge/python-3.11.9-green.svg">
<img src="https://img.shields.io/badge/license-GPL3.0-green.svg">
<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" >
</p>

- [English](./readme.md) | [中文](./readme_zh_TW.md)

![image](https://github.com/user-attachments/assets/6da709e7-0c95-41a3-9fa5-38bb2322fdf9)
- Supports major websites like YouTube, Twitch, CNN, Bilibili, etc. For detailed sites: [Supported sites](https://github.com/yt-dlp/yt-dlp/blob/2024.07.16/supportedsites.md).
- Supports unlimited resolution, including 720p, 1080p, 2k, 4k, 8k, etc.
- Automatically selects the best Video & Audio format for you, just download without any hassle!
- Supports automatic conversion to common formats such as mp4, m4v, mkv, webm, avi, etc. during download.
- You can also manually download the format you need based on fps, resolution, filesize, protocol, vcodec, acodec, etc.
![image](https://github.com/user-attachments/assets/9e24ff40-d984-43e8-a48a-0c21957c58c2)

---

- If you want to download CC subtitles, you can download them together, including native or machine-translated subtitles.
- Supports common subtitle formats such as json3, srv1, srv2, srv3, ttml, vtt, and allows multiple subtitle downloads at once.
![image](https://github.com/user-attachments/assets/a718e73d-991e-4c9d-b076-1522322a300c)

---

- If you want to change the video format or perform simple editing, we provide Resize, Flip, Rotate, Change Extension functions.
- Preview images are also available during video editing.
![image](https://github.com/user-attachments/assets/782d08f7-acb0-4155-ab7f-d1159e00d319)

## Download
You can download the pre-compiled version from [![GitHub release (latest by date)](https://img.shields.io/github/v/release/Alone/video_downloader)](https://github.com/Alone/video_downloader/releases/latest).

After extracting the files, the directory structure is as follows:
```tex
|-video_downloader
|    |_ _internal
|       ffmpeg
|       video_downloader.exe
|
```
Run `video_downloader.exe`.

## Usage
#### Download Video
1. Run video_downloader.exe
2. Paste the URL in step 1 and click the Get Information button
3. (Optional) To download the video, click the `Choose Video Source` button. After selecting, the chosen ID will appear below. If not selected, the default will be the best quality/audio.
4. (Optional) To download subtitles, click the `Choose Subtitles` button and select the desired subtitles. The results will appear below after selection.
5. Choose the save location and format, then click `Download`.

***Some videos, due to encoding restrictions, cannot be converted to the specified format immediately. Please download them first and then convert the format on the Convert page.**

#### Convert Video
1. Run `video_downloader.exe`.
2. Choose the video file. Supported extensions are `mp4`, `m4v`, `mkv`, `webm`, `avi`, `mov`, `wmv`, `flv`, `asf`, `avchd`(11 formats in total).
3. (Optional) Choose Resize, Flip, or Rotate to edit the video. The comparison image will be displayed below.
4. Choose the file format.
5. Choose the save location and click the `Convert` button.

## Compile
▶ You need to download ffmpeg and place it in the same directory as main.py. In the release, download ffmpeg as follows: [Inatall FFmpeg (windows)](https://hackmd.io/@Alone0506/rJp3USqm0).

## Q&A
▶ Error `Could not find QtWebEngineProcess.exe`: Ensure that all paths on the exe are in English.
▶ Error `ERROR: Postprocessing: Conversion failed!`: Due to unsupported video encoding format, the file cannot be converted while merging audio and video. Try downloading in `mp4` or `webm` format first, then convert on the Convert page.

## Issue
If you encounter any problems, you can raise an issue at [Issue](https://github.com/Alone0506/video_downloader/issues).