from PyQt6.QtWidgets import QDialog, QProgressDialog
from PyQt6.QtWidgets import QDialog, QTreeWidgetItem
from PyQt6.QtCore import Qt, QCoreApplication, pyqtSignal
from ui.ui_search_lyric_dialog import Ui_qDialog_searchLyricDialog
from managers.library_manager import LibraryManager
from managers.lyric_manager import LyricManager
from models.media import Lyric,LyricLine,LyricTrack
from PyQt6.QtGui import QBrush, QColor, QFont

class SearchLyricDialog(QDialog):
    songDoubleClicked=pyqtSignal(str)

    def __init__(self,libmgr:LibraryManager,parent=None):
        super().__init__()
        self.ui=Ui_qDialog_searchLyricDialog()
        self.libraryManager=libmgr
        self.ui.setupUi(self)
        self.lyrics=[]
        self.titles=[]
        self.ids=[]
        self.parent=parent
        self.init_ui()
        self.init_lib()
        self.show_tree()
        self.bind_signals()

    def init_ui(self):
        self.ui.qProgressBar.setValue(0)
        self.ui.qTreeWidget_lyric.clear()
        self.ui.qTreeWidget_lyric.setHeaderHidden(True)
        self.ui.qProgressBar.hide()
        self.ui.qPushButton_search.hide()

    def init_lib(self):
        songs=self.libraryManager.get_playlist_by_id("-----")
        progress = QProgressDialog(
            "正在加载歌词...",
            None,
            0,
            len(songs.media_ids),
            self.parent
        )
        progress.setWindowTitle("歌词搜索")
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress.setAutoClose(False)
        progress.setAutoReset(False)
        progress.show()
        progress.setValue(0)
        QCoreApplication.processEvents()
        for i in range(len(songs.media_ids)):
            current_id=songs.media_ids[i]
            media=self.libraryManager.get_media_by_id(current_id)
            lm=LyricManager()
            try:
                lm.load(media.lyric_track.path)
                tmp=[]
                for j in lm.lyric.lines:
                    tmp.append(j.text)
                self.titles.append(media.title)
                self.lyrics.append(tmp)
                self.ids.append(media.id)
            except:
                print("Fail to get lyric for",media.id,",",media.title)
            progress.setValue(int(100*(i+1)/len(songs.media_ids)))
            QCoreApplication.processEvents()
        progress.close()
        progress.deleteLater()

    def show_tree(self):
        tree=self.ui.qTreeWidget_lyric
        tree.clear()
        tree.setHeaderHidden(True)
        for i in range(len(self.titles)):
            item=QTreeWidgetItem([self.titles[i]])
            item.setData(0, Qt.ItemDataRole.UserRole,self.ids[i])
            tree.addTopLevelItem(item)
            for j in self.lyrics[i]:
                sub_item=QTreeWidgetItem([j])
                sub_item.setData(0, Qt.ItemDataRole.UserRole,self.ids[i])
                item.addChild(sub_item)

    def filter_tree(self,text:str):
            text=text.lower().strip()
            tree=self.ui.qTreeWidget_lyric
            for i in range(tree.topLevelItemCount()):
                playlist=tree.topLevelItem(i)
                visible_song=False
                for j in range(playlist.childCount()):
                    song=playlist.child(j)
                    # match=text in song.text(0).lower()
                    match=(text in song.text(0).lower())
                    song.setHidden(not match)
                    if match:
                        visible_song = True
                playlist.setHidden(not visible_song)
                playlist.setExpanded(bool(text) and visible_song)

    def bind_signals(self):
        self.ui.qPushButton_quit.clicked.connect(self.close)
        self.ui.qLineEdit_search.textChanged.connect(self.filter_tree)
        self.ui.qTreeWidget_lyric.itemDoubleClicked.connect(self.on_item_double_clicked)

    def on_item_double_clicked(self,item,column):
        song_id=item.data(0, Qt.ItemDataRole.UserRole)
        if song_id is None:
            return
        self.songDoubleClicked.emit(song_id)