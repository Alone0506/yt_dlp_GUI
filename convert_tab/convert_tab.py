import os
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QIntValidator
from moviepy.editor import VideoFileClip, vfx

from mainwindow_ui import Ui_MainWindow


class ConvertTab:
    def __init__(self, main_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_ui
        self.setup_tab()
        self.img_processing = ImgProcesser()
        self.before_img = QPixmap()
        
    def setup_tab(self):
        self.ui.width_lineedit.setValidator(QIntValidator())
        self.ui.height_lineedit.setValidator(QIntValidator())
        self.ui.angle_lineedit.setValidator(QIntValidator())
        
    def choose_file(self):
        # TODO: except handle
        video_path, _ = QFileDialog.getOpenFileName(caption="Open file")
        if video_path == "":
            return
        self.ui.video_path_lineedit.setText(str(Path(video_path)))
        self.ui.video_save_as_lineedit.setText(str(Path(video_path).parent))
        self.set_before_img()
        self.set_placeholder()
        self.set_after_img()
        
    def set_before_img(self):
        """
        Select the frame in the middle of the video as the preview image.
        """
        video = VideoFileClip(self.ui.video_path_lineedit.text())
        middle_time = video.duration / 2
        middle_img = video.get_frame(middle_time)
        video.close()
        
        # transfer numpy array to QImage
        height, width, channel = middle_img.shape
        bytes_per_line = channel * width
        qimage = QImage(middle_img.data, width, height, bytes_per_line, QImage.Format_BGR888).rgbSwapped()
        
        self.before_img = QPixmap().fromImage(qimage)
        self.ui.before_size_lbl.setText(f'{self.before_img.width()} x {self.before_img.height()}')
        pixmap = self.before_img.scaled(self.ui.before_lbl.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.before_lbl.setPixmap(pixmap)
        
    def set_placeholder(self):
        self.ui.width_lineedit.setPlaceholderText(str(self.before_img.width()))
        self.ui.height_lineedit.setPlaceholderText(str(self.before_img.height()))
        self.ui.angle_lineedit.setPlaceholderText('0')
        
    def new_video_size(self) -> tuple[int, int]:
        width = self.ui.width_lineedit.text()
        width = self.ui.width_lineedit.placeholderText() if width == '' else width
        height = self.ui.height_lineedit.text()
        height = self.ui.height_lineedit.placeholderText() if height == '' else height
        return int(width), int(height)
        
    def new_video_flip_dir(self) -> tuple[bool, bool]:
        # TODO: 看能不用moviepy取代
        is_vertical_flip = self.ui.vertical_checkbox.isChecked()
        is_horizontal_flip = self.ui.horizontal_checkbox.isChecked()
        return is_vertical_flip, is_horizontal_flip
    
    def new_video_rotate_angle(self) -> int:
        angle = self.ui.angle_lineedit.text()
        angle = self.ui.angle_lineedit.placeholderText() if angle == '' else angle
        return int(angle)
        
    def set_after_img(self):
        pixmap = self.before_img
        
        # resize
        width, height = self.new_video_size()
        pixmap = self.img_processing.resize(pixmap, width, height)
        
        # flip
        is_vertical_flip, is_horizontal_flip = self.new_video_flip_dir()
        pixmap = self.img_processing.flip(pixmap, is_vertical_flip, is_horizontal_flip)
        
        # rotate
        angle = self.new_video_rotate_angle()
        pixmap = self.img_processing.rotate(pixmap, angle)
        
        self.ui.after_size_lbl.setText(f'{pixmap.width()} x {pixmap.height()}')
        pixmap = pixmap.scaled(self.ui.after_lbl.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.after_lbl.setPixmap(pixmap)
        
    def convert(self):
        video = VideoFileClip(self.ui.video_path_lineedit.text())
        video_processer = VideoProcesser()
        
        # # resize
        # width, height = self.new_video_size()
        # video = video_processer.resize(width, height)
        
        # # flip
        # is_vertical_flip, is_horizontal_flip = self.new_video_flip_dir()
        # video = video_processer.flip(video, is_vertical_flip, is_horizontal_flip)
        
        # # rotate
        # angle = self.new_video_rotate_angle()
        # video = video_processer.rotate(angle)
        
        # convert
        output_path = self.ui.video_save_as_lineedit.text()
        file_name = Path(self.ui.video_path_lineedit.text()).stem
        ext = self.ui.ext_combobox.currentText()
        full_path = str(Path(output_path) / (file_name + f'.{ext}'))
        video_processer.convert(video, full_path, ext)
        print('convert video success.')
        
    
class VideoProcesser:
    # TODO: run in qthread
    def __init__(self):
        return
    @staticmethod
    def resize(video: VideoFileClip, width: int, height: int):
        if video.w == width and video.h == height:
            return video
        video = video.resize((width, height))  # need opencv-python
        return video
    
    @staticmethod
    def flip(video: VideoFileClip, is_vertical_flip: bool, is_horizontal_flip: bool):
        if is_vertical_flip == False and is_horizontal_flip == False:
            return video
        if is_vertical_flip:
            video = video.fx(vfx.mirror_x)
        if is_horizontal_flip:
            video = video.fx(vfx.mirror_y)
        return video
    
    @staticmethod
    def rotate(video: VideoFileClip, angle: int):
        if angle % 360 == 0:
            return video
        video = video.rotate(90)
        return video
    
    @staticmethod
    def _get_codec_and_audio_codec(output_ext: str) -> tuple[str, str]:
        ext = output_ext.lower()
        if ext in ['mp4', 'm4v']:
            return 'libx264', 'aac'
        elif ext == 'webm':
            return 'libvpx', 'libvorbis'
        elif ext == 'avi':
            return 'libxvid', 'mp3'
        elif ext == 'mov':
            return 'libx264', 'aac'
        elif ext == 'wmv':
            return 'wmv2', 'wmav2'
        elif ext == 'flv':
            return 'flv', 'libmp3lame'
        elif ext == 'asf':
            return 'wmv2', 'wmav2'
        elif ext == 'mkv':
            return 'libx264', 'aac'  # or 'libvorbis'
        elif ext == 'avchd':
            return 'libx264', 'aac'
        elif ext == 'gif':
            return 'gif', None
        elif ext == 'vob':
            return 'mpeg2video', 'mp2'
        else:
            return None, None
        
    def convert(self, video: VideoFileClip, output_path: str, output_ext: str):
        num_threads = os.cpu_count()
        vcodec, acodec = self._get_codec_and_audio_codec(output_ext)
        if vcodec is None and acodec is None:
            QMessageBox.critical(None, 'ERROR', f'Unsupported file extension: {output_ext}')
            return
        if acodec:
            video.write_videofile(output_path, codec=vcodec, audio_codec=acodec, threads=num_threads)
        else:
            video.write_videofile(output_path, codec=vcodec, threads=num_threads)
    
    
class ImgProcesser:
    # TODO: 用 VideoFileClip 取代
    @staticmethod
    def resize(before: QPixmap, width: int, height: int) -> QPixmap:
        if before.width == width and before.height == height:
            return before
        return before.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
    
    @staticmethod
    def flip(before: QPixmap, is_vertical_flip: bool, is_horizontal_flip: bool) -> QPixmap:
        if is_vertical_flip == False and is_horizontal_flip == False:
            return before
        dx = -1 if is_vertical_flip else 1
        dy = -1 if is_horizontal_flip else 1
        return before.transformed(QTransform().scale(dx, dy))
    
    @staticmethod
    def rotate(before: QPixmap, angle: int) -> QPixmap:
        if angle % 360 == 0:
            return before
        return before.transformed(QTransform().rotate(angle))