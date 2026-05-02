import re
from models.media import LyricLine, Lyric
import bisect

class LyricManager:
    def __init__(self):
        self.lyric=Lyric()
        self.path=""
        self.loaded=False
    
    def load(self,path):
        self.path = path
        self.lyric = Lyric()
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        pattern = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
        for line in content.splitlines():
            match = pattern.match(line)
            if not match:
                continue
            minute = int(match.group(1))
            second = float(match.group(2))
            text = match.group(3).strip()
            time_ms = int((minute * 60 + second) * 1000)
            lyric_line = LyricLine(
                time_ms=time_ms,
                text=text
            )
            self.lyric.lines.append(lyric_line)
        self.loaded = True
        self.lyric.lines.sort(key=lambda x: x.time_ms)

    def get_current_lyric(self, time_ms):
        times = [line.time_ms for line in self.lyric.lines]
        index = bisect.bisect_right(times, time_ms) - 1
        if index >= 0:
            return self.lyric.lines[index].text
        return None

    