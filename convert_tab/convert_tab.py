from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QResizeEvent, QIntValidator

from mainwindow_ui import Ui_MainWindow
from .convert import Video


class ConvertTab:
    def __init__(self, main_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_ui
        self.video = Video()
        self.before = QPixmap()
        self.after = QPixmap()
        self.setup_tab()
        
    def setup_tab(self):
        self.ui.width_lineedit.setValidator(QIntValidator())
        self.ui.height_lineedit.setValidator(QIntValidator())
        
    def reset_step2_groupbox(self):
        self.ui.width_lineedit.clear()
        self.ui.height_lineedit.clear()
        self.ui.vertical_checkbox.setChecked(False)
        self.ui.horizontal_checkbox.setChecked(False)
        self.ui.ext_combobox.setCurrentIndex(0)
        # before_lbl, before_size_lbl, after_lbl, after_size_lbl, are not to
        # clear, because they will be filled in with new values ​​soon.
        
    def get_support_exts(self) -> list[str]:
        exts = [self.ui.ext_combobox.itemText(i) for i in range(self.ui.ext_combobox.count())]
        return exts
        
    def choose_file(self):
        video_path, _ = QFileDialog.getOpenFileName(caption="Open file")
        if video_path == "":
            return
        if Path(video_path).suffix.lstrip('.') not in self.get_support_exts():
            QMessageBox.critical(None, 'EXTENSION ERROR', 'This file is not supported.')
            return
        self.ui.video_path_lineedit.setText(str(Path(video_path)))
        self.ui.video_save_as_lineedit.setText(str(Path(video_path).parent))
        self.reset_step2_groupbox()
        self.video = Video()
        before_pixmap = self.video.init(str(Path(video_path)))
        self.set_before_img(before_pixmap)
        self.set_placeholder(before_pixmap)
        self.set_after_img(before_pixmap)
        self.ui.convert_btn.setEnabled(True)
        
    def set_before_img(self, before: QPixmap):
        self.before = before
        self.ui.before_size_lbl.setText(f'Before: {before.width()} x {before.height()}')
        pixmap = before.scaled(self.ui.before_lbl.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.before_lbl.setPixmap(pixmap)
        
    def set_placeholder(self, before: QPixmap):
        self.ui.width_lineedit.setPlaceholderText(str(before.width()))
        self.ui.height_lineedit.setPlaceholderText(str(before.height()))
        
    def set_after_img(self, after: QPixmap):
        self.after = after
        self.ui.after_size_lbl.setText(f'After: {after.width()} x {after.height()}')
        pixmap = after.scaled(self.ui.after_lbl.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.after_lbl.setPixmap(pixmap)
        
    def get_input_size(self) -> tuple[int, int]:
        width = self.ui.width_lineedit.text()
        width = self.ui.width_lineedit.placeholderText() if width == '' else width
        height = self.ui.height_lineedit.text()
        height = self.ui.height_lineedit.placeholderText() if height == '' else height
        return int(width), int(height)
    
    def get_is_flip(self) -> tuple[bool, bool]:
        is_x_flip = self.ui.vertical_checkbox.isChecked()
        is_y_flip = self.ui.horizontal_checkbox.isChecked()
        return is_x_flip, is_y_flip
        
    def resize(self) -> None:
        width, height = self.get_input_size()
        self.video.resize(width, height)
        self.set_after_img(self.video.get_after_pixmap())
        
    def flip(self) -> None:
        is_x_flip, is_y_flip = self.get_is_flip()
        self.video.flip(is_x_flip, is_y_flip)
        self.set_after_img(self.video.get_after_pixmap())
        
    def rotate(self, angle: int) -> None:
        self.video.rotate(angle)
        self.set_after_img(self.video.get_after_pixmap())
        
    def convert(self):
        output_path = self.ui.video_save_as_lineedit.text()
        file_name = Path(self.ui.video_path_lineedit.text()).stem
        ext = self.ui.ext_combobox.currentText()
        full_path = str(Path(output_path) / (file_name + f'.{ext}'))
        self.video.convert(full_path, ext)

    def resize_preview(self, event: QResizeEvent):
        def resize(pixmap: QPixmap, lbl: QLabel):
            if pixmap.isNull():
                return
            new_pixmap = pixmap.scaled(lbl.width() - 5, lbl.height() - 5, aspectRatioMode=Qt.KeepAspectRatio)
            lbl.setPixmap(new_pixmap)    
        resize(self.before, self.ui.before_lbl)
        resize(self.after, self.ui.after_lbl)