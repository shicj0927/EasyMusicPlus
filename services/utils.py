def safe_file_name(name):
    """将字符串转换为安全的文件名"""
    dangerous_chars = r'\/:*?"<>|'
    for char in dangerous_chars:
        name = name.replace(char, '_')
    if len(name) > 200:
        name = name[:200]
    return name.strip()