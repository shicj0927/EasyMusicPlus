import mpv
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class PlayerManager:
    positionChanged = pyqtSignal(float)
    durationChanged = pyqtSignal(float)
    stateChanged = pyqtSignal()

    def __init__(self):
        self.player=mpv.MPV

    def play(self, path):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def seek(self, seconds):
        pass

    def set_position_percent(self, percent):
        pass

    def set_volume(self, volume):
        pass

    def get_position(self):
        pass

    def get_duration(self):
        pass 

    def is_playing(self):
        pass