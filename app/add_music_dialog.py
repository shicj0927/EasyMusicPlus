from PyQt6.QtWidgets import QDialog
from ui.ui_add_music_dialog import Ui_qDialog_addMusicDialog
from app.get_netease_songlist_dialog import GetNeteaseSonglistDialog
from managers.library_manager import LibraryManager
from app.download_dialog import DownloadDialog
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from app.add_music_from_list_dialog import AddMusicFromListDialog
from app.netease_list_download_dialog import NeteaseListDownloadDialog

class AddMusicDialog(QDialog):
    downloadCompletedSignal = pyqtSignal(object)
    addedFromDataSignal = pyqtSignal(str)
    loadedSonglistSignal = pyqtSignal()
    addCompletedSignal = pyqtSignal()
    refreshPlaylistSignal = pyqtSignal()

    def __init__(self, parent, libraryManager: LibraryManager, songlist_id:str, dlconfig: dict):
        super().__init__(parent)
        self.parent = parent
        self.libraryManager = libraryManager
        self.songlist_id = songlist_id
        self.dlconfig = dlconfig
        self.getDialog=None
        self.addFromListDialog=None
        self.neteaseDialog=None
        self.ui = Ui_qDialog_addMusicDialog()
        self.ui.setupUi(self)
        self.init_ui()
        self.bind_signals()

    def init_ui(self):
        # self.ui.qComboBox_selectFromData.clear()
        # for mid in self.libraryManager.get_playlist_by_id("-----").media_ids:
        #     m = self.libraryManager.get_media_by_id(mid)
        #     self.ui.qComboBox_selectFromData.addItem(f"{m.title} - {",".join(m.artists)}", m.id)
        pass

    def bind_signals(self):
        self.ui.qPushButton_quit.clicked.connect(self.close)
        self.ui.qPushButton_add_from_list.clicked.connect(self.add_from_list)
        # self.ui.qPushButton_add_from_data.clicked.connect(self.add_from_data)
        self.ui.qPushButton_open_downloader.clicked.connect(self.open_downloader)
        self.ui.qPushButton_netease_songlist.clicked.connect(self.open_get_songlist_dialog)
        self.ui.qPushButton_netease_list_download.clicked.connect(self.open_netease_list_download_dialog)
    
    def add_from_data(self):
        media_id = self.ui.qComboBox_selectFromData.currentData()
        if media_id:
            self.libraryManager.add_media_to_playlist(self.songlist_id, self.libraryManager.get_media_by_id(media_id))
            self.addedFromDataSignal.emit(media_id)
            self.close()
    
    def add_from_list(self):
        # print(self.libraryManager)
        self.addFromListDialog=AddMusicFromListDialog(
            self.libraryManager,
            self.songlist_id
        )
        self.addFromListDialog.addedSignal.connect(self.on_added)
        self.addFromListDialog.exec()
    
    def open_downloader(self):
        if self.dlconfig.get("downloadPath"):
            downloadDialog = DownloadDialog(
                parent=self.parent,
                config=self.dlconfig
            )
            downloadDialog.downloadCompletedSignal.connect(self.on_song_download_completed)
            downloadDialog.exec()
    
    def open_get_songlist_dialog(self):
        self.getDialog=GetNeteaseSonglistDialog(
            self.libraryManager,
            self.songlist_id,self.dlconfig
        )
        self.getDialog.allCompletedSignal.connect(self.on_get_completed)
        self.getDialog.exec()

    def refresh_playlist(self):
        self.refreshPlaylistSignal.emit()

    def open_netease_list_download_dialog(self):
        self.neteaseDialog=NeteaseListDownloadDialog(
            self.libraryManager,
            self.songlist_id,self.dlconfig
        )
        self.neteaseDialog.refreshPlaylistSignal.connect(self.refresh_playlist)
        self.neteaseDialog.exec()
    
    def on_get_completed(self):
        self.getDialog.accept()
        self.loadedSonglistSignal.emit()
        # self.close()
    
    def on_song_download_completed(self, download_result):
        self.downloadCompletedSignal.emit(download_result)
        # self.close()
    
    def on_added(self):
        self.addCompletedSignal.emit()