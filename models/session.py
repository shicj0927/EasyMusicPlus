from dataclasses import dataclass

@dataclass
class Session:
    vol: int=100
    lib: str|None=None
    theme: str="dark"

    @classmethod
    def from_dict(cls, data):
        return cls(**data)