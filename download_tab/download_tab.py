from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
import markdown
from pathlib import Path

from .downloader import Downloader
from mainwindow_ui import Ui_MainWindow
from .video_subwindow.video_controller import VideoSubWindow
from .subtitle_subwindow.subtitle_controller import SubtitleSubWindow


class DownloadTab:
    def __init__(self, main_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_ui
        self.pixmap = QPixmap()
        self.downloader = Downloader()
        self.subtitles_choose: dict[str, list[str]] = dict()
        self.video_subwindow = VideoSubWindow()
        self.subtitle_subwindow = SubtitleSubWindow()
        self.setup_tab()
        
    def setup_tab(self):
        self.ui.path_lineedit.setText(str(Path(__file__).parent.absolute()))
        
        self.downloader.info_thread.finished.connect(self.info_thread_finished)
        self.downloader.video_thread.finished.connect(self.video_thread_finished)
        self.downloader.subtitle_thread.progress.connect(self.subtitle_thread_progress)
        self.downloader.subtitle_thread.finished.connect(self.subtitle_thread_finished)
        self.video_subwindow.data_sent.connect(self.show_video_audio_src)
        self.subtitle_subwindow.data_sent.connect(self.show_subtitle_lang_format)
    
    def show_supported_sites(self):
        with open('download_tab/supportedsites.md', 'r', encoding='utf-8') as f:
            markdown_data = f.read()
        html_data = markdown.markdown(markdown_data)  # Convert markdown to HTML
        dialog = MarkdownViewerDialog(html_data)  # Create and show the MarkdownViewerDialog
        dialog.exec_()
    
    def get_info(self):
        url = self.ui.url_lineedit.text()
        self.downloader.info_thread.download(url)
        
    def save_as(self):
        folder_path = QFileDialog.getExistingDirectory(caption="Save as...")
        if folder_path != "":
            self.ui.path_lineedit.setText(folder_path)
            
    def choose_video(self):
        self.video_subwindow.show()
        
    def choose_subtitle(self):
        self.subtitle_subwindow.show()
        
    def download(self):
        url = self.ui.url_lineedit.text()
        path = self.ui.path_lineedit.text()
        video_format = self.ui.format_lbl.text()
        self.downloader.video_thread.download(url, path, video_format)
        
    def resize_thumbnail(self, event: QResizeEvent):
        if self.pixmap.isNull():
            return
        # Need some space to allow thumbnail to shrink.
        lbl_width = self.ui.thumbnail_lbl.width()
        lbl_height = self.ui.thumbnail_lbl.height()
        new_pixmap = self.pixmap.scaled(lbl_width - 5, lbl_height - 5, aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.thumbnail_lbl.setPixmap(new_pixmap)
        
        
    def info_thread_finished(self, info: dict[str, str | int | None]) -> None:
        if info == {}:
            QMessageBox.critical(None, 'URL ERROR', 'Please check the error message in terminal and try again.')
            return
        
        def get_format_infos(formats: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
            video_audio_srcs: list[dict[str, str]] = []
            video_srcs: list[dict[str, str]] = []
            audio_srcs: list[dict[str, str]] = []
            
            for format in formats:
                vcodec = format.get('vcodec', 'none')
                acodec = format.get('acodec', 'none')
                if vcodec != 'none' and acodec != 'none':
                    video_audio_srcs.append(format)
                elif vcodec != 'none':
                    video_srcs.append(format)
                elif acodec != 'none':
                    audio_srcs.append(format)
            return video_audio_srcs, video_srcs, audio_srcs
        
        video_audio_srcs, video_srcs, audio_srcs = get_format_infos(info.get('formats', []))
        # setting mainwindow
        try:
            res = requests.get(info['thumbnail'])
            img = QImage.fromData(res.content)
        except:
            img = QImage.fromData(b"")
        self.pixmap = QPixmap.fromImage(img)
        self.resize_thumbnail(None)
        self.ui.video_title_lbl.setText(info['title'])
        self.ui.video_author_lbl.setText(info['uploader_id'])
        self.ui.video_length_lbl.setText(info['duration_string'])
        
        # setting subwindows
        best_formats = info['format_id']
        self.video_subwindow.setting_tables(video_audio_srcs, video_srcs, audio_srcs, best_formats)
        self.subtitle_subwindow.setting_tables(info.get('subtitles', {}), info.get('automatic_captions', {}))
        
    def show_video_audio_src(self, video_audio_src: str):
        self.ui.format_lbl.setText(video_audio_src)
            
    def show_subtitle_lang_format(self, subtitles_choose: dict[str, list[str]], auto_subtitles_choose: dict[str, list[str]]):
        def get_choose_str(choose_datas: dict[str, list[str]]) -> str:
            choose_str = ''
            for lang, formats in choose_datas.items():
                choose_str += f'{lang}: '
                choose_str += ', '.join(i for i in formats)
            return choose_str
        self.ui.subtitle_lineedit.setText(get_choose_str(subtitles_choose))
        self.ui.auto_subtitle_lineedit.setText(get_choose_str(auto_subtitles_choose))
        
        # merge subtitles_choose & auto_subtitles_choose
        self.subtitles_choose = auto_subtitles_choose.copy()
        self.subtitles_choose.update(subtitles_choose)
        
    def video_thread_finished(self, is_success: bool) -> None:
        if is_success:
            print('Download video success.\n')
        else:
            QMessageBox.critical(None, 'ERR', 'Please check the error message in terminal and try again.')
            print('Download video fail.\n')
        url = self.ui.url_lineedit.text()
        path = self.ui.path_lineedit.text()
        self.downloader.subtitle_thread.download(url, path, self.subtitles_choose)
        
    def subtitle_thread_progress(self, is_success: bool, lang: str, format: str) -> None:
        if is_success:
            print(f'Downlaod language: {lang}, format: {format} success.\n')
        else:
            print(f'Downlaod language: {lang}, format: {format} error.\n')
        
    def subtitle_thread_finished(self) -> None:
        print('Download all subtitle success.')
        print("Download finished.")
        

class MarkdownViewerDialog(QDialog):
    def __init__(self, html_data):
        super().__init__()
        self.setWindowTitle("Supported sites")
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.web_view = QWebEngineView()
        self.web_view.setHtml(html_data)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.search_text)

        self.search_label = QLabel("")

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.web_view)
        layout.addWidget(self.search_label)
        self.setLayout(layout)

    def search_text(self):
        search_string = self.search_bar.text()
        self.web_view.findText(search_string)
        self.search_label.setText(f"Searching for: {search_string}")