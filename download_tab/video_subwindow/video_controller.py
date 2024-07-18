from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from yt_dlp.YoutubeDL import format_bytes

from .video_ui import Ui_Form as Ui_Video_Form

class VideoSubWindow(QWidget):
    data_sent = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Video_Form()
        self.ui.setupUi(self)
        self.tables = [self.ui.video_audio_table, self.ui.video_table, self.ui.audio_table]
        self.vide_audio_choose_id = ""
        self.video_choose_id = ""
        self.audio_choose_id = ""

        self.ui.video_audio_table.horizontalHeader().sortIndicatorChanged.connect(lambda col, ord: self.indicator_changed(self.ui.video_audio_table, col, ord))
        self.ui.video_table.horizontalHeader().sortIndicatorChanged.connect(lambda col, ord: self.indicator_changed(self.ui.video_table, col, ord))
        self.ui.audio_table.horizontalHeader().sortIndicatorChanged.connect(lambda col, ord: self.indicator_changed(self.ui.audio_table, col, ord))
        
    def setting_tables(self, video_audio: list[dict[str, str]], video: list[dict[str, str]], audio: list[dict[str, str]], best_formats: str):
        def get_infos(src: dict[str, str]) -> list[str]:
            infos = []
            infos.append(src.get('format_id', 'none'))
            
            infos.append(src.get('ext', 'none'))
            
            infos.append(src.get('resolution', 'none'))
            
            fps = 'none'
            if src.get('fps') is not None:
                fps = '%sfps' % int(src['fps'])
            infos.append(fps)
            
            filesize = 'none'
            if src.get('filesize') is not None:
                filesize = format_bytes(src['filesize'])
            elif src.get('filesize_approx') is not None:
                filesize = '~' + format_bytes(src['filesize_approx'])
            infos.append(filesize)
            
            tbr = 'none'
            if src.get('tbr') is not None:
                tbr = '%4dk' % src['tbr']
            infos.append(tbr)
            
            infos.append(src.get('protocol', 'none'))
            
            vcodec = 'none'
            if src.get('vcodec') is not None and src.get('vcodec') != 'none':
                vcodec = src.get('vcodec')
            infos.append(vcodec)
            
            vbr = 'none'
            if src.get('vbr') is not None:
                vbr = '%4dk' % src['vbr']
            infos.append(vbr)
            
            acodec = 'none'
            if src.get('acodec') is not None:
                if src['acodec'] == 'none':
                    acodec = 'video only'
                else:
                    acodec = '%-5s' % src['acodec']
            elif src.get('abr') is not None:
                acodec = 'audio'
            infos.append(acodec)
            
            abr = 'none'
            if src.get('abr') is not None:
                abr = '%4dk' % src['abr']
            infos.append(abr)
            return infos
        
        def clear_table(table: QTableWidget):
            table.blockSignals(True)
            while table.rowCount() > 0:
                table.removeRow(table.rowCount() - 1)
            table.blockSignals(False)
        
        def set_table_item(table: QTableWidget, infos: list[dict[str, str]]) -> None:
            table.blockSignals(True)
            for row, info in enumerate(infos[::-1]):
                items = [QTableWidgetItem()] + [QTableWidgetItem(data) for data in get_infos(info)]
                for idx, item in enumerate(items):
                    if idx == 0:
                        item.setCheckState(Qt.Unchecked)
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    else:
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                table.insertRow(row)
                for col, item in enumerate(items):
                    table.setItem(row, col, item)
                    
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            for col in range(1, header.count()):
                header.setSectionResizeMode(col, QHeaderView.Stretch)
            table.blockSignals(False)
        
        for table, table_src in zip(self.tables, [video_audio, video, audio]):
            clear_table(table)
            set_table_item(table, table_src)
        self.ui.default_lbl.setText('default best format: ' + best_formats)
        self.vide_audio_choose_id = ""
        self.video_choose_id = ""
        self.audio_choose_id = ""
                
    def lock_table(self, table: QTableWidget, except_row: int = -1):
        table.blockSignals(True)
        for row in range(table.rowCount()):
            if row != except_row:
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        table.blockSignals(False)
            
    def unlock_table(self, table: QTableWidget):
        table.blockSignals(True)
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
        table.blockSignals(False)
            
    @pyqtSlot(QTableWidgetItem)
    def on_video_audio_table_itemChanged(self, changed_item: QTableWidgetItem) -> None:
        if changed_item.checkState() == Qt.Checked:
            self.vide_audio_choose_id = self.ui.video_audio_table.item(changed_item.row(), 1).text()
            self.lock_table(self.ui.video_audio_table, changed_item.row())
            self.lock_table(self.ui.video_table)
            self.lock_table(self.ui.audio_table)
        else:
            self.unlock_table(self.ui.video_audio_table)
            self.unlock_table(self.ui.video_table)
            self.unlock_table(self.ui.audio_table)
            
    @pyqtSlot(QTableWidgetItem)
    def on_video_table_itemChanged(self, changed_item: QTableWidgetItem) -> None:
        if changed_item.checkState() == Qt.Checked:
            self.video_choose_id = self.ui.video_table.item(changed_item.row(), 1).text()
            self.lock_table(self.ui.video_audio_table)
            self.lock_table(self.ui.video_table, changed_item.row())
        else:
            self.video_choose_id = ""
            if self.audio_choose_id == "":
                self.unlock_table(self.ui.video_audio_table)
            self.unlock_table(self.ui.video_table)
            
    @pyqtSlot(QTableWidgetItem)
    def on_audio_table_itemChanged(self, changed_item: QTableWidgetItem) -> None:
        if changed_item.checkState() == Qt.Checked:
            self.audio_choose_id = self.ui.audio_table.item(changed_item.row(), 1).text()
            self.lock_table(self.ui.video_audio_table)
            self.lock_table(self.ui.audio_table, changed_item.row())
        else:
            self.audio_choose_id = ""
            if self.video_choose_id == "":
                self.unlock_table(self.ui.video_audio_table)
            self.unlock_table(self.ui.audio_table)

    @pyqtSlot()
    def on_ok_btn_clicked(self) -> None:
        format_id = '+'.join((s for s in [self.vide_audio_choose_id, self.video_choose_id, self.audio_choose_id] if s != ''))
        self.data_sent.emit(format_id)
        self.hide()

    def indicator_changed(self, table: QTableWidget, col: int, order: int):
        if table.horizontalHeaderItem(col).text() == 'RESOLUTION':
            for row in range(table.rowCount()):
                item = table.item(row, col)
                item.setText(item.text().rjust(10))
            table.sortItems(col, order)
            for row in range(table.rowCount()):
                item = table.item(row, col)
                item.setText(item.text().strip())
        else:
            table.sortItems(col, order)
        
    def closeEvent(self, event: QCloseEvent):
        self.hide()
        event.ignore()
