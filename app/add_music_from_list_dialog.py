from PyQt6.QtWidgets import QDialog, QTreeWidgetItem
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from ui.ui_add_music_from_list_dialog import Ui_qDialog_addMusicFromListDialog
from managers.library_manager import LibraryManager
from PyQt6.QtCore import Qt
import re

class AddMusicFromListDialog(QDialog):
    addedSignal = pyqtSignal()

    def __init__(self, libraryManager: LibraryManager, songlist_id:str):
        super().__init__()
        self.ui = Ui_qDialog_addMusicFromListDialog()
        self.ui.setupUi(self)
        self.libraryManager=libraryManager
        self.songlist_id=songlist_id
        self.init_ui()
        self.bind_signals()

    def init_ui(self):
        self.show_tree()

    def bind_signals(self):
        self.ui.qPushButton_quit.clicked.connect(self.close)
        self.ui.qPushButton_add.clicked.connect(self.on_add_clicked)
        self.ui.qLineEdit_search.textChanged.connect(self.filter_tree)
    

    def fuzzy_pattern(self,text:str):
        chars =map(re.escape,text)
        return ".*?".join(chars)

    def fuzzy_match(self,text:str,key: str):
        return re.search(self.fuzzy_pattern(key), text, re.IGNORECASE)

    def show_tree(self):
        tree=self.ui.qTreeWidget_songs
        tree.clear()
        tree.setHeaderHidden(True)
        for pl in self.libraryManager.get_playlists():
            playlist_item = QTreeWidgetItem([pl.title])
            playlist_item.setFlags(
                playlist_item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsAutoTristate
            )
            playlist_item.setCheckState(0, Qt.CheckState.Unchecked)
            tree.addTopLevelItem(playlist_item)
            for mid in pl.media_ids:
                media=self.libraryManager.get_media_by_id(mid)
                song_item = QTreeWidgetItem([media.title+" - "+",".join(media.artists)])
                song_item.setFlags(
                    song_item.flags()
                    | Qt.ItemFlag.ItemIsUserCheckable
                )
                song_item.setData(0, Qt.ItemDataRole.UserRole, media)
                song_item.setCheckState(0, Qt.CheckState.Unchecked)
                playlist_item.addChild(song_item)

    def get_selected(self):
        selected=[]
        tree=self.ui.qTreeWidget_songs
        for i in range(tree.topLevelItemCount()):
            playlist = tree.topLevelItem(i)
            for j in range(playlist.childCount()):
                song = playlist.child(j)
                if (not song.isHidden()) and song.checkState(0) == Qt.CheckState.Checked:
                    selected.append(song.data(0,Qt.ItemDataRole.UserRole))
        return selected

    def on_add_clicked(self):
        selected=self.get_selected()
        for m in selected:
            self.libraryManager.add_media_to_playlist(self.songlist_id,m)
        self.addedSignal.emit()
        self.close()
    
    def filter_tree(self,text:str):
        text=text.lower().strip()
        tree=self.ui.qTreeWidget_songs
        for i in range(tree.topLevelItemCount()):
            playlist=tree.topLevelItem(i)
            visible_song=False
            for j in range(playlist.childCount()):
                song=playlist.child(j)
                # match=text in song.text(0).lower()
                match=self.fuzzy_match(song.text(0).lower(),text)
                song.setHidden(not match)
                if match:
                    visible_song = True
            playlist.setHidden(not visible_song)
            playlist.setExpanded(bool(text) and visible_song)