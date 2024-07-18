from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from mainwindow_ui import Ui_MainWindow
from download_tab.download_tab import DownloadTab

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
        
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.download_tab.resize_thumbnail(event)
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
