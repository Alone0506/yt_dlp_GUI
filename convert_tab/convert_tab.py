from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QResizeEvent, QIntValidator

from mainwindow_ui import Ui_MainWindow
from .processer import VideoProcesser


class ConvertTab:
    def __init__(self, main_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_ui
        self.video_processer = VideoProcesser()
        self.before = QPixmap()
        self.after = QPixmap()
        self.ui.width_lineedit.setValidator(QIntValidator())
        self.ui.height_lineedit.setValidator(QIntValidator())
        
    def choose_file(self):
        video_path, _ = QFileDialog.getOpenFileName(caption="Open file")
        if video_path == "":
            return
        support_exts = [self.ui.convert_ext_combobox.itemText(i) for i in range(self.ui.convert_ext_combobox.count())]
        if Path(video_path).suffix.lstrip('.') not in support_exts:
            QMessageBox.critical(None, 'EXTENSION ERROR', 'This file is not supported.')
            return
        self.__set_convert_tab(video_path)
        
    def __set_convert_tab(self, video_path: str) -> None:
        self.ui.video_path_lineedit.setText(str(Path(video_path)))
        self.ui.video_save_as_lineedit.setText(str(Path(video_path).parent))
        self.__reset_step2_groupbox()
        self.video_processer = VideoProcesser()
        self.before = self.video_processer.get_preview(str(Path(video_path)))
        self.__set_before_img(self.before)
        self.__set_placeholder(self.before)
        self.__set_after_img(self.before)
        self.ui.convert_step2_gb.setEnabled(True)
        self.ui.convert_step3_gb.setEnabled(True)
        
    def __reset_step2_groupbox(self):
        self.ui.width_lineedit.clear()
        self.ui.height_lineedit.clear()
        self.ui.vertical_checkbox.setChecked(False)
        self.ui.horizontal_checkbox.setChecked(False)
        self.ui.convert_ext_combobox.setCurrentIndex(0)
        # before_lbl, before_size_lbl, after_lbl, after_size_lbl, are not to
        # clear, because they will be filled in with new values ​​soon.
        
    def __set_before_img(self, before: QPixmap):
        self.ui.before_size_lbl.setText(f'Before: {before.width()} x {before.height()}')
        pixmap = before.scaled(self.ui.before_lbl.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.before_lbl.setPixmap(pixmap)
        
    def __set_placeholder(self, before: QPixmap):
        self.ui.width_lineedit.setPlaceholderText(str(before.width()))
        self.ui.height_lineedit.setPlaceholderText(str(before.height()))
        
    def __set_after_img(self, after: QPixmap):
        self.after = after
        self.ui.after_size_lbl.setText(f'After: {after.width()} x {after.height()}')
        pixmap = after.scaled(self.ui.after_lbl.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.after_lbl.setPixmap(pixmap)
        
    def resize(self) -> None:
        width = self.ui.width_lineedit.text()
        width = self.ui.width_lineedit.placeholderText() if width == '' else width
        height = self.ui.height_lineedit.text()
        height = self.ui.height_lineedit.placeholderText() if height == '' else height
        self.video_processer.resize(int(width), int(height))
        self.__set_after_img(self.video_processer.get_after_pixmap())
        
    def flip(self) -> None:
        is_x_flip = self.ui.vertical_checkbox.isChecked()
        is_y_flip = self.ui.horizontal_checkbox.isChecked()
        self.video_processer.flip(is_x_flip, is_y_flip)
        self.__set_after_img(self.video_processer.get_after_pixmap())
        
    def rotate(self, angle: int) -> None:
        self.video_processer.rotate(angle)
        self.__set_after_img(self.video_processer.get_after_pixmap())
        
    def save_as(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(caption="Save as...")
        if folder_path != "":
            self.ui.video_save_as_lineedit.setText(str(Path(folder_path)))
        
    def convert(self):
        output_path = self.ui.video_save_as_lineedit.text()
        file_name = Path(self.ui.video_path_lineedit.text()).stem
        ext = self.ui.convert_ext_combobox.currentText()
        full_path = str(Path(output_path) / (file_name + f'.{ext}'))
        self.video_processer.convert(full_path)

    def resize_preview(self, event: QResizeEvent):
        def resize(pixmap: QPixmap, lbl: QLabel):
            if pixmap.isNull():
                return
            new_pixmap = pixmap.scaled(lbl.width() - 5, lbl.height() - 5, aspectRatioMode=Qt.KeepAspectRatio)
            lbl.setPixmap(new_pixmap)    
        resize(self.before, self.ui.before_lbl)
        resize(self.after, self.ui.after_lbl)