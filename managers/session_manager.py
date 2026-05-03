import os
from models.session import Session
from dataclasses import asdict
import json
import traceback


class SessionManager:
    def __init__(self):
        # 务必在打开文件前创建
        self.path=os.path.join(os.getcwd(),"session.json")
        self.session=Session()
    
    def load_session(self):
        try:
            if not os.path.exists(self.path):
                with open(self.path, "w") as f:
                    json.dump(asdict(self.session),f,indent=4)
            with open(self.path,"r") as f:
                data=json.load(f)
            self.session=Session.from_dict(data)
        except Exception as e:
            traceback.print_exc(e)
            return Session()
    
    def save_session(self):
        with open(self.path+".tmp", "w") as f:
            json.dump(asdict(self.session),f,indent=4)
            f.flush()
            os.fsync(f.fileno())
        os.replace(self.path+".tmp",self.path)

    def get_session(self):
        return self.session
    
    def set_session(self,s):
        self.session=s
        self.save_session()
