from PyQt6.QtWidgets import QDialog
from ui.ui_get_netease_songlist_dialog import Ui_qDialog_get_netease_songlist
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from workers.get_netease_songlist_worker import getNeteaseSonglistWorker
from PyQt6.QtWidgets import QMessageBox
from managers.library_manager import LibraryManager
from models.media import MediaItem_V10
from models.library import PlayList_V20
from app.download_dialog import DownloadDialog
from repositories.media_repository import download_result_to_media_item

class GetNeteaseSonglistDialog(QDialog):
    startGetSignal=pyqtSignal(str)
    downloadCompletedSignal = pyqtSignal(object)
    allCompletedSignal = pyqtSignal()

    def __init__(self, parent, libraryManager: LibraryManager, songlist_id:str, dlconfig: dict):
        super().__init__()
        self.ui = Ui_qDialog_get_netease_songlist()
        self.ui.setupUi(self)
        self.start_workers()
        self.init_ui()
        self.bind_signals()
        self.songlist=[]
        self.next_index=0
        self.error_indexs=[]
        self.libraryManager = libraryManager
        self.songlist_id = songlist_id
        self.dlconfig = dlconfig

    def init_ui(self):
        pass

    def bind_signals(self):
        self.ui.qPushButton_quit.clicked.connect(self.close)
        self.ui.qPushButton_request.clicked.connect(self.start_get)
        self.ui.qPushButton_get_ids.clicked.connect(self.display_ids)
        self.ui.qPushButton_start.clicked.connect(self.start_download)
    
    def start_workers(self):
        self.thread = QThread()
        self.getNeteaseSonglistWorker=getNeteaseSonglistWorker()
        self.getNeteaseSonglistWorker.moveToThread(self.thread)
        self.getNeteaseSonglistWorker.getNeteaseSonglistFinishedSignal.connect(self.on_get_finished)
        self.startGetSignal.connect(self.getNeteaseSonglistWorker.get)
        self.thread.start()
        self.result=None

    def on_get_finished(self,result):
        self.ui.qPlainTextEdit_get_log.clear()
        self.result=result
        if result==None:
            self.ui.qPlainTextEdit_get_log.setPlainText("错误！请检查连接并重试！")
        else:
            print(result)
            txt=""
            txt+="歌单名："+result.get("name")+"\n"
            txt+="歌曲数："+str(len(result.get("trackIds")))+"\n"
            txt+="歌单id: "+str(result.get("id"))+"\n"
            txt+="创建者: "+result.get("creator").get("nickname")+"\n\n"
            txt+="确认无误后点击“加载”按钮将歌曲id加载到左侧编辑框"
            self.ui.qPlainTextEdit_get_log.setPlainText(txt)
    
    def start_get(self):
        url=self.ui.qLineEdit_url.text()
        self.startGetSignal.emit(url)
    
    def display_ids(self):
        ids=""
        try:
            for i in self.result.get("trackIds"):
                ids+=str(i.get("id"))+"\n"
        except:
            self.ui.qPlainTextEdit_log.setPlainText("加载失败！")
            return
        if ids!="":
            self.ui.qPlainTextEdit_song_ids.clear()
            self.ui.qPlainTextEdit_song_ids.setPlainText(ids)

    def start_download(self):
        self.songlist=[]
        ids=self.ui.qPlainTextEdit_song_ids.toPlainText()
        for line in ids.splitlines():
            try:
                line = line.strip()
                if line:
                    self.songlist.append(line)
            except Exception:
                self.songlist=[]
                self.ui.qPlainTextEdit_log.setPlainText("解析歌单错误")
                return
        if len(self.songlist)==0:
            self.ui.qPlainTextEdit_log.setPlainText("歌单为空")
            return
        self.next_index=0
        self.error_indexs=[]
        self.ui.qPlainTextEdit_log.appendPlainText(f"开始下载 {len(self.songlist)} 首歌曲...")
        self.download_next()
    
    def download_next(self):
        if self.next_index==len(self.songlist):
            self.on_all_finished()
            return
        all_songs=self.libraryManager.get_playlist_by_id("-----")
        song_id=""
        for i in all_songs.media_ids:
            song=self.libraryManager.get_media_by_id(i)
            if song.source=="netease" and song.source_id==self.songlist[self.next_index]:
                song_id=i
        if song_id!="":
            self.ui.qPlainTextEdit_log.appendPlainText(f"{self.next_index+1}: 本地已有存档")
            media=self.libraryManager.get_media_by_id(song_id)
            self.libraryManager.add_media_to_playlist(self.songlist_id, media)
            self.update_progress()
            self.next_index+=1
            self.download_next()
        else:
            self.ui.qPlainTextEdit_log.appendPlainText(f"{self.next_index+1}: 开始下载")
            downloadDialog = DownloadDialog(
                parent=self,
                config=self.dlconfig,
                autoStartId=self.songlist[self.next_index]
            )
            downloadDialog.downloadCompletedSignal.connect(self.on_song_download_completed)
            downloadDialog.exec()

    def on_song_download_completed(self,download_result):
        if "error" in download_result:
            self.ui.qPlainTextEdit_log.appendPlainText(f"{self.next_index+1}: 下载失败")
            self.error_indexs.append(self.next_index)
        else:
            self.ui.qPlainTextEdit_log.appendPlainText(f"{self.next_index+1}: 下载成功")
            media_item=download_result_to_media_item(download_result, self.libraryManager.gen_new_media_id())
            self.libraryManager.add_media_to_playlist(self.songlist_id, media_item)
        self.update_progress()
        self.next_index+=1
        self.download_next()
    
    def update_progress(self):
        if len(self.songlist):
            self.ui.qProgressBar_progress.setValue(int(100*self.next_index/len(self.songlist)))

    def on_all_finished(self):
        self.ui.qProgressBar_progress.setValue(100)
        self.allCompletedSignal.emit()
        self.accept()

    def closeEvent(self, event):
        self.stop_thread()
        event.accept()

    def reject(self):
        self.stop_thread()
        super().reject()

    def stop_thread(self):
        print("Stopping thread safely")
        if hasattr(self, "thread"):
            self.thread.quit()
            self.thread.wait()
