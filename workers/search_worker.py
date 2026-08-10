import requests
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import traceback
import api.netease as neteaseAPI
import config

class SearchWorker(QObject):
    searchFinishedSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot(str, str, int, int)
    def search(self, keyword, source, page_length=20, page_num=1):
        # 旧实现方法，使用gdstudio API，速度慢，已弃用
        # print(requests.get("https://music-api.gdstudio.xyz/api.php?types=search&source=netease&name=t&count=60&pages=1"))
        try:
            print(f"search: {keyword} from {source}")
            url = f"https://music-api.gdstudio.xyz/api.php?types=search&source={source}&name={keyword}&count={page_length}&pages={page_num}"
            i=1
            while i<=8:
                print(f"Attempt {i} to fetch data from {url}")
                response = requests.get(url, timeout=5)
                print(response)
                if response.status_code == 200 and response.json()!=None and response.json()!=[]:
                    self.searchFinishedSignal.emit(response.json())
                    return
                i+=1
            self.searchFinishedSignal.emit(None)
        except Exception as e:
            traceback.print_exc()
        # 死于风控
        # try:
        #     print(f"search: {keyword} from {source}")
        #     if source=="netease":
        #         # url=API_BASE+"/search?name="+keyword
        #         for _ in range(5):
        #             try:
        #                 json=neteaseAPI.search(keyword,60,1)
        #                 if json==None or json=={} or json=="":
        #                     raise ValueError("Empty response")
        #                 dat=json
        #                 # print(dat)
        #                 result=[]
        #                 for i in dat["result"]["songs"]:
        #                     tmp={}
        #                     tmp["source"]="netease"
        #                     tmp["name"]=i["name"]
        #                     artmp=[]
        #                     for j in i["ar"]:
        #                         artmp.append(j["name"])
        #                     tmp["artist"]=artmp
        #                     tmp["id"]=str(i["id"])
        #                     result.append(tmp)
        #                 print(result)
        #                 self.searchFinishedSignal.emit(result)
        #                 return
        #             except:
        #                 traceback.print_exc()
        #     else:
        #         url="https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword="+keyword+"&page=1"
        #         headers = {
        #             "User-Agent": config.USER_AGENT,
        #             "Referer": "https://www.bilibili.com/",
        #             "Origin": "https://www.bilibili.com",
        #             "Accept": "application/json, text/plain, */*",
        #             "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        #         }
        #         for _ in range(5):
        #             try:
        #                 print(url)
        #                 dat=requests.get(url,timeout=5,headers=headers).json()
        #                 result=[]
        #                 print(result)
        #                 for i in dat["data"]["result"]:
        #                     tmp={}
        #                     tmp["source"]="bilibili"
        #                     tmp["name"]=i["title"]
        #                     tmp["artist"]=[i["author"]]
        #                     tmp["id"]=i["bvid"]
        #                     tmp["name"]= re.sub(r'<em class="keyword">|</em>','',tmp["name"])
        #                     result.append(tmp)
        #                 print(result)
        #                 self.searchFinishedSignal.emit(result)
        #                 return
        #             except:
        #                 traceback.print_exc()
        # except Exception as e:
        #     traceback.print_exc()
