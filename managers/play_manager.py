from managers.player_manager import PlayerManager,PlayerState
from managers.lyric_manager import LyricManager
from managers.library_manager import LibraryManager
from models.media import MediaItem_V10
from PyQt6.QtCore import QObject, pyqtSignal
import random
from enum import Enum

class PlayMode(Enum):
    SEQUENCE = 0
    LOOP = 1
    RANDOM = 2

class PlayManager(QObject):
    lyricChangedSignal=pyqtSignal(int)

    def __init__(self,widget,library_manager:LibraryManager):
        super().__init__()
        self.media=None
        self.playerManager=PlayerManager(widget)
        self.lyricManager=LyricManager()
        self.play_mode=PlayMode.SEQUENCE
        self.play_list_id=None
        self.library_manager=library_manager
        self.playerManager.positionChangedSignal.connect(self.on_position_changed)
    
    def check_type(self,media:MediaItem_V10) -> str:
        if media.video_track!=None:
            return "video"
        else:
            return "audio"
    
    def on_position_changed(self,time_s):
        time_ms=int(time_s*1000)
        self.lyricChangedSignal.emit(self.lyricManager.get_current_lyric_index(time_ms))
    
    def play(self,media:MediaItem_V10,play_list_id=None):
        self.media=media
        if play_list_id!=None:
            self.play_list_id=play_list_id
        if media.lyric_track!=None:
            self.lyricManager.load(media.lyric_track.path)
        if media.video_track!=None:
            self.playerManager.play(media.video_track.path)
        else:
            self.playerManager.play(media.audio_track.path)
    
    def auto_play_next(self):
        # self.playerManager.lock_switching()
        now_index=None
        if self.play_list_id!=None:
            play_list=self.library_manager.get_playlist_by_id(self.play_list_id)
            for i in range(len(play_list.media_ids)):
                m=self.library_manager.get_media_by_id(play_list.media_ids[i])
                if m==self.media:
                    now_index=i
        if self.play_mode==PlayMode.LOOP:
            self.play(self.media)
        elif self.play_mode==PlayMode.SEQUENCE:
            if now_index==None:
                raise RuntimeError("media index not found")
            next_index=(now_index+1)%len(play_list.media_ids)
            self.play(self.library_manager.get_media_by_id(play_list.media_ids[next_index]))
        else:
            if now_index==None:
                raise RuntimeError("media index not found")
            next_index=random.randint(0,len(play_list.media_ids)-1)
            self.play(self.library_manager.get_media_by_id(play_list.media_ids[next_index]))
        return self.media

    def play_next(self):
        now_index=None
        if self.play_list_id!=None:
            play_list=self.library_manager.get_playlist_by_id(self.play_list_id)
            for i in range(len(play_list.media_ids)):
                m=self.library_manager.get_media_by_id(play_list.media_ids[i])
                if m==self.media:
                    now_index=i
        if now_index==None:
            raise RuntimeError("media index not found")
        prev_index=(now_index+1)%len(play_list.media_ids)
        self.play(self.library_manager.get_media_by_id(play_list.media_ids[prev_index]))
        return self.media
    
    def play_prev(self):
        now_index=None
        if self.play_list_id!=None:
            play_list=self.library_manager.get_playlist_by_id(self.play_list_id)
            for i in range(len(play_list.media_ids)):
                m=self.library_manager.get_media_by_id(play_list.media_ids[i])
                if m==self.media:
                    now_index=i
        if now_index==None:
            raise RuntimeError("media index not found")
        prev_index=(len(play_list.media_ids)+now_index-1)%len(play_list.media_ids)
        self.play(self.library_manager.get_media_by_id(play_list.media_ids[prev_index]))
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
