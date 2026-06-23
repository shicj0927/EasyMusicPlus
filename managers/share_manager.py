from res.templates.share_html import get_share_html
from models.library import PlayList_V20,MediaItem_V10
from managers.library_manager import LibraryManager
import json

def gen_music_link(music:MediaItem_V10):
    if music.source=="netease":
        return {
            "name":"网易云",
            "url":f"https://music.163.com/#/song?id={music.source_id}"
        }
    elif music.source=="bilibili":
        return {
            "name":"Bilibili",
            "url":f"https://www.bilibili.com/video/{music.source_id}"
        }
    else:
        return {
            "name":"未知来源",
            "url":"#"
        }

def get_share_json(library_manager: LibraryManager, playlist_id: str, title: str):
    play_list = library_manager.get_playlist_by_id(playlist_id)
    data = {
        "title": title,
        "list": []
    }
    for music_id in play_list.media_ids:
        music = library_manager.get_media_by_id(music_id)
        item = {
            "name": music.title,
            "artist": ", ".join(music.artists),
            "link": gen_music_link(music)
        }
        data["list"].append(item)
    json_data = json.dumps(data, ensure_ascii=False)
    return json_data

def save_share_html(library_manager: LibraryManager, playlist_id: str, title: str, file_path: str):
    json_data = get_share_json(library_manager, playlist_id, title)
    html_content = get_share_html(json_data)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)