from PyQt6.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox
from ui.ui_main_window import Ui_mainWindow
from managers.library_manager import LibraryManager
from managers.play_manager import PlayManager,PlayMode
from managers.player_manager import PlayerState
from PyQt6.QtCore import QTimer
from repositories.media_repository import download_result_to_media_item
import os
from utils import time_s_to_m_s
import qtawesome as qta

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.libraryManager = LibraryManager()
        self.playManager=PlayManager(self.ui.qWidget_vedio)
        self.current_playlist_id=None
        self.current_media_id=None
        self.changing_slider=False
        self.init_ui()
        self.bind_signals()
        # self.libraryManager.load_library("./test/test")
        # self.load_playlists_to_ui()
    
    def set_icon(self,obj,icon):
        obj.setText("")
        obj.setIcon(qta.icon(icon))

    def init_ui(self):
        self.ui.qSplitter_mainSplitter.setSizes(
            [200, 600, 200]
        )
        self.set_icon(self.ui.qPushButton_control,"fa5s.play")
        self.set_icon(self.ui.qPushButton_next,"fa5s.forward")
        self.set_icon(self.ui.qPushButton_prev,"fa5s.backward")
        self.set_icon(self.ui.qPushButton_stop,"fa5s.stop")
        self.set_icon(self.ui.qPushButton_mode,"fa5s.list")
        self.ui.qLabel_soundIcon.setPixmap(qta.icon("fa5s.volume-up").pixmap(16,16))
        self.ui.qSlider_soundBar.setValue(100)

    def bind_signals(self):
        self.ui.qAction_quit.triggered.connect(self.close)
        self.ui.qAction_downloader.triggered.connect(self.open_download_dialog)
        self.ui.qAction_about.triggered.connect(self.open_about_dialog)
        self.ui.qAction_aboutQt.triggered.connect(lambda: QMessageBox.aboutQt(self,"关于 Qt"))
        self.ui.qAction_newDB.triggered.connect(self.create_new_library)
        self.ui.qAction_openDB.triggered.connect(self.open_library)
        self.ui.qPushButton_addSongList.clicked.connect(self.new_playlist)
        self.ui.qPushButton_removeSongList.clicked.connect(self.remove_playlist)
        self.ui.qListWidget_listsList.currentRowChanged.connect(self.on_playlist_selection_changed)
        self.ui.qListWidget_songsList.currentRowChanged.connect(self.on_song_selection_changed)
        self.ui.qPushButton_addSong.clicked.connect(self.on_add_song_clicked)
        self.ui.qPushButton_removeSong.clicked.connect(self.remove_song)
        self.ui.qPushButton_control.clicked.connect(self.playManager.playerManager.pause_resume)
        self.ui.qPushButton_stop.clicked.connect(self.playManager.playerManager.stop)
        self.playManager.playerManager.durationChangedSignal.connect(self.on_duration_changed)
        self.playManager.playerManager.stateChangedSignal.connect(self.on_state_changed)
        self.playManager.playerManager.positionChangedSignal.connect(self.on_position_changed)
        self.playManager.lyricChangedSignal.connect(self.on_lyric_changed)
        self.ui.qSlider_progressBar.valueChanged.connect(self.on_slider_value_changed)
        self.ui.qListWidget_songsList.doubleClicked.connect(self.on_song_double_clicked)
        self.ui.qPushButton_next.clicked.connect(self.on_next)
        self.ui.qPushButton_prev.clicked.connect(self.on_prev)
        self.ui.qSlider_soundBar.valueChanged.connect(self.on_vol_changed)
        self.ui.qPushButton_mode.clicked.connect(self.change_play_mode)
    
    
    def open_download_dialog(self):
        from app.download_dialog import DownloadDialog
        dialog = DownloadDialog(self)
        dialog.exec()
    
    def open_about_dialog(self):
        from app.about_dialog import AboutDialog
        dialog = AboutDialog()
        dialog.exec()
    
    def create_new_library(self):
        fa_folder=QFileDialog.getExistingDirectory(self, "选择新建媒体库目录")
        if fa_folder:
            folder=QInputDialog.getText(self, "输入媒体库名称", "媒体库名称：")
            if folder[1]:
                library_name=folder[0]
                library_path=os.path.join(fa_folder, library_name)
                if not os.path.exists(library_path):
                    os.makedirs(library_path)
                    self.libraryManager.load_library(library_path)
                    self.load_playlists_to_ui()
                else:
                    print("名称已存在！")
    
    def open_library(self):
        library_path=QFileDialog.getOpenFileName(self, "选择媒体库文件", filter="JSON Files (library.json)")[0]
        if library_path:
            library_path=os.path.dirname(library_path)
            self.libraryManager.load_library(library_path)
        self.load_playlists_to_ui()
    
    def load_playlists_to_ui(self):
        playlists=self.libraryManager.get_playlists()
        self.ui.qListWidget_listsList.clear()
        for playlist in playlists:
            self.ui.qListWidget_listsList.addItem(playlist.title)
    
    def load_playlist_to_ui(self):
        if self.current_playlist_id==None:
            self.ui.qListWidget_songsList.clear()
            return
        playlists=self.libraryManager.get_playlists()
        for pl in playlists:
            if pl.id==self.current_playlist_id:
                self.ui.qListWidget_songsList.clear()
                for m in pl.media_items:
                    # print(pl.media_items)
                    self.ui.qListWidget_songsList.addItem(m.title+" - "+",".join(m.artists))
                break
    
    def new_playlist(self):
        if not self.libraryManager.is_loaded():
            raise FileNotFoundError("library not loaded")
        title, ok = QInputDialog.getText(self, "新建歌单", "请输入歌单名称：")
        if ok and title:
            self.libraryManager.new_playlist(title)
            self.load_playlists_to_ui()
    
    def remove_playlist(self):
        current_row=self.ui.qListWidget_listsList.currentRow()
        if current_row>=0:
            playlists=self.libraryManager.get_playlists()
            playlist_id=playlists[current_row].id
            reply = QMessageBox.question(self, "确认删除", f"确定要删除歌单 '{playlists[current_row].title}' 吗？其中所有歌曲将被删除！", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.libraryManager.remove_playlist(playlist_id)
                self.load_playlists_to_ui()
    
    def remove_song(self):
        current_row=self.ui.qListWidget_songsList.currentRow()
        if current_row>=0:
            media=self.libraryManager.get_media_by_index(self.current_playlist_id,current_row)
            reply=QMessageBox.question(self, "确认删除", f"确认删除 '{media.title}' 吗？",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply==QMessageBox.StandardButton.Yes:
                self.libraryManager.remove_media_from_playlist(self.current_playlist_id,media.id)
                self.load_playlist_to_ui()
    
    def on_playlist_selection_changed(self, current_row):
        if current_row<0:
            self.current_playlist_id=None
            self.current_media_id=None
        else:
            self.current_playlist_id=self.libraryManager.get_playlist_by_index(current_row).id
        self.load_playlist_to_ui()
    
    def on_song_selection_changed(self, current_row):
        if self.current_playlist_id==None or current_row<0:
            self.current_media_id=None
            return
        self.current_media_id=self.libraryManager.get_media_by_index(self.current_playlist_id,current_row).id
    
    def on_add_song_clicked(self):
        if not self.libraryManager.is_loaded():
            raise FileNotFoundError("library not loaded")
        from app.download_dialog import DownloadDialog
        downloadDialog = DownloadDialog(self,config={"downloadPath": self.libraryManager.repository.library.master_folder})
        downloadDialog.downloadCompletedSignal.connect(self.on_song_download_completed)
        downloadDialog.exec()

    def on_song_download_completed(self, download_result):
        media_item=download_result_to_media_item(download_result, self.libraryManager.gen_new_media_id())
        self.libraryManager.add_media_to_playlist(self.current_playlist_id, media_item)
        self.load_playlist_to_ui()
    
    def on_duration_changed(self, duration):
        self.ui.qSlider_progressBar.setMaximum(int(duration))
        self.ui.qLabel_progressLeft.setText("00:00/"+time_s_to_m_s(duration))
        self.ui.qLabel_progressRight.setText(time_s_to_m_s(duration))

    def on_state_changed(self, state):
        print("get state:",state)
        if state==PlayerState.STOPPED:
            self.ui.qLabel_lyricAreaSongname.setText("")
            self.ui.qLabel_lyric.setText("")
            self.ui.qLabel_nowPlaying.setText("当前播放：-")
            self.ui.qLabel_progressLeft.setText("--:--/--:--")
            self.ui.qLabel_progressRight.setText("--:--")
            self.set_icon(self.ui.qPushButton_control,"fa5s.play")
        elif state==PlayerState.PLAYING:
            media=self.playManager.get_current_media()
            self.ui.qLabel_lyricAreaSongname.setText(media.title)
            self.ui.qLabel_nowPlaying.setText("当前播放："+media.title)
            self.set_icon(self.ui.qPushButton_control,"fa5s.pause")
        elif state==PlayerState.PAUSED:
            media=self.playManager.get_current_media()
            self.ui.qLabel_nowPlaying.setText("当前播放："+media.title+"[暂停]")
            self.set_icon(self.ui.qPushButton_control,"fa5s.play")
        elif state==PlayerState.WAITING:
            media=self.playManager.auto_play_next()
            if self.playManager.check_type(media)=="video":
                self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_vedio)
            else:
                self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_song)

    def on_position_changed(self, position):
        self.changing_slider=True
        self.ui.qSlider_progressBar.setValue(int(position))
        duration=self.playManager.playerManager.get_duration()
        self.ui.qLabel_progressLeft.setText(time_s_to_m_s(position)+"/"+time_s_to_m_s(duration))
        self.ui.qLabel_progressRight.setText(time_s_to_m_s(duration-position))
        self.changing_slider=False
    
    def on_slider_value_changed(self):
        if self.changing_slider==False:
            seconds=self.ui.qSlider_progressBar.value()
            self.playManager.playerManager.seek_absolute(seconds)
    
    def on_lyric_changed(self,text):
        if self.playManager.playerManager.get_state()==PlayerState.STOPPED:
            self.ui.qLabel_lyric.setText("")
        elif text!=None:
            self.ui.qLabel_lyric.setText(text)
    
    def on_song_double_clicked(self):
        media=self.libraryManager.get_media_by_id(self.current_playlist_id,self.current_media_id)
        if self.playManager.check_type(media)=="video":
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_vedio)
        else:
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_song)
            # self.ui.qLabel_lyricAreaSongname.setText(media.title)
            # self.ui.qLabel_lyric.setText("")
        play_list=self.libraryManager.get_playlist_by_id(self.current_playlist_id)
        self.playManager.play(media,play_list)
    
    def on_next(self):
        media=self.playManager.play_next()
        if self.playManager.check_type(media)=="video":
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_vedio)
        else:
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_song)
    
    def on_vol_changed(self):
        vol=self.ui.qSlider_soundBar.value()
        self.playManager.playerManager.set_volume(vol)
    
    def on_prev(self):
        media=self.playManager.play_prev()
        if self.playManager.check_type(media)=="video":
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_vedio)
        else:
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_song)
    
    def change_play_mode(self):
        self.playManager.change_play_mode()
        if self.playManager.play_mode==PlayMode.SEQUENCE:
            self.set_icon(self.ui.qPushButton_mode,"fa5s.list")
        elif self.playManager.play_mode==PlayMode.LOOP:
            self.set_icon(self.ui.qPushButton_mode,"fa5s.sync")
        elif self.playManager.play_mode==PlayMode.RANDOM:
            self.set_icon(self.ui.qPushButton_mode,"fa5s.random")
        print(self.playManager.play_mode)