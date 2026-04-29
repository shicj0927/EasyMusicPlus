from PySide6.QtWidgets import QMainWindow
from ui.ui_main_window import Ui_MainWindow
from services.player_service import PlayerService

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.player_service = PlayerService()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_ui()
        self.bind_signals()

    def init_ui(self):
        self.ui.qSplitter_mainSplitter.setSizes(
            [200, 400, 300]
        )

    def bind_signals(self):
        self.ui.qPushButton_control.clicked.connect(
            self.toggle_play
        )

    def toggle_play(self):
        self.player_service.play()