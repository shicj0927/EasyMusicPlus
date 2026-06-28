import requests
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import traceback
from config import *
import re

'''
此api应当返回[name,artist[],id]
'''

class SearchWorker(QObject):
    searchFinishedSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot(str, str, int, int)
    def search(self, keyword, source, page_length=20, page_num=1):
        # print(requests.get("https://music-api.gdstudio.xyz/api.php?types=search&source=netease&name=t&count=60&pages=1"))
        try:
            print(f"search: {keyword} from {source}")
            if source=="netease":
                url=API_BASE+"/search?name="+keyword
                for _ in range(5):
                    try:
                        resp=requests.get(url,timeout=5)
                        print("STATUS:", resp.status_code)
                        print("TEXT:", resp.text[:300])
                        dat = resp.json()
                        result=[]
                        for i in dat["result"]["songs"]:
                            tmp={}
                            tmp["source"]="netease"
                            tmp["name"]=i["name"]
                            artmp=[]
                            for j in i["ar"]:
                                artmp.append(j["name"])
                            tmp["artist"]=artmp
                            tmp["id"]=str(i["id"])
                            result.append(tmp)
                        print(result)
                        self.searchFinishedSignal.emit(result)
                        return
                    except:
                        traceback.print_exc()
            else:
                url="https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword="+keyword+"&page=1"
                for _ in range(5):
                    try:
                        headers={
                            "User-Agent": USER_AGENT,
                            "Referer": "https://www.bilibili.com/"
                        }
                        dat=requests.get(url,timeout=5,headers=headers).json()
                        result=[]
                        for i in dat["data"]["result"]:
                            tmp={}
                            tmp["source"]="bilibili"
                            tmp["name"]=i["title"]
                            tmp["artist"]=[i["author"]]
                            tmp["id"]=i["bvid"]
                            tmp["name"]= re.sub(r'<em class="keyword">|</em>','',tmp["name"])
                            result.append(tmp)
                        print(result)
                        self.searchFinishedSignal.emit(result)
                        return
                    except:
                        traceback.print_exc()
        except Exception as e:
            traceback.print_exc()