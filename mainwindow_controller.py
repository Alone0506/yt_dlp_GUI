import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from mainwindow_ui import Ui_MainWindow
from download_tab.download_tab import DownloadTab
from convert_tab.convert_tab import ConvertTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # setting download tab signal & slot
        self.download_tab = DownloadTab(self.ui)
        self.ui.supported_sites_btn.clicked.connect(self.download_tab.show_supported_sites)
        self.ui.get_info_btn.clicked.connect(self.download_tab.get_info)
        self.ui.path_btn.clicked.connect(self.download_tab.save_as)
        self.ui.choose_video_src_btn.clicked.connect(self.download_tab.choose_video)
        self.ui.choose_subtitle_lang_format_btn.clicked.connect(self.download_tab.choose_subtitle)
        self.ui.download_btn.clicked.connect(self.download_tab.download)
        
        # setting convert tab signal & slot 
        self.convert_tab = ConvertTab(self.ui)
        self.ui.choose_file_btn.clicked.connect(self.convert_tab.choose_file)
        
        self.ui.width_lineedit.textEdited.connect(self.convert_tab.set_after_img)
        self.ui.height_lineedit.textEdited.connect(self.convert_tab.set_after_img)
        self.ui.vertical_checkbox.toggled.connect(self.convert_tab.set_after_img)
        self.ui.horizontal_checkbox.toggled.connect(self.convert_tab.set_after_img)
        self.ui.angle_lineedit.textEdited.connect(self.convert_tab.set_after_img)
        
        self.ui.convert_btn.clicked.connect(self.convert_tab.convert)
        
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.download_tab.resize_thumbnail(event)
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
