from models.library import *

def upgrade_library_v10_to_v20(lib_v10: MediaLibrary_V10) -> MediaLibrary_V20:
    media_items=[]
    media_id_flags={}
    for pl in lib_v10.play_lists:
        for item in pl.media_items:
            if item.id not in media_id_flags:
                media_items.append(item)
                media_id_flags[item.id]=True
    media_data = MediaData_V20(media_items=media_items)
    play_lists = [
        PlayList_V20(
            id=pl.id,
            title=pl.title,
            media_ids=[item.id for item in pl.media_items]
        )
        for pl in lib_v10.play_lists
    ]
    return MediaLibrary_V20(
        master_folder=lib_v10.master_folder,
        play_lists=play_lists,
        media_data=media_data
    )