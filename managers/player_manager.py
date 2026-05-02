import mpv
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from enum import Enum

class PlayerState(Enum):
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2

class PlayerManager(QObject):
    positionChangedSignal = pyqtSignal(float)
    durationChangedSignal = pyqtSignal(float)
    stateChangedSignal = pyqtSignal(PlayerState)

    def __init__(self,widget):
        super().__init__()
        self.player=mpv.MPV(wid=str(int(widget.winId())))
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(200)
        self.state=PlayerState.STOPPED

        @self.player.event_callback("file-loaded")
        def on_loaded(event):
            self.update_duration()
        
        @self.player.event_callback("end-file")
        def on_end(event):
            self.state=PlayerState.STOPPED
            self.stateChangedSignal.emit(self.state)

    def play(self, path):
        self.player.play(path)
        self.state=PlayerState.PLAYING
        self.stateChangedSignal.emit(self.state)

    def pause(self):
        if self.state!=PlayerState.PLAYING:
            return
        self.player.pause=True
        self.state=PlayerState.PAUSED
        self.stateChangedSignal.emit(self.state)

    def resume(self):
        if self.state!=PlayerState.PAUSED:
            return
        self.player.pause=False
        self.state=PlayerState.PLAYING
        self.stateChangedSignal.emit(self.state)
    
    def pause_resume(self):
        if self.player.pause==False:
            self.pause()
        else:
            self.resume()

    def stop(self):
        self.player.stop()
        self.state=PlayerState.STOPPED
        self.stateChangedSignal.emit(self.state)

    def seek(self, seconds):
        self.player.seek(seconds)
    
    def seek_absolute(self, seconds):
        self.player.command(
            "seek",
            seconds,
            "absolute"
        )

    def set_volume(self, volume):
        self.player.volumn=volume

    def get_position(self):
        return self.player.time_pos or 0
    
    def update_position(self):
        self.positionChangedSignal.emit(self.get_position())

    def get_duration(self):
        return self.player.duration or 0
    
    def update_duration(self):
        self.durationChangedSignal.emit(self.get_duration())
