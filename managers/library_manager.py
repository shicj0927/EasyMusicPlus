from repositories.library_repository import LibraryRepository
from models.library import PlayList, Session
from models.media import MediaItem
import random

class LibraryManager:
    def __init__(self):
        self.repository = LibraryRepository()
        self.loaded=False
    
    def load_library(self, path: str):
        self.repository = LibraryRepository()
        try:
            self.repository.load_library(path)
            self.loaded=True
        except FileNotFoundError as e:
            print(f"Error loading library: {e}")
    
    def is_loaded(self):
        return self.loaded
    
    def get_playlists(self) -> list[PlayList]:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.library.play_lists

    def get_playlist(self, index: int) -> PlayList:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.library.play_lists[index]

    def get_media(self, songlistId: str, index: int) -> MediaItem:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        for pl in self.repository.library.play_lists:
            if pl.id==songlistId:
                return pl.media_items[index]
        raise RuntimeError("songlistId not found")
    
    def gen_new_playlist_id(self):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        ids=[pl.id for pl in self.repository.library.play_lists]
        chars="0123456789abcdefghijklmnopqrstuvwxyz"
        while True:
            new_id = ''.join(random.choice(chars) for _ in range(5))
            if new_id not in ids:
                return new_id
    
    def gen_new_media_id(self):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        ids=[]
        for pl in self.repository.library.play_lists:
            ids.extend([mi.id for mi in pl.media_items])
        chars="0123456789abcdefghijklmnopqrstuvwxyz"
        while True:
            new_id = ''.join(random.choice(chars) for _ in range(5))
            if new_id not in ids:
                return new_id

    def new_playlist(self, title: str):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        new_playlist = PlayList(id=self.gen_new_playlist_id(), title=title, media_items=[])
        self.repository.add_playlist(new_playlist)
    
    def remove_playlist(self, playlist_id: str):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        for pl in self.repository.library.play_lists:
            if pl.id == playlist_id:
                for m in pl.media_items:
                    self.repository.remove_from_playlist(playlist_id, m.id)
                self.repository.library.play_lists.remove(pl)
                self.repository.save_library()
                return
    
    def add_media_to_playlist(self, playlist_id: str, media):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        self.repository.insert_into_playlist(playlist_id, media)
    
    def remove_media_from_playlist(self, playlist_id: str, media_id: str):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        self.repository.remove_from_playlist(playlist_id, media_id)