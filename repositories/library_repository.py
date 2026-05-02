import json
from models.library import MediaLibrary, PlayList, Session
from models.media import MediaItem, AudioTrack, VideoTrack, LyricTrack
from dataclasses import asdict
import shutil
import os

class LibraryRepository:
    def __init__(self):
        self.library: MediaLibrary = MediaLibrary(master_folder="")
    
    def load_library(self, path: str):
        self.library.master_folder = path
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        json_path = os.path.join(path, "library.json")
        if not os.path.exists(json_path):
            with open(json_path, "w") as f:
                json.dump({
                    "play_lists": [],
                    "session": None
                }, f)
        with open(json_path, "r") as f:
            data = json.load(f)
        self.library.play_lists = [
            PlayList.from_dict(pl)
            for pl in data.get("play_lists", [])
        ]
        session_data = data.get("session")
        self.library.session = (
            Session.from_dict(session_data)
            if session_data else None
        )
    
    def save_library(self):
        if not self.library.master_folder:
            raise ValueError("Master folder is not set")
        data = {
            "play_lists": [
                asdict(pl)
                for pl in self.library.play_lists
            ],
            "session": (
                asdict(self.library.session)
                if self.library.session
                else None
            )
        }
        print(f"Saving library to {os.path.join(self.library.master_folder, 'library.json')}")
        print(f"Library data: {data}")
        with open(os.path.join(self.library.master_folder, "library.json"), "w") as f:
            json.dump(data, f, indent=4)
    
    def add_playlist(self, playlist: PlayList):
        self.library.play_lists.append(playlist)
        self.save_library()
    
    def update_session(self, session: Session):
        self.library.session = session
        self.save_library()
    
    def update_playlists(self, playlists: list):
        self.library.play_lists=playlists
        self.save_library()

    def insert_into_playlist(self, playlist_id: str, media: MediaItem):
        for pl in self.library.play_lists:
            if pl.id == playlist_id:
                pl.media_items.append(media)
                self.save_library()
                return
        raise ValueError(f"Playlist {playlist_id} not found")

    def remove_from_playlist(self, playlist_id: str, media_id: str):
        print(f"removing {media_id} from {playlist_id}")
        media=None
        for pl in self.library.play_lists:
            if pl.id == playlist_id:
                for m in pl.media_items:
                    if m.id == media_id:
                        media=m
                        break
                if media:
                    pl.media_items.remove(media)
                    self.save_library()
                    os.remove(media.audio_track.path) if media.audio_track else None
                    os.remove(media.video_track.path) if media.video_track else None
                    os.remove(media.lyric_track.path) if media.lyric_track else None
                    os.remove(media.cover_path) if media.cover_path else None
                    os.removedirs(media.folder_path) if media.folder_path else None
                    return
                else:
                    raise ValueError(f"Media {media_id} not found in playlist {playlist_id}")
        raise ValueError(f"Playlist {playlist_id} not found")