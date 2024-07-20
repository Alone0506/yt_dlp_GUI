import os
from pathlib import Path

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QProcess
from moviepy.editor import VideoFileClip, vfx

class VideoProcesser:
    def __init__(self):
        self.video_path = ''
        self.origin_clip: VideoFileClip = None
        self.clip: VideoFileClip = None
        self.width = 0
        self.height = 0
        self.is_x_flip = False
        self.is_y_flip = False
        self.rotate_angle = 0
        
        self.convert_process = QProcess()
        self.convert_process.readyReadStandardOutput.connect(self.process_output)
        self.convert_process.readyReadStandardError.connect(self.process_err)
        self.convert_process.finished.connect(self.process_finished)
    
    def get_preview(self, video_path: str) -> QPixmap:
        self.video_path = video_path
        video = VideoFileClip(video_path)
        mid_time= video.duration / 2
        video = video.subclip(mid_time, mid_time + 1 / video.fps)
        self.origin_clip = video.copy()
        self.clip = video.copy()
        video.close()
        
        self.width = self.clip.w
        self.height = self.clip.h
        before_pixmap = self.__clip2QPixmap()
        return before_pixmap
    
    def __clip2QPixmap(self) -> QPixmap | None:
        img = self.clip.get_frame(0)
        height, width, channel = img.shape
        bytes_per_line = channel * width
        qimage = QImage(img.data.tobytes(), width, height, bytes_per_line, QImage.Format_BGR888).rgbSwapped()
        return QPixmap().fromImage(qimage)
    
    def get_after_pixmap(self) -> QPixmap:
        after_pixmap = self.__clip2QPixmap()
        return after_pixmap
        
    def resize(self, width, height) -> None:
        self.clip = self.origin_clip.copy()
        self.width = width
        self.height = height
        if self.clip.w != self.width or self.clip.h != self.height:
            self.clip = self.clip.resize((self.width, self.height))
        if self.is_x_flip:
            self.clip = self.clip.fx(vfx.mirror_x)
        if self.is_y_flip:
            self.clip = self.clip.fx(vfx.mirror_y)
        if self.rotate_angle != 0:
            self.clip = self.clip.rotate(self.rotate_angle)
        
    def flip(self, is_x_flip: bool, is_y_flip: bool) -> None:
        if is_x_flip != self.is_x_flip:
            self.clip = self.clip.fx(vfx.mirror_x)
            self.is_x_flip = is_x_flip
            
        if is_y_flip != self.is_y_flip:
            self.clip = self.clip.fx(vfx.mirror_y)
            self.is_y_flip = is_y_flip
            
    def rotate(self, angle: int) -> None:
        self.rotate_angle = (self.rotate_angle + angle) % 360
        self.clip = self.clip.rotate(angle)
        
    def convert(self, output_path: str) -> None:
        cmd = ['-i', self.video_path]
        if self.clip.w != self.width or self.clip.h != self.width:
            cmd.extend(['-vf', f'scale={self.width}:{self.height}'])
        
        if self.is_x_flip:
            cmd.extend(['-vf', 'vflip'])
        if self.is_y_flip:
            cmd.extend(['-vf', 'hflip'])
            
        trans_dict = {90: 'transpose=1', 180: 'transpose=2,transpose=2', 270: 'transpose=2'}
        if self.rotate_angle in trans_dict:
            cmd.extend(['-vf', trans_dict[self.rotate_angle]])
        
        cmd.extend(['-threads', str(os.cpu_count()), output_path])
        ffmpeg_path = str(Path.cwd() / 'ffmpeg' / 'bin' / 'ffmpeg.exe')
        self.convert_process.start(ffmpeg_path, cmd)
        
    def process_output(self):
        print(self.convert_process.readAllStandardOutput().data().decode(), end='')
        
    def process_err(self):
        print(self.convert_process.readAllStandardError().data().decode(), end='')
        
    def process_finished(self):
        print("Convert Finished.")