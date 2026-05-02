import requests
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class SearchWorker(QObject):
    searchFinishedSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot(str, str, int, int)
    def search(self, keyword, source, page_length=20, page_num=1):
        print(f"search: {keyword} from {source}")
        url = f"https://music-api.gdstudio.xyz/api.php?types=search&source={source}&name={keyword}&count={page_length}&pages={page_num}"
        i=1
        while i<=5:
            print(f"Attempt {i} to fetch data from {url}")
            response = requests.get(url)
            if response.status_code == 200 and response.json()!=None and response.json()!=[]:
                self.searchFinishedSignal.emit(response.json())
                return
            i+=1
        self.searchFinishedSignal.emit(None)
    