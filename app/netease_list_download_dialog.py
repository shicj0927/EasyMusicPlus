from PyQt6.QtWidgets import QDialog,QHeaderView,QProgressBar,QLabel
from ui.ui_netease_list_download_dialog import Ui_qDialog_downloadListDialog
from managers.library_manager import LibraryManager
from PyQt6.QtCore import QThread, QTimer
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from workers.get_netease_songlist_worker import getNeteaseSonglistWorker
from workers.download_worker import DownloadWorker
from PyQt6.QtWidgets import QMessageBox
from models.media import MediaItem_V10
from repositories.media_repository import download_result_to_media_item

class NeteaseListDownloadDialog(QDialog):
    startGetSignal=pyqtSignal(str)
    startDownloadSignal=pyqtSignal(object, str, str, str, bool)
    refreshPlaylistSignal=pyqtSignal()

    def __init__(self, libraryManager: LibraryManager, songlist_id:str, dlconfig: dict):
        super().__init__()
        self.ui = Ui_qDialog_downloadListDialog()
        self.ui.setupUi(self)
        self.start_workers()
        self.libraryManager=libraryManager
        self.songlist_id=songlist_id
        self.dlconfig=dlconfig
        self.id_list=[]
        self.psb_list=[]
        self.sta_list=[]
        self.id_dict={}
        self.is_downloaded=[]
        self.downloading=False
        self.current_index=0
        self.result=None
        self.init_ui()
        self.bind_signals()

    def init_ui(self):
        model=QStandardItemModel()
        model.setHorizontalHeaderLabels(["id","曲名","作者","状态","进度"])
        self.ui.qTableView_detail.setModel(model)
        header=self.ui.qTableView_detail.horizontalHeader()
        header.setSectionResizeMode(0,QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2,QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3,QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4,QHeaderView.ResizeMode.Interactive)
        self.ui.qProgressBar_progress.setValue(0)
        self.ui.qPushButton_pause.hide()
        #Debug Start
        # self.ui.qLineEdit_source.setText("6886060493")
        #Debug End

    def bind_signals(self):
        self.ui.qPushButton_quit.clicked.connect(self.close)
        self.ui.qPushButton_get.clicked.connect(self.start_get)
        self.ui.qPushButton_download.clicked.connect(self.start_download)

    def start_workers(self):
        self.searchThread=QThread()
        self.getNeteaseSonglistWorker=getNeteaseSonglistWorker()
        self.getNeteaseSonglistWorker.moveToThread(self.searchThread)
        self.getNeteaseSonglistWorker.getNeteaseSonglistFinishedSignal.connect(self.on_get_finished)
        self.startGetSignal.connect(self.getNeteaseSonglistWorker.get)
        self.searchThread.start()
        self.result=None
        self.downloadThread=QThread()
        self.downloadWorker=DownloadWorker()
        self.downloadWorker.parseResultSignal.connect(self.on_get_parse_result)
        self.downloadWorker.downloadLogSingnal.connect(self.on_get_download_log)
        self.downloadWorker.procressUpdateSignal.connect(self.on_progress_updated)
        self.downloadWorker.downloadFinishedSignal.connect(self.on_download_finished)
        self.startDownloadSignal.connect(self.downloadWorker.download)
        self.downloadWorker.moveToThread(self.downloadThread)
        self.downloadThread.start()

    def on_get_parse_result(self,result):
        self.ui.qPlainTextEdit_log.appendPlainText(str(result))

    def on_get_download_log(self,log):
        self.ui.qPlainTextEdit_log.appendPlainText(log)

    def on_progress_updated(self,val):
        self.psb_list[self.current_index].setValue(val)
        
    def start_get(self):
        if self.downloading:
            return
        self.ui.qLabel_name.clear()
        self.ui.qLabel_num.clear()
        self.ui.qLabel_writer.clear()
        self.ui.qProgressBar_progress.setValue(0)
        self.ui.qTableView_detail.clearMask()
        self.id_list=[]
        self.psb_list=[]
        self.sta_list=[]
        self.is_downloaded=[]
        id=self.ui.qLineEdit_source.text()
        self.startGetSignal.emit(id)

    def on_get_finished(self,result):
        if result==None:
            self.result=None
            self.ui.qLabel_name.setText("获取失败，请检查网络")
        else:
            result=result.get("playlist")
            self.result=result
            self.ui.qLabel_name.setText(result.get("name"))
            self.ui.qLabel_num.setText(str(len(result.get("trackIds"))))
            self.ui.qLabel_writer.setText(result.get("creator").get("nickname"))
            """
            {'name': '情歌',
            'mainTitle': None,
            'additionalTitle': None,
            'id': 254059, 'pst': 0, 't': 0, 
            'ar': [{'id': 8325, 'name': '梁静茹', 'tns': [], 'alias': []}],
            ......
            ["id","曲名","作者","状态","进度"]
            """
            # try:
            model=QStandardItemModel()
            model.setHorizontalHeaderLabels(["id","曲名","作者","状态","进度"])
            self.ui.qTableView_detail.setModel(model)
            all_songs=self.libraryManager.get_playlist_by_id("-----")
            self.id_dict={}
            for i in all_songs.media_ids:
                song=self.libraryManager.get_media_by_id(i)
                if song.source=="netease":
                    self.id_dict[song.source_id]=song.id
            for row in range(len(self.result.get("tracks"))):
                i=self.result.get("tracks")[row]
                id=QStandardItem(str(i.get("id")))
                id.setToolTip(str(i.get("id")))
                self.id_list.append(str(i.get("id")))
                name=QStandardItem(i.get("name"))
                name.setToolTip(i.get("name"))
                artist_list=[]
                for j in i.get("ar"):
                    artist_list.append(j.get("name"))
                artist_text=",".join(artist_list)
                artist=QStandardItem(artist_text)
                artist.setToolTip(artist_text)
                status_item=QStandardItem()
                progress_item=QStandardItem()
                model.appendRow([
                    id,
                    name,
                    artist,
                    status_item,
                    progress_item
                ])
                psb=QProgressBar()
                index=model.index(row,4)
                self.ui.qTableView_detail.setIndexWidget(index,psb)
                self.psb_list.append(psb)
                lbl=QLabel()
                if str(i.get("id")) in self.id_dict:
                    self.is_downloaded.append(1)
                    lbl.setText("已有存档")
                    lbl.setStyleSheet("color: green;")
                    psb.setValue(100)
                else:
                    self.is_downloaded.append(0)
                    lbl.setText("等待下载")
                    lbl.setStyleSheet("color: blue;")
                self.sta_list.append(lbl)
                index=model.index(row,3)
                self.ui.qTableView_detail.setIndexWidget(index,lbl)
            # except:
            #     print("ERROR")
    
    def from_library_to_list(self,index):
        self.libraryManager.add_media_to_playlist(
            self.songlist_id,self.libraryManager.get_media_by_id(self.id_dict[self.id_list[index]])
        )

    def start_download(self):
        if self.result==None or len(self.sta_list)==0:
            return
        self.downloading=True
        self.current_index=0
        while self.current_index<len(self.is_downloaded) and self.is_downloaded[self.current_index]:
            self.from_library_to_list(self.current_index)
            self.current_index+=1
        self.refreshPlaylistSignal.emit()
        if self.current_index==len(self.is_downloaded)-1 and self.is_downloaded[self.current_index]:
            self.from_library_to_list(self.current_index)
            self.refreshPlaylistSignal.emit()
            QMessageBox.information(self,"提示","下载完成")
            self.downloading=False
            return
        self.sta_list[self.current_index].setText("下载中")
        self.sta_list[self.current_index].setStyleSheet("color: orange;")
        # self.downloadWorker.download(None,None,self.id_list[self.current_index],
        #                              self.dlconfig["downloadPath"],True)
        self.startDownloadSignal.emit(None,None,self.id_list[self.current_index],
                                        self.dlconfig["downloadPath"],True)

    def on_download_finished(self,result):
        self.ui.qPlainTextEdit_log.appendPlainText(str(result))
        if result.get("status")!="success":
            self.ui.qPlainTextEdit_log.appendPlainText(result.get("message"))
            self.sta_list[self.current_index].setText("下载失败")
            self.sta_list[self.current_index].setStyleSheet("color: red;")
        else:
            self.sta_list[self.current_index].setText("下载完成")
            self.sta_list[self.current_index].setStyleSheet("color: green;")
            res=download_result_to_media_item(result.get("result"),self.libraryManager.gen_new_media_id())
            self.libraryManager.add_media_to_playlist(self.songlist_id,res)
        self.refreshPlaylistSignal.emit()
        self.current_index+=1
        while self.current_index<len(self.id_list) and self.is_downloaded[self.current_index]:
            self.from_library_to_list(self.current_index)
            self.current_index+=1
        self.ui.qProgressBar_progress.setValue(int(100*self.current_index/len(self.id_list)))
        if self.current_index==len(self.id_list) or self.is_downloaded[self.current_index]:
            if self.current_index<len(self.id_list):
                self.from_library_to_list(self.current_index)
            self.ui.qProgressBar_progress.setValue(100)
            QMessageBox(self,"消息","全部下载完成！")
            self.downloading=False
        # self.downloadWorker.download(None,None,self.id_list[self.current_index],
        #                                      self.dlconfig["downloadPath"],True)
        self.sta_list[self.current_index].setText("下载中")
        self.sta_list[self.current_index].setStyleSheet("color: orange;")
        self.startDownloadSignal.emit(None,None,self.id_list[self.current_index],
                                        self.dlconfig["downloadPath"],True)

    def closeEvent(self, event):
        self.stop_thread()
        event.accept()

    def reject(self):
        self.stop_thread()
        super().reject()

    def stop_thread(self):
        print("Stopping thread safely")
        if hasattr(self, "thread"):
            self.searchThread.quit()
            self.searchThread.wait()
            self.downloadThread.quit()
            self.downloadThread.wait()
