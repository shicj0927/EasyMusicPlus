from PyQt6.QtWidgets import QDialog
from ui.ui_about_dialog import Ui_qDialog_aboutDialog

class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_qDialog_aboutDialog()
        self.ui.setupUi(self)
        self.init_ui()
        self.bind_signals()

    def init_ui(self):
        pass

    def bind_signals(self):
        self.ui.qPushButton_quit.clicked.connect(self.close)