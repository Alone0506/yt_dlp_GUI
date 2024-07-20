from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal
# from convert_tab.processer import VideoProcesser
import yt_dlp

class DownloadInfoThread(QThread):
    finished = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
    
    def download(self, url: str):
        self.url = url
        self.start()
    
    def run(self):
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'skip_download': True,
            'ffmpeg_location': str(Path.cwd() / 'ffmpeg' / 'bin' / 'ffmpeg.exe'),
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
            self.finished.emit(info_dict)
        except yt_dlp.utils.DownloadError as e:
            self.finished.emit({})


class DownloadVideoThread(QThread):
    finished = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
    
    def download(self, url: str, output_path: str, video_ids: str, video_ext: str):
        self.url = url
        self.output_path = output_path
        self.video_ids = video_ids
        self.video_ext = video_ext
        self.start()
    
    def run(self):
        if not self.video_ids:
            return
        ydl_opts = {
            'format': self.video_ids,
            "paths": {"home": self.output_path},
            "outtmpl": "%(title)s.%(ext)s",
            'ffmpeg_location': str(Path.cwd() / 'ffmpeg' / 'bin' / 'ffmpeg.exe'),
            'merge_output_format': self.video_ext,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished.emit(True)
        except yt_dlp.utils.DownloadError:
            self.finished.emit(False)


class DownloadSubtitleThread(QThread):
    progress = pyqtSignal(bool, str, str)
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
    
    def download(self, url: str, output_path: str, choose_datas: dict[str, list[str]]):
        self.url = url
        self.output_path = output_path
        self.choose_datas = choose_datas
        self.start()
    
    def run(self):
        if self.choose_datas == {}:
            self.finished.emit()
            return
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [],
            'subtitlesformat': '',
            'skip_download': True,
            "paths": {"home": self.output_path},
            "outtmpl": "%(title)s.%(ext)s",
            'ffmpeg_location': str(Path.cwd() / 'ffmpeg' / 'bin' / 'ffmpeg.exe'),
        }
        for lang, formats in self.choose_datas.items():
            ydl_opts['subtitleslangs'] = [lang]
            for format in formats:
                ydl_opts['subtitlesformat'] = format
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([self.url])
                    self.progress.emit(True, lang, format)
                except yt_dlp.utils.DownloadError:
                    self.progress.emit(False, lang, format)
        self.finished.emit()

class Downloader:
    def __init__(self):
        self.info_thread = DownloadInfoThread()
        self.video_thread = DownloadVideoThread()
        self.subtitle_thread = DownloadSubtitleThread()
