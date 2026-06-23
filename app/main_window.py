from PyQt6.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox, QListWidget
from PyQt6.QtWidgets import QApplication, QListWidgetItem, QLabel, QWidget, QVBoxLayout
from ui.ui_main_window import Ui_mainWindow
from app.download_dialog import DownloadDialog
from app.about_dialog import AboutDialog
from app.add_music_dialog import AddMusicDialog
from managers.library_manager import LibraryManager
from managers.play_manager import PlayManager,PlayMode
from managers.player_manager import PlayerState
from managers.share_manager import save_share_html
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from repositories.media_repository import download_result_to_media_item
from managers.session_manager import SessionManager,Session
from utils import load_theme,safe_file_name
import os
from utils import time_s_to_m_s
import qtawesome as qta
import qdarktheme
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.sessionManager=SessionManager()
        self.libraryManager=LibraryManager()
        self.playManager=PlayManager(self.ui.qWidget_vedio,self.libraryManager)
        self.timer_5s=QTimer()
        self.timer_5s.setInterval(5000)
        self.timer_5s.start()
        self.current_playlist_id=None
        self.current_media_id=None
        self.changing_slider=False
        self.lyricLabels = []
        self.init_ui()
        self.bind_signals()
        self.theme="dark"
        self.auto_clear_current_id_lock=False
        self.app=QApplication.instance()
        self.app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
        self.sessionManager.load_session()
        self.apply_session()
        # self.libraryManager.load_library("./test/test")
        # self.load_playlists_to_ui()
    
    def set_icon(self,obj,icon):
        obj.setText("")
        obj.setIcon(qta.icon(icon,color="#3daee9"))

    def init_ui(self):
        self.ui.qSplitter_mainSplitter.setSizes(
            [200, 600, 200]
        )
        self.set_icon(self.ui.qPushButton_control,"fa5s.play")
        self.set_icon(self.ui.qPushButton_next,"fa5s.forward")
        self.set_icon(self.ui.qPushButton_prev,"fa5s.backward")
        self.set_icon(self.ui.qPushButton_stop,"fa5s.stop")
        self.set_icon(self.ui.qPushButton_mode,"fa5s.list")
        self.ui.qLabel_soundIcon.setPixmap(qta.icon("fa5s.volume-up",color="#3daee9").pixmap(16,16))
        self.ui.qSlider_soundBar.setValue(100)
        self.lyricContainer = QWidget()
        self.lyricLayout = QVBoxLayout()
        self.lyricLayout.setSpacing(5)
        self.lyricLayout.setContentsMargins(10, 10, 10, 10)
        self.lyricContainer.setLayout(self.lyricLayout)
        self.ui.qScrollArea_lyrics.setWidget(self.lyricContainer)
        self.ui.qScrollArea_lyrics.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.qScrollArea_lyrics.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.qPushButton_empty.setDisabled(True)
        self.ui.qListWidget_listsList.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.ui.qListWidget_songsList.setDragDropMode(QListWidget.DragDropMode.InternalMove)

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
        self.ui.qPushButton_theme.clicked.connect(self.change_theme)
        self.timer_5s.timeout.connect(self.update_session)
        self.ui.qPushButton_shareList.clicked.connect(self.share_playlist)
        self.ui.qListWidget_listsList.model().rowsMoved.connect(self.on_playlists_reordered)
        self.ui.qListWidget_songsList.model().rowsMoved.connect(self.on_songs_reordered)

    def change_theme(self):
        if self.theme=="dark":
            self.theme="light"
        else:
            self.theme="dark"
        self.app.setStyleSheet(qdarktheme.load_stylesheet(self.theme))
        self.update_session()
    
    def sellect_playlist_by_id(self, playlist_id):
        playlists=self.libraryManager.get_playlists()
        for index, pl in enumerate(playlists):
            if pl.id==playlist_id:
                self.ui.qListWidget_listsList.setCurrentRow(index)
                break

    def apply_session(self):
        session=self.sessionManager.get_session()
        print(session)
        self.theme=session.theme
        self.app.setStyleSheet(qdarktheme.load_stylesheet(self.theme))
        self.ui.qSlider_soundBar.setValue(session.vol)
        self.current_playlist_id=session.current_playlist_id
        if session.lib!="" and session.lib!=None:
            # self.auto_clear_current_id_lock=True
            self.libraryManager.load_library(session.lib)
            self.load_playlists_to_ui()
            self.sellect_playlist_by_id(self.current_playlist_id)
            self.load_playlist_to_ui()
            print("session applied, current playlist id:",self.current_playlist_id)
            # self.auto_clear_current_id_lock=False
    
    def update_session(self):
        session=Session()
        session.theme=self.theme
        session.vol=self.ui.qSlider_soundBar.value()
        session.current_playlist_id=self.current_playlist_id
        if self.libraryManager.is_loaded:
            session.lib=os.getcwd()
        print("update session:",session)
        self.sessionManager.set_session(session)
    
    def open_download_dialog(self):
        dialog = DownloadDialog(self)
        dialog.exec()
    
    def open_about_dialog(self):
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
        self.update_session()
    
    def open_library(self):
        library_path=QFileDialog.getOpenFileName(self, "选择媒体库文件", filter="JSON Files (library.json)")[0]
        if library_path:
            library_path=os.path.dirname(library_path)
            self.libraryManager.load_library(library_path)
        self.load_playlists_to_ui()
        self.update_session()

    def load_playlists_to_ui(self):
        playlists=self.libraryManager.get_playlists()
        self.ui.qListWidget_listsList.clear()
        for playlist in playlists:
            item=QListWidgetItem(playlist.title)
            item.setData(Qt.ItemDataRole.UserRole, playlist.id)
            self.ui.qListWidget_listsList.addItem(item)
    
    def load_playlist_to_ui(self):
        # breakpoint()
        print("load playlist to ui, current playlist id:",self.current_playlist_id)
        if self.current_playlist_id==None:
            self.ui.qListWidget_songsList.clear()
            return
        playlists=self.libraryManager.get_playlists()
        flag=False
        for pl in playlists:
            if pl.id==self.current_playlist_id:
                flag=True
                self.ui.qListWidget_songsList.clear()
                for m in pl.media_ids:
                    media_item=self.libraryManager.get_media_by_id(m)
                    item=QListWidgetItem(media_item.title+" - "+",".join(media_item.artists))
                    item.setData(Qt.ItemDataRole.UserRole, media_item.id)
                    self.ui.qListWidget_songsList.addItem(item)
                print(f"playlist {pl.title} ({pl.id}) loaded to ui")
                break
        if flag==False:
            self.ui.qListWidget_songsList.clear()
            self.current_playlist_id=None
    
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
            if playlist_id=="-----":
                return
            reply = QMessageBox.question(self, "确认删除", f"确定要删除歌单 '{playlists[current_row].title}' 吗？其中所有歌曲将被删除！", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.libraryManager.remove_playlist(playlist_id)
                self.load_playlists_to_ui()
    
    def remove_song(self):
        current_row=self.ui.qListWidget_songsList.currentRow()
        if current_row>=0:
            media=self.libraryManager.get_media_by_index(self.current_playlist_id,current_row)
            info=f"确认从歌单移除 '{media.title}' 吗？"
            if self.current_playlist_id=="-----":
                influence=self.libraryManager.check_remove_influence(media.id)
                if influence:
                    info=f"确认删除 '{media.title}' 吗？\n\n注意：该歌曲存在于以下歌单中，将同时被删除：\n{"\n".join(influence)}"
                else:
                    info=f"确认删除 '{media.title}' 吗？\n\n注意：将删除该歌曲的数据文件！"
            reply=QMessageBox.question(self, "确认删除", info,
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply==QMessageBox.StandardButton.Yes:
                self.libraryManager.remove_media_from_playlist(self.current_playlist_id,media.id)
                self.load_playlist_to_ui()
    
    def on_playlist_selection_changed(self, current_row):
        if self.auto_clear_current_id_lock:
            return
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
        if self.current_playlist_id=="-----":
            download_dialog = DownloadDialog(self,config={"downloadPath": self.libraryManager.repository.library.master_folder})
            download_dialog.downloadCompletedSignal.connect(self.on_song_download_completed)
            download_dialog.exec()
        else:
            add_music_dialog = AddMusicDialog(
                parent=self,
                libraryManager=self.libraryManager,
                songlist_id=self.current_playlist_id,
                dlconfig={"downloadPath": self.libraryManager.repository.library.master_folder}
            )
            add_music_dialog.downloadCompletedSignal.connect(self.on_song_download_completed)
            add_music_dialog.addedFromDataSignal.connect(lambda media_id: self.on_song_added_from_data(media_id))
            add_music_dialog.exec()
        
    def on_song_added_from_data(self, media_id):
        self.load_playlist_to_ui()

    def on_song_download_completed(self, download_result):
        media_item=download_result_to_media_item(download_result, self.libraryManager.gen_new_media_id())
        self.libraryManager.add_media_to_playlist(self.current_playlist_id, media_item)
        self.load_playlist_to_ui()
    
    def on_duration_changed(self, duration):
        self.ui.qSlider_progressBar.setMaximum(int(duration))
        self.ui.qLabel_progressLeft.setText("00:00/"+time_s_to_m_s(duration))
        self.ui.qLabel_progressRight.setText(time_s_to_m_s(duration))

    def clear_lyrics(self):
        while self.lyricLayout.count():
            item = self.lyricLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.lyricLabels.clear()

    def on_state_changed(self, state):
        print("get state:",state)
        if state==PlayerState.STOPPED:
            self.ui.qLabel_lyricAreaSongname.setText("")
            self.clear_lyrics()
            self.ui.qLabel_nowPlaying.setText("当前播放：-")
            self.ui.qLabel_progressLeft.setText("--:--/--:--")
            self.ui.qLabel_progressRight.setText("--:--")
            self.set_icon(self.ui.qPushButton_control,"fa5s.play")
        elif state==PlayerState.PLAYING:
            media=self.playManager.get_current_media()
            self.ui.qLabel_lyricAreaSongname.setText(media.title)
            lyric_lines=self.playManager.lyricManager.get_lyric_lines()
            for line in lyric_lines:
                label = QLabel(line.text)
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont()
                font.setPointSize(13)
                label.setFont(font)
                label.setStyleSheet("""
                    color: gray;
                    padding: 5px;
                """)
                self.lyricLayout.addWidget(label)
                self.lyricLabels.append(label)
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
    
    def on_lyric_changed(self, index):
        if index < 0 or index >= len(self.lyricLabels):
            return
        for label in self.lyricLabels:
            font = label.font()
            font.setPointSize(13)
            font.setBold(False)
            label.setFont(font)
            label.setStyleSheet("""
                color: gray;
                padding: 5px;
            """)
        current_label = self.lyricLabels[index]
        font = current_label.font()
        font.setPointSize(15)
        font.setBold(True)
        current_label.setFont(font)
        if self.theme=="dark":
            current_label.setStyleSheet("""
                color: white;
                padding: 5px;
            """)
        else:
            current_label.setStyleSheet("""
                color: black;
                padding: 5px;
            """)
        scroll_area = self.ui.qScrollArea_lyrics
        scrollbar = scroll_area.verticalScrollBar()
        target = (
            current_label.y()
            - scroll_area.viewport().height() // 2
            + current_label.height() // 2
        )
        target = max(0, target)
        self.lyricAnimation = QPropertyAnimation(
            scrollbar,
            b"value"
        )
        self.lyricAnimation.setDuration(300)
        self.lyricAnimation.setStartValue(
            scrollbar.value()
        )
        self.lyricAnimation.setEndValue(target)
        self.lyricAnimation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )
        self.lyricAnimation.start()
    
    def on_song_double_clicked(self):
        media=self.libraryManager.get_media_by_id(self.current_media_id)
        if self.playManager.check_type(media)=="video":
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_vedio)
        else:
            self.ui.qStackedWidget_playArea.setCurrentWidget(self.ui.qWidget_song)
        self.playManager.play(media,self.current_playlist_id)
    
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
    
    def share_playlist(self):
        if self.current_playlist_id==None:
            return
        playlist=self.libraryManager.get_playlist_by_id(self.current_playlist_id)
        filename=safe_file_name(playlist.title)+".html"
        file_path=QFileDialog.getSaveFileName(self, "保存歌单", filename, filter="HTML Files (*.html)")[0]
        if file_path:
            save_share_html(self.libraryManager, self.current_playlist_id, playlist.title, file_path)
            open = QMessageBox.question(self, "成功", "歌单已保存，是否打开？", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if open == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
    
    def on_playlists_reordered(self, parent, start, end, destination, row):
        new_order=[]
        for i in range(self.ui.qListWidget_listsList.count()):
            playlist_id=self.ui.qListWidget_listsList.item(i).data(Qt.ItemDataRole.UserRole)
            new_order.append(playlist_id)
        self.libraryManager.change_playlists_order(new_order)

    def on_songs_reordered(self, parent, start, end, destination, row):
        if self.current_playlist_id==None:
            return
        new_order=[]
        for i in range(self.ui.qListWidget_songsList.count()):
            media_id=self.ui.qListWidget_songsList.item(i).data(Qt.ItemDataRole.UserRole)
            new_order.append(media_id)
        self.libraryManager.change_medias_order(self.current_playlist_id, new_order)

    def closeEvent(self, event):
        self.update_session()
        exit()