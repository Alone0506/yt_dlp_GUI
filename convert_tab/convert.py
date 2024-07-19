import os

from PyQt5.QtGui import QPixmap, QImage
from moviepy.editor import VideoFileClip, vfx


class Video:
    def __init__(self):
        self.video_path = ''
        self.origin_clip: VideoFileClip = None
        self.clip: VideoFileClip = None
        self.width = 0
        self.height = 0
        self.is_x_flip = False
        self.is_y_flip = False
        self.rotate_angle = 0
    
    def init(self, video_path: str) -> QPixmap:
        self.video_path = video_path
        video = VideoFileClip(video_path)
        mid_time= video.duration / 2
        video = video.subclip(mid_time, mid_time + 1 / video.fps)
        self.origin_clip = video.copy()
        self.clip = video.copy()
        video.close()
        
        self.width = self.clip.w
        self.height = self.clip.h
        before_pixmap = self._clip2QPixmap()
        return before_pixmap
    
    def _clip2QPixmap(self):
        img = self.clip.get_frame(0)
        height, width, channel = img.shape
        bytes_per_line = channel * width
        qimage = QImage(img.data.tobytes(), width, height, bytes_per_line, QImage.Format_BGR888).rgbSwapped()
        return QPixmap().fromImage(qimage)
    
    def get_after_pixmap(self) -> QPixmap:
        after_pixmap = self._clip2QPixmap()
        return after_pixmap
        
    def resize(self, width, height) -> QPixmap:
        self.width = width
        self.height = height
        self.clip = self.pre_process(self.origin_clip)
        
    def flip(self, is_x_flip: bool, is_y_flip: bool) -> QPixmap:
        if is_x_flip != self.is_x_flip:
            self.clip = self.clip.fx(vfx.mirror_x)
            self.is_x_flip = is_x_flip
            
        if is_y_flip != self.is_y_flip:
            self.clip = self.clip.fx(vfx.mirror_y)
            self.is_y_flip = is_y_flip
            
    def rotate(self, angle: int) -> QPixmap:
        self.rotate_angle = (self.rotate_angle + angle) % 360
        if self.rotate_angle != 0:
            self.clip = self.clip.rotate(angle)
        
    @staticmethod
    def _get_codec_and_audio_codec(output_ext: str) -> tuple[str, str]:
        ext = output_ext.lower()
        if ext in ['mp4', 'm4v']:
            return 'libx264', 'aac'
        elif ext == 'mkv':
            return 'libx264', 'aac'  # or 'libvorbis'        
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
        elif ext == 'avchd':
            return 'libx264', 'aac'
        elif ext == 'vob':
            return 'mpeg2video', 'mp2'
        else:
            return None, None
        
    def pre_process(self, video: VideoFileClip) -> VideoFileClip:
        clip = video.copy()
        if video.w != self.width or video.h != self.height:
            clip = clip.resize((self.width, self.height))
        if self.is_x_flip:
            clip = clip.fx(vfx.mirror_x)
        if self.is_y_flip:
            clip = clip.fx(vfx.mirror_y)
        if self.rotate_angle != 0:
            clip = clip.rotate(self.rotate_angle)
        return clip
        
    def convert(self, output_path: str, output_ext: str) -> None:
        video = VideoFileClip(self.video_path)
        video = self.pre_process(video)
        num_threads = os.cpu_count()
        vcodec, acodec = self._get_codec_and_audio_codec(output_ext)
        video.write_videofile(output_path, codec=vcodec, audio_codec=acodec, threads=num_threads)