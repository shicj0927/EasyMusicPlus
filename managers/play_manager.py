from managers.player_manager import PlayerManager,PlayerState
from models.media import MediaItem
import os

class PlayManager:
    def __init__(self,widget):
        self.playerManager=PlayerManager(widget)
    
    def check_type(self,media:MediaItem) -> str:
        if media.video_track!=None:
            return "video"
        else:
            return "audio"
    
    def play(self,media:MediaItem):
        if media.video_track!=None:
            self.playerManager.play(media.video_track.path)
        else:
            self.playerManager.play(media.audio_track.path)
    
