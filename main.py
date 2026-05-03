import os

os.environ["LC_NUMERIC"] = "C"

import sys
import traceback

def exception_hook(exctype, value, tb):
    traceback.print_exception(exctype, value, tb)

sys.excepthook = exception_hook

from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

# from app.download_dialog import DownloadDialog
# dialog = DownloadDialog()
# dialog.show()

app.exec()