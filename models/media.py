from dataclasses import dataclass
from dataclasses import field

@dataclass
class AudioTrack:
    path: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class VideoTrack:
    path: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class LyricTrack:
    path: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class LyricLine:
    time_ms: int
    text: str

@dataclass
class Lyric:
    lines: list[LyricLine]=field(default_factory=list)

@dataclass
class MediaItem_V10:
    id: str=""
    title: str=""
    artists: list[str]=field(default_factory=list)
    source: str=""
    source_id: str=""
    url: str=""
    folder_path: str=""
    cover_path: str|None=None
    cover_url: str|None=None
    audio_track: AudioTrack|None=None
    video_track: VideoTrack|None=None
    lyric_track: LyricTrack|None=None

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            artists=data.get("artists", []),
            source=data.get("source", ""),
            source_id=data.get("source_id", ""),
            url=data.get("url", ""),
            cover_path=data.get("cover_path"),
            cover_url=data.get("cover_url"),
            audio_track=AudioTrack.from_dict(data["audio_track"])
            if data.get("audio_track") else None,
            video_track=VideoTrack.from_dict(data["video_track"])
            if data.get("video_track") else None,
            lyric_track=LyricTrack.from_dict(data["lyric_track"])
            if data.get("lyric_track") else None,
        )