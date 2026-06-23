from dataclasses import dataclass

@dataclass
class Session:
    vol: int=100
    lib: str|None=None
    theme: str="light"
    current_playlist_id: str|None=None

    @classmethod
    def from_dict(cls, data):
        return cls(**data)