import requests
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import traceback
import api.netease as neteaseAPI
import config, re


class SearchListWorker(QObject):
    searchFinishedSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str, int, int)
    def search_list(self, keyword, source, page_length=60, page_num=1):
        try:
            print(f"search: {keyword} from {source}")
            for _ in range(5):
                try:
                    json = neteaseAPI.search_list(keyword, page_length, page_num)
                    if json == None or json == {} or json == "":
                        raise ValueError("Empty response")
                    dat = json
                    # print(dat)
                    # {'result': {'searchQcReminder': None, 'playlists': [{'id': 10103602289, 'name': '邓紫棋IAG2.0演唱会歌单（2026顺序版）', 'coverImgUrl': 'http://p1.music.126.net/bHSEZzN-Dr62mz5-T8eogg==/109951171495533706.jpg', 'creator': {'nickname': '紫叶枫辰_', 'userId': 291817750, 'userType': 0, 'avatarUrl': None, 'authStatus': 0, 'expertTags': None, 'experts': None}, 'subscribed': False, 'trackCount': 58, 'userId': 291817750, 'playCount': 2020350, 'bookCount': 24953, 'specialType': 0, 'officialTags': None, 'action': None, 'actionType': None, 'recommendText': None, 'score': None, 'officialPlaylistTitle': None, 'playlistType': 'UGC', 'description': '\n1-35为固定曲目 35-57为点唱环节高频曲目', 'highQuality': False}, {'id': 2488306802, 'name': '邓紫棋热门单曲', 'coverImgUrl': 'http://p1.music.126.net/fkqFqMaEt0CzxYS-0NpCog==/18587244069235039.jpg', 'creator': {'nickname': 'Master-辰曜', 'userId': 1298326298, 'userType': 0, 'avatarUrl': None, 'authStatus': 0, 'expertTags': None, 'experts': None}, 'subscribed': False, 'trackCount': 49, 'userId': 1298326298, 'playCount': 9543226, 'bookCount': 88415, 'specialType': 0, 'officialTags': None, 'action': None, 'actionType': None, 'recommendText': None, 'score': None, 'officialPlaylistTitle': None, 'playlistType': 'UGC', 'description': None, 'highQuality': False}], 'playlistCount': 400}, 'code': 200}
                    result = []
                    for i in dat["result"]["playlists"]:
                        tmp = {}
                        tmp["name"] = i["name"]
                        tmp["id"] = str(i["id"])
                        result.append(tmp)
                    print(result)
                    self.searchFinishedSignal.emit(result)
                    return
                except:
                    traceback.print_exc()
        except Exception as e:
            traceback.print_exc()


"""
Example
{
    'result': {
        'searchQcReminder': None,
        'playlists': [
            {
                'id': 10103602289,
                'name': '邓紫棋IAG2.0演唱会歌单（2026顺序版）',
                'coverImgUrl': 'http://p1.music.126.net/bHSEZzN-Dr62mz5-T8eogg==/109951171495533706.jpg',
                'creator': {
                    'nickname': '紫叶枫辰_',
                    'userId': 291817750,
                    'userType': 0,
                    'avatarUrl': None,
                    'authStatus': 0,
                    'expertTags': None,
                    'experts': None
                },
                'subscribed': False,
                'trackCount': 58,
                'userId': 291817750,
                'playCount': 2020350,
                'bookCount': 24953,
                'specialType': 0,
                'officialTags': None,
                'action': None,
                'actionType': None,
                'recommendText': None,
                'score': None,
                'officialPlaylistTitle': None,
                'playlistType': 'UGC',
                'description': '\n1-35为固定曲目 35-57为点唱环节高频曲目',
                'highQuality': False
            },
            {
                'id': 2488306802,
                'name': '邓紫棋热门单曲',
                'coverImgUrl': 'http://p1.music.126.net/fkqFqMaEt0CzxYS-0NpCog==/18587244069235039.jpg',
                'creator': {
                    'nickname': 'Master-辰曜',
                    'userId': 1298326298,
                    'userType': 0,
                    'avatarUrl': None,
                    'authStatus': 0,
                    'expertTags': None,
                    'experts': None
                },
                'subscribed': False,
                'trackCount': 49,
                'userId': 1298326298,
                'playCount': 9543226,
                'bookCount': 88415,
                'specialType': 0,
                'officialTags': None,
                'action': None,
                'actionType': None,
                'recommendText': None,
                'score': None,
                'officialPlaylistTitle': None,
                'officialPlaylistTitle': None,
                'playlistType': 'UGC',
                'description': None,
                'highQuality': False
            }
        ],
        'playlistCount': 400
    },
    'code': 200
}
"""
