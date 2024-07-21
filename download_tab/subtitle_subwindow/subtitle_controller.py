from collections import defaultdict

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QCloseEvent

from .subtitle_ui import Ui_Form as Ui_Subtitle_Form


class SubtitleSubWindow(QWidget):
    data_sent = pyqtSignal(dict, dict)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Subtitle_Form()
        self.ui.setupUi(self)
        
    def setting_tables(self, subtitles: dict[str, list[dict[str, str]]], auto_subtitles: dict[str, list[dict[str, str]]]):
        def clear_tables(table: QTableWidget):
            while table.rowCount() > 0:
                table.removeRow(table.rowCount() - 1)
        
        def get_row_items(table: QTableWidget, lang: str, subs: list[dict[str, str]]) -> list[QTableWidgetItem]:
            # setting flags
            items = [QTableWidgetItem() for _ in range(table.columnCount())]
            for idx, item in enumerate(items):
                if idx == 0 or idx == 1:  # 0: language, 1: name
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                else:
                    item.setCheckState(Qt.Unchecked)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
            
            # setting item's data
            items[0].setText(lang)
            items[1].setText(subs[0].get('name', ''))
            ext_hash = {table.horizontalHeaderItem(col).text(): col for col in range(2, table.columnCount())}
            for sub in subs:
                ext = sub.get('ext', None)
                if ext is not None and ext in ext_hash:
                    col = ext_hash[ext]
                    items[col].setFlags(items[col].flags() | Qt.ItemIsEnabled)
                    items[col].setTextAlignment(Qt.AlignCenter)
            return items
        
        def setting_table(table: QTableWidget, subtitles: dict[str, list[dict[str, str]]]):
            for row, (lang, subs) in enumerate(subtitles.items()):
                if len(subs) == 0:
                    continue
                table.insertRow(row)
                row_items = get_row_items(table, lang, subs)
                for col, item in enumerate(row_items):
                    table.setItem(row, col, item)
            header = table.horizontalHeader()
            for col in range(header.count()):
                header.setSectionResizeMode(col, QHeaderView.Stretch)
            
        clear_tables(self.ui.subtitles_table)
        clear_tables(self.ui.auto_subtitles_table)
        setting_table(self.ui.subtitles_table, subtitles)
        setting_table(self.ui.auto_subtitles_table, auto_subtitles)

    @pyqtSlot()
    def on_ok_btn_clicked(self):
        def get_choose(table: QTableWidget) -> dict[str, list[str]]:
            ans = defaultdict(list)
            for row in range(table.rowCount()):
                lang = table.item(row, 0).text()
                for col in range(2, table.columnCount()):
                    if table.item(row, col).checkState() == Qt.Checked:
                        ans[lang].append(table.horizontalHeaderItem(col).text())
            return ans
            
        subtitle_choose = get_choose(self.ui.subtitles_table)
        auto_subtitle_choose = get_choose(self.ui.auto_subtitles_table)
        self.data_sent.emit(subtitle_choose, auto_subtitle_choose)
        self.hide()
        
    def closeEvent(self, event: QCloseEvent):
        self.hide()
        event.ignore()
