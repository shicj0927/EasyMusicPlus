import json
import requests
from config import *

def get_current_playlist_by_id(id):
    url=API_BASE+"/playlist?id="+id
    for i in range(5):
        try:
            return requests.get(url).json()
        except:
            pass
    return None

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import traceback

class getNeteaseSonglistWorker(QObject):
    getNeteaseSonglistFinishedSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot(str)
    def get(self, id):
        try:
            self.getNeteaseSonglistFinishedSignal.emit(get_current_playlist_by_id(id))
        except Exception as e:
            traceback.print_exc()