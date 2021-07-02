# General Imports
import sys

# Module Imports
from ui import ui

# Other specific Imports
from PyQt5.QtWidgets import QApplication

class Window(ui.MainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Pyxel")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
