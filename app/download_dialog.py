from PyQt6.QtWidgets import QDialog,QHeaderView
from ui.ui_download_dialog import Ui_qDialog_downloadDialog
from workers.search_worker import SearchWorker
from workers.download_worker import DownloadWorker
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtCore import QStringListModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QStyledItemDelegate, QPushButton, QApplication, QStyle
from PyQt6.QtCore import Qt

class DownloadButtonDelegate(QStyledItemDelegate):
    downloadClicked = pyqtSignal(int)
    def paint(self, painter, option, index):
        if index.column() == 2:
            from PyQt6.QtWidgets import QStyleOptionButton
            button = QStyleOptionButton()
            button.rect = option.rect
            button.text = "下载"
            button.state = QStyle.StateFlag.State_Enabled
            QApplication.style().drawControl(QApplication.style().ControlElement.CE_PushButton,button,painter)
        else:
            super().paint(painter, option, index)
    def editorEvent(self, event, model, option, index):
        if index.column() == 2 and event.type() == event.Type.MouseButtonRelease:
            row = index.row()
            print("点击下载：第", row, "行")
            self.downloadClicked.emit(index.row())
            return True
        return False

class DownloadDialog(QDialog):
    startSearchSignal = pyqtSignal(str,str,int,int)
    startDownloadSignal = pyqtSignal(object,str,str,str,bool)
    downloadCompletedSignal = pyqtSignal(object)

    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config=config
        self.ui = Ui_qDialog_downloadDialog()
        self.ui.setupUi(self)
        self.thread = QThread()
        self.searchWorker = SearchWorker()
        self.searchWorker.moveToThread(self.thread)
        self.startSearchSignal.connect(self.searchWorker.search)
        self.searchWorker.searchFinishedSignal.connect(self.on_search_finished)
        self.downloadWorker = DownloadWorker()
        self.downloadWorker.moveToThread(self.thread)
        self.startDownloadSignal.connect(self.downloadWorker.download)
        self.downloadWorker.downloadLogSingnal.connect(self.on_download_log_update)
        self.downloadWorker.parseResultSignal.connect(self.on_parse_result)
        self.downloadWorker.procressUpdateSignal.connect(self.ui.qProgressBar_download.setValue)
        self.downloadWorker.downloadFinishedSignal.connect(self.on_download_finished)
        self.thread.start()
        self.init_ui()
        self.bind_signals()
        self.delegate = DownloadButtonDelegate(self.ui.qTableView_searchResult)
        self.ui.qTableView_searchResult.setItemDelegate(self.delegate)
        self.delegate.downloadClicked.connect(self.on_download_with_info_clicked)
        self.nowSearchResult = None

    def init_ui(self):
        self.ui.qProgressBar_download.setValue(0)
        self.ui.qTabWidget_mainTabs.setCurrentIndex(0)
        self.ui.qLineEdit_url.setPlaceholderText("输入媒体URL")
        self.ui.qLineEdit_mediaId.setPlaceholderText("输入媒体ID（BV号或网易id）")
        self.ui.qLineEdit_outputPath.setPlaceholderText("输入下载路径，默认为当前目录下downloads文件夹")
        # self.ui.qLineEdit_url.setText("https://music.163.com/#/song?id=1414813561")
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["歌曲", "歌手", "下载"])
        self.ui.qTableView_searchResult.setModel(model)
        header = self.ui.qTableView_searchResult.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.ui.qTableView_searchResult.setColumnWidth(3, 80)
        if self.config!=None:
            self.ui.qLineEdit_outputPath.setReadOnly(True)
            self.ui.qCheckBox_randomIdFlag.setDisabled(True)
            self.ui.qPushButton_browsePath.setDisabled(True)
            self.ui.qLineEdit_outputPath.setText(self.config["downloadPath"])
    
    def bind_signals(self):
        self.ui.qPushButton_search.clicked.connect(self.start_search)
        self.ui.qPushButton_downloadId.clicked.connect(self.on_download_with_mediaId_clicked)
        self.ui.qPushButton_downloadUrl.clicked.connect(self.on_download_with_url_clicked)
        self.ui.qPushButton_browsePath.clicked.connect(self.on_browse_path_clicked)
    
    def start_search(self):
        keyword = self.ui.qLineEdit_searchKeyword.text()
        source = self.ui.qComboBox_searchSource.currentText()
        if source=="网易云":
            source="netease"
        else:
            source="bilibili"
        self.startSearchSignal.emit(keyword, source, 20, 1)
    
    def on_search_finished(self, result):
        self.nowSearchResult = result
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["歌曲", "歌手", "下载"])
        for i in result:
            name = QStandardItem(i["name"])
            name.setToolTip(i["name"])
            artist = QStandardItem(",".join(i["artist"]))
            artist.setToolTip(",".join(i["artist"]))
            download = QStandardItem("下载")
            model.appendRow([name, artist, download])
        self.ui.qTableView_searchResult.setModel(model)
    
    def on_download_with_info_clicked(self, row):
        if 0 <= row < len(self.nowSearchResult):
            songInfo = self.nowSearchResult[row]
        else:
            print("下载行索引超出范围")
            return
        self.ui.qTabWidget_mainTabs.setCurrentIndex(1)
        print("下载歌曲：", songInfo["name"],songInfo)
        self.ui.qLineEdit_mediaId.setText(songInfo["id"])
        self.ui.qLineEdit_url.setText("")
        self.start_download(songInfo, None, None, self.ui.qCheckBox_randomIdFlag.isChecked())
    
    def on_download_with_url_clicked(self):
        url = self.ui.qLineEdit_url.text()
        mediaId = self.ui.qLineEdit_mediaId.text()
        if url=="":
            print("请输入URL")
            return
        self.ui.qTabWidget_mainTabs.setCurrentIndex(1)
        self.start_download(None, url, None, self.ui.qCheckBox_randomIdFlag.isChecked())
    
    def on_download_with_mediaId_clicked(self):
        mediaId = self.ui.qLineEdit_mediaId.text()
        if mediaId=="":
            print("请输入媒体ID")
            return
        self.ui.qTabWidget_mainTabs.setCurrentIndex(1)
        self.start_download(None, None, mediaId, self.ui.qCheckBox_randomIdFlag.isChecked())
    
    def on_browse_path_clicked(self):
        from PyQt6.QtWidgets import QFileDialog
        dir = QFileDialog.getExistingDirectory(self, "选择下载目录", "./")
        if dir:
            self.ui.qLineEdit_outputPath.setText(dir)
    
    def start_download(self, songInfo, url, mediaId, randomIdFlag=False):
        print("开始下载：", songInfo, url, mediaId)
        self.ui.qTextBrowser_taskDetail.clear()
        self.ui.qTextBrowser_parseResult.clear()
        self.ui.qProgressBar_download.setValue(0)
        self.ui.qTextBrowser_downloadLog.clear()
        self.ui.qTextBrowser_taskDetail.append(f"下载参数：{songInfo}, {url}, {mediaId}, {randomIdFlag}")
        downloadPath = self.ui.qLineEdit_outputPath.text()
        if downloadPath=="":
            downloadPath="./downloads"
        self.startDownloadSignal.emit(songInfo, url, mediaId, downloadPath, randomIdFlag)
    
    def on_parse_result(self, songData):
        self.ui.qTextBrowser_parseResult.append(f"解析结果：{songData}")

    def on_download_log_update(self, log):
        self.ui.qTextBrowser_downloadLog.append(log)
    
    def on_download_finished(self, result):
        self.ui.qTextBrowser_downloadLog.append(f"下载结束：{result}")
        if self.config!=None:
            if result["status"]=="success":
                self.downloadCompletedSignal.emit(result["result"])
                self.thread.quit()
                self.thread.wait()
                self.accept()
    
    def closeEvent(self, a0):
        print("Dialog closing... stopping thread")
        self.thread.quit()
        self.thread.wait()
        self.accept()