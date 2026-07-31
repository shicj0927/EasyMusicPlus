import os
from pathlib import Path

def safe_file_name(name, max_bytes=150):
    dangerous_chars = r'\/:*?"<>|'
    for c in dangerous_chars:
        name = name.replace(c, "_")
    while len(name.encode("utf-8")) > max_bytes:
        name = name[:-1]
    return name.strip()

def time_s_to_m_s(time_s):
    time_s=int(time_s)
    return "%02d:%02d"%(time_s/60,time_s%60)

def get_rel_path(target):
    if target=="" or target==None:
        return target
    current = os.getcwd()
    rel_path = os.path.relpath(target, current)
    return rel_path

def load_theme(self, name: str):
    path = Path("themes") / f"{name}.qss"
    with open(path, "r", encoding="utf-8") as f:
        self.setStyleSheet(f.read())