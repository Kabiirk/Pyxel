import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


##########GLOBALS###########
DEFAULT_TTY_CMD = ['/bin/bash']
DEFAULT_COLS = 80
DEFAULT_ROWS = 25

# NOTE: You can use any QColor instance, not just the predefined ones.
DEFAULT_TTY_FONT = QFont('Noto', 16)
DEFAULT_TTY_FG = Qt.lightGray
DEFAULT_TTY_BG = Qt.black

# The character to use as a reference point when converting between pixel and
# character cell dimensions in the presence of a non-fixed-width font
REFERENCE_CHAR = 'W'
############################


class Terminal(QTextEdit):
    backspace_budget = 0
    pty_m = None
    subproc = None
    notifier = None
    
    def __init__(self, *args, **kwargs):
        super(Terminal, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = Terminal()

    # Cheap hack to estimate what 80x25 should be in pixels and resize to it
    fontMetrics = mainwin.fontMetrics()
    target_width = (fontMetrics.boundingRect(
        REFERENCE_CHAR * DEFAULT_COLS
    ).width() + app.style().pixelMetric(QStyle.PM_ScrollBarExtent))
    mainwin.resize(target_width, fontMetrics.height() * DEFAULT_ROWS)

    # Take advantage of how Qt lets any widget be a top-level window
    mainwin.show()
    app.exec_()