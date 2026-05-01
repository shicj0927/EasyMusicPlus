from PyQt6.QtWidgets import QMainWindow
from ui.ui_main_window import Ui_mainWindow
from services.player_service import PlayerService

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.player_service = PlayerService()

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.init_ui()
        self.bind_signals()

    def init_ui(self):
        self.ui.qSplitter_mainSplitter.setSizes(
            [200, 600, 200]
        )

    def bind_signals(self):
        self.ui.qAction_quit.triggered.connect(self.close)
        self.ui.qAction_downloader.triggered.connect(self.open_download_dialog)
    
    def open_download_dialog(self):
        from app.download_dialog import DownloadDialog
        dialog = DownloadDialog(self)
        dialog.exec()