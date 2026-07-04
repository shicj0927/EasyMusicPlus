import os
from models.session import Session
from dataclasses import asdict
from pathlib import Path
from platformdirs import user_data_dir
import json
import traceback


class SessionManager:
    def __init__(self):
        base_dir = Path(user_data_dir("EasyMusicPlus"))
        base_dir.mkdir(parents=True, exist_ok=True)
        self.path = base_dir / "session.json"
        self.session = Session()
    
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
        tmp_path = self.path.with_name(self.path.name + ".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self.session), f, indent=4)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, self.path)

    def get_session(self):
        return self.session
    
    def set_session(self,s):
        self.session=s
        self.save_session()
