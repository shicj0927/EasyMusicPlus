import json
from models.library import MediaLibrary, PlayList, Session
from models.media import MediaItem, AudioTrack, VideoTrack, LyricTrack
from utils import get_rel_path
import os

def download_result_to_media_item(download_result: dict, id: str) -> MediaItem:
    return MediaItem(
        id=id,
        source_id=download_result["id"],
        title=download_result["title"],
        artists=download_result["artists"],
        source=download_result["source"],
        url=download_result["url"],
        folder_path=get_rel_path(download_result["folder_path"]),
        cover_url=download_result["cover_url"],
        cover_path=get_rel_path(download_result["cover_path"]),
        audio_track=AudioTrack(path=get_rel_path(download_result["audio_path"])) if download_result["audio_path"] is not None and os.path.exists(download_result["audio_path"]) else None,
        video_track=VideoTrack(path=get_rel_path(download_result["video_path"])) if download_result["video_path"] is not None and os.path.exists(download_result["video_path"]) else None,
        lyric_track=LyricTrack(path=get_rel_path(download_result["lyric_path"])) if download_result["lyric_path"] is not None and os.path.exists(download_result["lyric_path"]) else None
    )