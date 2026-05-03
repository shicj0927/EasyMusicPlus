from managers.player_manager import PlayerManager,PlayerState
from managers.lyric_manager import LyricManager
from models.media import MediaItem
from models.library import PlayList
from PyQt6.QtCore import QObject, pyqtSignal
import random
from enum import Enum

class PlayMode(Enum):
    SEQUENCE = 0
    LOOP = 1
    RANDOM = 2

class PlayManager(QObject):
    lyricChangedSignal=pyqtSignal(int)

    def __init__(self,widget):
        super().__init__()
        self.media=None
        self.playerManager=PlayerManager(widget)
        self.lyricManager=LyricManager()
        self.play_mode=PlayMode.SEQUENCE
        self.play_list=None
        self.playerManager.positionChangedSignal.connect(self.on_position_changed)
    
    def check_type(self,media:MediaItem) -> str:
        if media.video_track!=None:
            return "video"
        else:
            return "audio"
    
    def on_position_changed(self,time_s):
        time_ms=int(time_s*1000)
        self.lyricChangedSignal.emit(self.lyricManager.get_current_lyric_index(time_ms))
    
    def play(self,media:MediaItem,play_list=None):
        self.media=media
        if play_list!=None:
            self.play_list=play_list
        if media.lyric_track!=None:
            self.lyricManager.load(media.lyric_track.path)
        if media.video_track!=None:
            self.playerManager.play(media.video_track.path)
        else:
            self.playerManager.play(media.audio_track.path)
    
    def auto_play_next(self):
        # self.playerManager.lock_switching()
        now_index=None
        if self.play_list!=None:
            for i in range(len(self.play_list.media_items)):
                m=self.play_list.media_items[i]
                if m==self.media:
                    now_index=i
        if self.play_mode==PlayMode.LOOP:
            self.play(self.media)
        elif self.play_mode==PlayMode.SEQUENCE:
            if now_index==None:
                raise RuntimeError("media index not found")
            next_index=(now_index+1)%len(self.play_list.media_items)
            self.play(self.play_list.media_items[next_index])
        else:
            if now_index==None:
                raise RuntimeError("media index not found")
            next_index=random.randint(0,len(self.play_list.media_items)-1)
            self.play(self.play_list.media_items[next_index])
        return self.media

    def play_next(self):
        now_index=None
        if self.play_list!=None:
            for i in range(len(self.play_list.media_items)):
                m=self.play_list.media_items[i]
                if m==self.media:
                    now_index=i
        if now_index==None:
            raise RuntimeError("media index not found")
        prev_index=(now_index+1)%len(self.play_list.media_items)
        self.play(self.play_list.media_items[prev_index])
        return self.media
    
    def play_prev(self):
        now_index=None
        if self.play_list!=None:
            for i in range(len(self.play_list.media_items)):
                m=self.play_list.media_items[i]
                if m==self.media:
                    now_index=i
        if now_index==None:
            raise RuntimeError("media index not found")
        prev_index=(len(self.play_list.media_items)+now_index-1)%len(self.play_list.media_items)
        self.play(self.play_list.media_items[prev_index])
        return self.media
    
    def get_current_media(self):
        return self.media
    
    def change_play_mode(self):
        if self.play_mode==PlayMode.SEQUENCE:
            self.play_mode=PlayMode.LOOP
        elif self.play_mode==PlayMode.LOOP:
            self.play_mode=PlayMode.RANDOM
        elif self.play_mode==PlayMode.RANDOM:
            self.play_mode=PlayMode.SEQUENCE
        return self.play_mode
