from dataclasses import dataclass
from dataclasses import field
from models.media import MediaItem_V10

#################################V1.0#################################

@dataclass
class PlayList_V10:
    id: str
    title: str
    media_items: list[MediaItem_V10]
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            media_items=[
                MediaItem_V10.from_dict(m)
                for m in data.get("media_items", [])
            ]
        )

@dataclass
class Session_V10:
    last_played_media_id: str
    last_played_playlist_id: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class MediaLibrary_V10:
    master_folder: str
    version: str="1.0"
    play_lists: list[PlayList_V10]=field(default_factory=list)
    session: Session_V10|None=None

#################################V2.0#################################

@dataclass
class MediaData_V20:
    media_items: list[MediaItem_V10]=field(default_factory=list)

@dataclass
class PlayList_V20:
    id: str
    title: str
    media_ids: list[str]
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            media_ids=data.get("media_ids", [])
        )

@dataclass
class MediaLibrary_V20:
    master_folder: str
    version: str="2.0"
    media_data: MediaData_V20=field(default_factory=MediaData_V20)
    play_lists: list[PlayList_V20]=field(default_factory=list)
