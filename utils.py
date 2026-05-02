import os

def safe_file_name(name):
    dangerous_chars = r'\/:*?"<>|'
    for char in dangerous_chars:
        name = name.replace(char, '_')
    if len(name) > 200:
        name = name[:200]
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