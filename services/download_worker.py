import requests
import re
import urllib.parse
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtCore import QThread
import os
from services.utils import safe_file_name
from yt_dlp import YoutubeDL


class DownloadWorker(QObject):
    downloadFinishedSignal = pyqtSignal(object)
    downloadLogSingnal = pyqtSignal(str)
    parseResultSignal = pyqtSignal(object)
    procressUpdateSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot(object, str, str, str)
    def download(self, songData, url, mediaId, path):
        bilibiliHtmlCache=""
        neteaseHtmlCache={}
        print(f"download: {songData}, {url}, {mediaId}, {path}")
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/135.0.0.0 Safari/537.36"
            )
        }
        if songData==None or songData=={}:
            songData={}
            if url==None or url=="":
                if mediaId==None or mediaId=="":
                    self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：缺少必要参数"})
                    return
                else:
                    songData["id"]=mediaId
                    if mediaId.startswith("BV"):
                        songData["source"]="bilibili"
                    else:
                        songData["source"]="netease"
            else:
                urlData=urllib.parse.urlparse(url)
                #https://www.bilibili.com/video/BV1rwAEzyET2/?spm_id_from=333.337.search-card.all.click
                if "bilibili.com" in urlData.netloc:
                    songData["source"]="bilibili"
                    pathParts=urlData.path.split("/")
                    for part in pathParts:
                        if part.startswith("BV"):
                            songData["id"]=part
                            break
                    if "BV" not in songData["id"]:
                        self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：无法从URL中提取媒体ID"})
                        return
                elif "music.163.com" in urlData.netloc:
                    #https://music.163.com/#/song?id=3345742920
                    songData["source"]="netease"
                    fragment=urlData.fragment
                    # /song?id=3345742920 -> id=3345742920
                    fragment=fragment.replace("/song?", "")
                    queryParts=urllib.parse.parse_qs(fragment)
                    if "id" in queryParts and len(queryParts["id"])>0:
                        songData["id"]=queryParts["id"][0]
                    else:
                        self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：无法从URL中提取媒体ID"})
                        return
                else:
                    self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：不支持的URL"})
                    return
            self.downloadLogSingnal.emit(f"提取到媒体ID：{songData['id']}，来源：{songData['source']}")
            # 请求title和artist等信息
            if songData["source"]=="bilibili":
                songData["url"]="https://www.bilibili.com/video/"+songData["id"]
                headers["Referer"]="https://www.bilibili.com/"
                for i in range(5):
                    resp=requests.get(songData["url"], headers=headers)
                    if resp.status_code==200:
                        break
                if resp.status_code!=200:
                    self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：无法访问B站视频页面"})
                    return
                html = resp.text
                bilibiliHtmlCache=html
                title = re.search(r"<h1 data-title=\"(.*?)\" title=\"(.*?)\" class=\"video-title special-text-indent\" data-v-fe6ec38e>", html).group(1)
                songData["title"]=title
                artist=re.search(r"<meta data-vue-meta=\"true\" itemprop=\"author\" name=\"author\" content=\"(.*?)\">", html).group(1)
                songData["artists"]=[artist]
            elif songData["source"]=="netease":
                songData["url"]="https://music.163.com/api/song/detail/?ids=["+songData["id"]+"]"
                headers["Referer"]="https://music.163.com/"
                for i in range(5):
                    resp=requests.get(songData["url"], headers=headers)
                    if resp.status_code==200:
                        break
                if resp.status_code!=200:
                    self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：无法访问网易云音乐页面"})
                    return
                dat = resp.json()
                neteaseHtmlCache=dat
                songData["title"]=dat["songs"][0]["name"]
                songData["artists"]=[ar["name"] for ar in dat["songs"][0]["artists"]]
            self.downloadLogSingnal.emit(f"获取到歌曲名称：{songData['title']} - {', '.join(songData['artists'])}")
        else:
            # 为songData补全url等字段
            if songData["source"]=="bilibili":
                songData["url"]="https://www.bilibili.com/video/"+songData["id"]
            elif songData["source"]=="netease":
                songData["url"]="https://music.163.com/api/song/detail/?ids=["+songData["id"]+"]"
            tmp={"id":songData["id"], "source":songData["source"], "title":songData.get("name",""), "artists":songData.get("artist",[]), "url":songData["url"]}
            songData=tmp
            self.downloadLogSingnal.emit(f"使用提供的歌曲信息，名称：{songData['title']} - {', '.join(songData['artists'])}")
        # 此时包含 url, id, source, title, artists等信息
        # 补齐封面
        if songData["source"]=="bilibili":
            if bilibiliHtmlCache=="":
                headers["Referer"]="https://www.bilibili.com/"
                for i in range(5):
                    resp=requests.get(songData["url"], headers=headers)
                    if resp.status_code==200:
                        break
                if resp.status_code!=200:
                    self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：无法访问B站视频页面"})
                    return
                bilibiliHtmlCache = resp.text
            songData["cover"]="https:"+re.search(r"<meta data-vue-meta=\"true\" property=\"og:image\" content=\"(.*?)@100w_100h_1c", bilibiliHtmlCache).group(1)
        elif songData["source"]=="netease":
            if neteaseHtmlCache=={}:
                headers["Referer"]="https://music.163.com/"
                for i in range(5):
                    resp=requests.get(songData["url"], headers=headers)
                    if resp.status_code==200:
                        break
                if resp.status_code!=200:
                    self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：无法访问网易云音乐页面"})
                    return
                neteaseHtmlCache = resp.json()
            try:
                songData["cover"]=neteaseHtmlCache["songs"][0]["album"]["picUrl"]
            except:
                songData["cover"]=""
            # print("neteaseHtmlCache:", neteaseHtmlCache)
        self.downloadLogSingnal.emit(f"获取到歌曲封面：{songData['cover']}")
        # 此时songData应该包含 id, source, title, artists, url, cover等信息
        self.downloadLogSingnal.emit(f"准备开始下载……")
        self.parseResultSignal.emit(songData)
        # 下载歌曲封面
        # 检查目录是否存在
        if not os.path.exists(path):
            os.makedirs(path)
        path=os.path.join(path, safe_file_name(f"{songData['title']} - {', '.join(songData['artists'])}"))
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            response = requests.get(songData["cover"], headers=headers)
            if response.status_code == 200:
                coverPath = os.path.join(path, safe_file_name(f"{songData['title']} - {', '.join(songData['artists'])}.jpg"))
                with open(coverPath, 'wb') as f:
                    f.write(response.content)
                self.downloadLogSingnal.emit(f"封面下载完成，保存路径：{coverPath}")
        except Exception as e:
            self.downloadLogSingnal.emit(f"封面下载失败：{str(e)}")
        # 开始下载
        if songData["source"]=="bilibili":
            def hook(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    downloaded = d.get('downloaded_bytes', 0)
                    if total > 0:
                        progress = int(downloaded / total * 100)
                        self.procressUpdateSignal.emit(progress)
                elif d['status'] == 'finished':
                    self.procressUpdateSignal.emit(100)
            ydl_opts = {
                'format': 'bestvideo[vcodec*=avc1]+bestaudio/best',
                'outtmpl': os.path.join(path, safe_file_name(f"{songData['title']} - {', '.join(songData['artists'])}.%(ext)s")),
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [hook]
            }
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([songData["url"]])
                self.downloadFinishedSignal.emit({"status":"success","message":f"下载完成，保存路径：{path}"})
            except Exception as e:
                self.downloadFinishedSignal.emit({"status":"error","message":f"下载失败：{str(e)}"})
        elif songData["source"]=="netease":
            # 下载歌词
            # https://music-api.gdstudio.xyz/api.php?types=lyric&source=[MUSIC SOURCE]&id=[LYRIC ID]
            lyricUrl = f"https://music-api.gdstudio.xyz/api.php?types=lyric&source=netease&id={songData['id']}"
            for i in range(5):
                resp=requests.get(lyricUrl, headers=headers)
                if resp.status_code==200 and resp.json()!=None and resp.json()!=[]:
                    break
            if resp.status_code==200 and resp.json()!=None and resp.json()!=[]:
                lyricData=resp.json()
                if "lyric" in lyricData:
                    lyricContent=lyricData["lyric"]
                    lyricPath=os.path.join(path, safe_file_name(f"{songData['title']} - {', '.join(songData['artists'])}.lrc"))
                    with open(lyricPath, 'w', encoding='utf-8') as f:
                        f.write(lyricContent)
                    self.downloadLogSingnal.emit(f"歌词下载完成，保存路径：{lyricPath}")
                else:
                    self.downloadLogSingnal.emit("未找到歌词信息")
            else:
                self.downloadLogSingnal.emit("歌词下载失败：无法获取歌词信息")
            # https://music-api.gdstudio.xyz/api.php?types=url&source=[MUSIC SOURCE]&id=[TRACK ID]&br=[128/192/320/740/999]
            url = f"https://music-api.gdstudio.xyz/api.php?types=url&source=netease&id={songData['id']}&br=320"
            for i in range(5):
                resp=requests.get(url, headers=headers)
                if resp.status_code==200 and resp.json()!=None and resp.json()!=[]:
                    break
            if resp.status_code!=200 or resp.json()==None or resp.json()==[]:
                self.downloadFinishedSignal.emit({"status":"error","message":"下载失败：无法获取网易云音乐下载链接"})
                return
            downloadUrl=resp.json()["url"]
            self.downloadLogSingnal.emit(f"获取到下载链接：{downloadUrl}")
            # 开始下载到本地
            # 生成安全的文件名
            fileName=safe_file_name(f"{songData['title']} - {', '.join(songData['artists'])}.mp3")
            filePath=os.path.join(path, fileName)
            try:
                with requests.get(downloadUrl, headers=headers, stream=True) as r:
                    r.raise_for_status()
                    total_length = int(r.headers.get('content-length', 0))
                    downloaded_length = 0
                    with open(filePath, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded_length += len(chunk)
                                progress = int(downloaded_length / total_length * 100)
                                self.procressUpdateSignal.emit(progress)
                self.downloadFinishedSignal.emit({"status":"success","message":f"下载完成，保存路径：{filePath}"})
            except Exception as e:
                self.downloadFinishedSignal.emit({"status":"error","message":f"下载失败：{str(e)}"})