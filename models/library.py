from dataclasses import dataclass
from dataclasses import field
from models.media import MediaItem

@dataclass
class PlayList:
    id: str
    title: str
    media_items: list[MediaItem]
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            media_items=[
                MediaItem.from_dict(m)
                for m in data.get("media_items", [])
            ]
        )

@dataclass
class Session:
    last_played_media_id: str
    last_played_playlist_id: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class MediaLibrary:
    master_folder: str
    play_lists: list[PlayList]=field(default_factory=list)
    session: Session|None=None