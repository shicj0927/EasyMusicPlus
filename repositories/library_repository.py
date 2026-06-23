import json
from models.library import *
from repositories.library_updater import upgrade_library_v10_to_v20
from models.media import MediaItem_V10, AudioTrack, VideoTrack, LyricTrack
from dataclasses import asdict
import shutil
import os

class LibraryRepository:
    def __init__(self):
        self.library: MediaLibrary_V20 = MediaLibrary_V20(master_folder="")
    
    def load_library(self, path: str):
        self.library.master_folder = path
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        json_path = os.path.join(path, "library.json")
        if not os.path.exists(json_path):
            with open(json_path, "w") as f:
                json.dump({
                    "version": "2.0",
                    "media_data": {
                        "media_items": []
                    },
                    "play_lists": []
                }, f)
        with open(json_path, "r") as f:
            data = json.load(f)
        if data.get("version") == "1.0":
            library_V10=MediaLibrary_V10(master_folder=path)
            library_V10.play_lists = [
                PlayList_V10.from_dict(pl)
                for pl in data.get("play_lists", [])
            ]
            session_data = data.get("session")
            library_V10.session = (
                Session_V10.from_dict(session_data)
                if session_data else None
            )
            self.library = upgrade_library_v10_to_v20(library_V10)
            self.save_library()
        elif data.get("version") == "2.0":
            self.library.play_lists = [
                PlayList_V20.from_dict(pl)
                for pl in data.get("play_lists", [])
            ]
            media_items = data.get("media_data", {}).get("media_items", [])
            self.library.media_data.media_items = [
                MediaItem_V10.from_dict(m)
                for m in media_items
            ]
        print(f"Library loaded from {json_path}")
        print(f"Library data: {self.library}")
    
    def save_library(self):
        if not self.library.master_folder:
            raise ValueError("Master folder is not set")
        data = {
            "version": "2.0",
            "media_data": {
                "media_items": [asdict(m) for m in self.library.media_data.media_items]
            },
            "play_lists": [
                asdict(pl)
                for pl in self.library.play_lists
            ]
        }
        print(f"Saving library to {os.path.join(self.library.master_folder, 'library.json')}")
        print(f"Library data: {data}")
        with open(os.path.join(self.library.master_folder, "library.json"), "w") as f:
            json.dump(data, f, indent=4)
    
    def add_playlist(self, playlist: PlayList_V20):
        self.library.play_lists.append(playlist)
        self.save_library()
    
    def remove_playlist(self, playlist_id: str):
        for pl in self.library.play_lists:
            if pl.id == playlist_id:
                self.library.play_lists.remove(pl)
                self.save_library()
                return
        raise ValueError(f"Playlist {playlist_id} not found")

    def update_playlists(self, playlists: list):
        self.library.play_lists=playlists
        self.save_library()

    def insert_into_playlist(self, playlist_id: str, media: MediaItem_V10):
        is_saved=False
        for m in self.library.media_data.media_items:
            if (m.source,m.source_id,m.url) == (media.source,media.source_id,media.url):
                is_saved=True
                break
        if not is_saved:
            self.library.media_data.media_items.append(media)
        if playlist_id=="-----":
            self.save_library()
            return
        for pl in self.library.play_lists:
            if pl.id == playlist_id:
                pl.media_ids.append(media.id)
                self.save_library()
                return
        raise ValueError(f"Playlist {playlist_id} not found")
    
    def remove_from_playlist(self, playlist_id: str, media_id: str):
        print(f"removing {media_id} from {playlist_id}")
        if playlist_id=="-----":
            # remove from all playlists
            self.remove_from_data(media_id)
            return
        media=None
        for pl in self.library.play_lists:
            if pl.id == playlist_id:
                try:
                    pl.media_ids.remove(media_id)
                    self.save_library()
                    return
                except:
                    raise ValueError(f"Media {media_id} not found in playlist {playlist_id}")
        raise ValueError(f"Playlist {playlist_id} not found")

    def remove_from_data(self, media_id: str):
        print(f"removing {media_id} from data")
        media=None
        for m in self.library.media_data.media_items:
            if m.id == media_id:
                media=m
                break
        if media:
            for pl in self.library.play_lists:
                if media_id in pl.media_ids:
                    pl.media_ids.remove(media_id)
            self.library.media_data.media_items.remove(media)
            self.save_library()
            os.remove(media.audio_track.path) if media.audio_track else None
            os.remove(media.video_track.path) if media.video_track else None
            os.remove(media.lyric_track.path) if media.lyric_track else None
            os.remove(media.cover_path) if media.cover_path else None
            os.removedirs(media.folder_path) if media.folder_path else None
            return
        else:
            raise ValueError(f"Media {media_id} not found in data")
        
    def check_remove_influence(self, media_id: str) -> list[str]:
        influence=[]
        for pl in self.library.play_lists:
            if media_id in pl.media_ids:
                influence.append(pl.title)
        return influence

    def get_media(self, media_id: str) -> MediaItem_V10:
        for m in self.library.media_data.media_items:
            if m.id == media_id:
                return m
        raise ValueError(f"Media {media_id} not found in data")
    
    def get_playlist(self, playlist_id: str) -> PlayList_V20:
        if playlist_id=="-----":
            # return all data as list
            return PlayList_V20(
                id="-----",
                title="全部音乐",
                media_ids=[m.id for m in self.library.media_data.media_items]
            )
        for pl in self.library.play_lists:
            if pl.id == playlist_id:
                return pl
        raise ValueError(f"Playlist {playlist_id} not found")
    
    def get_playlists(self) -> list[PlayList_V20]:
        result=[self.get_playlist("-----")]
        for pl in self.library.play_lists:
            result.append(pl)
        return result
    
    def get_data(self) -> MediaData_V20:
        return self.library.media_data
    
    def change_playlists_order(self, new_order: list[str]):
        tmp=new_order.copy()
        if "-----" in tmp:
            tmp.remove("-----")
        if sorted(tmp) != sorted([pl.id for pl in self.library.play_lists]):
            raise ValueError("New order does not match existing playlists")
        id_to_pl={pl.id: pl for pl in self.library.play_lists}
        new_playlists=[id_to_pl[pl_id] for pl_id in tmp]
        self.library.play_lists=new_playlists
        self.save_library()
    
    def change_medias_order(self, playlist_id: str, new_order: list[str]):
        pl=self.get_playlist(playlist_id)
        if sorted(new_order) != sorted(pl.media_ids):
            raise ValueError("New order does not match existing media ids in playlist")
        pl.media_ids=new_order
        self.save_library()