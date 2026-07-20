from repositories.library_repository import LibraryRepository
from models.library import PlayList_V20
from models.media import MediaItem_V10
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
    
    def get_playlists(self) -> list[PlayList_V20]:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.get_playlists()

    def get_playlist_by_index(self, index: int) -> PlayList_V20:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.get_playlists()[index]

    def get_playlist_by_id(self, id: str) -> PlayList_V20:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.get_playlist(id)

    def get_media_by_index(self, songlistId: str, index: int) -> MediaItem_V10:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.get_media(self.repository.get_playlist(songlistId).media_ids[index])

    def get_media_by_id(self, mediaId: str) -> MediaItem_V10:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.get_media(mediaId)
    
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
        ids=[m.id for m in self.repository.library.media_data.media_items]
        chars="0123456789abcdefghijklmnopqrstuvwxyz"
        while True:
            new_id = ''.join(random.choice(chars) for _ in range(5))
            if new_id not in ids:
                return new_id

    def new_playlist(self, title: str):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        new_playlist = PlayList_V20(id=self.gen_new_playlist_id(), title=title, media_ids=[])
        self.repository.add_playlist(new_playlist)
    
    def rename_playlist(self, playlist_id: str, title: str):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        self.repository.rename_playlist(playlist_id,title)
    
    def remove_playlist(self, playlist_id: str):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        if playlist_id=="-----":
            raise RuntimeError("Unable to delete -----")
        for pl in self.repository.library.play_lists:
            if pl.id == playlist_id:
                for m in pl.media_ids:
                    self.repository.remove_from_playlist(playlist_id, m)
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
    
    def remove_mdeia_from_data(self, media_id: str):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        self.repository.remove_from_data(media_id)

    def check_remove_influence(self, media_id: str) -> list[str]:
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        return self.repository.check_remove_influence(media_id)
    
    def change_playlists_order(self, new_order: list[str]):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        self.repository.change_playlists_order(new_order)
    
    def change_medias_order(self, playlist_id: str, new_order: list[str]):
        if not self.loaded:
            raise RuntimeError("Library not loaded")
        self.repository.change_medias_order(playlist_id, new_order)