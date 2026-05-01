from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

# from app.download_dialog import DownloadDialog
# dialog = DownloadDialog()
# dialog.show()

app.exec()