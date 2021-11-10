import sys, os, locale, struct
import subprocess
from PyQt5.QtGui import QFont, QPalette, QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


##########GLOBALS###########
DEFAULT_TTY_CMD = ['/bin/bash']
DEFAULT_COLS = 50
DEFAULT_ROWS = 25

# NOTE: You can use any QColor instance, not just the predefined ones.
DEFAULT_TTY_FONT = QFont('Noto', 10)
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

        self.codec = locale.getdefaultlocale()

        pal = self.palette()
        pal.setColor(QPalette.Base, DEFAULT_TTY_BG)
        pal.setColor(QPalette.Text, DEFAULT_TTY_FG)
        self.setPalette(pal)
        self.setFont(DEFAULT_TTY_FONT)

        self.setReadOnly(True)
    
    def cb_echo(self, pty_m):
        """Display output that arrives from the PTY"""
        # Read pending data or assume the child exited if we can't
        # (Not technically the proper way to detect child exit, but it works)
        try:
            # Use 'replace' as a not-ideal-but-better-than-nothing way to deal
            # with bytes that aren't valid in the chosen encoding.
            child_output = os.read(self.pty_m, 1024).decode(
                self.codec, 'replace')
        except OSError:
            # Ask the event loop to exit and then return to it
            QApplication.instance().quit()
            return

    def keyPressEvent(self, event):
        """Handler for all key presses delivered while the widget has focus"""
        char = event.text()
        print(char)

        # Move the cursor to the end
        self.moveCursor(QTextCursor.End)
        cursor = self.textCursor()

        if char and (char.isprintable() or char == '\r'):
            cursor.insertText(char)
            self.backspace_budget += len(char)

        # Implement backspacing characters we typed
        if char == '\x08' and self.backspace_budget > 0:  # Backspace
            cursor.deletePreviousChar()
            self.backspace_budget -= 1
        elif char == '\r':                                # Enter
            self.backspace_budget = 0

        # Regardless of what we do, send the character to the PTY
        # (Let the kernel's PTY implementation do most of the heavy lifting)
        print("Codec", self.codec[1])
        print("Char.encode", char.encode(self.codec[1]))
        #print(self.pty_m)
        #os.write(self.pty_m, char.encode(self.codec[1]))

        scroller = self.verticalScrollBar()
        scroller.setValue(scroller.maximum())

    def spawn(self, argv):
        if self.pty_m:
            self.pty_m.close()
        if self.notifier:
            self.notifier.disconnect()

        proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        self.pty_m, stderr = proc.communicate(b'dir c:\\')
        #print(self.pty_m)

        #self.pty_m, pty_s = os.openpty()

        self.backspace_budget = 0

        child_env = os.environ.copy()
        child_env['TERM'] = 'tty'

        # # Launch the subprocess
        # # FIXME: Keep a reference so we can reap zombie processes
        # subprocess.Popen(argv,  # nosec
        #     stdin=pty_s, stdout=pty_s, stderr=pty_s,
        #     env=child_env,
        #     preexec_fn=os.setsid)

        # # Close the child side of the PTY so that we can detect when to exit
        #print(int.from_bytes(b'', "big")  )
        #print("stderr", stderr)
        os.close(int.from_bytes(b'', "big") )

        # Hook up an event handler for data waiting on the PTY
        # (Because I didn't feel like looking into whether QProcess can be
        #  integrated with PTYs as a subprocess.Popen alternative)
        self.notifier = QSocketNotifier(
            self.pty_m, QSocketNotifier.Read, self)
        self.notifier.activated.connect(self.cb_echo)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = Terminal()

    # Cheap hack to estimate what 80x25 should be in pixels and resize to it
    fontMetrics = mainwin.fontMetrics()
    target_width = (fontMetrics.boundingRect(
        REFERENCE_CHAR * DEFAULT_COLS
    ).width() + app.style().pixelMetric(QStyle.PM_ScrollBarExtent))
    mainwin.resize(target_width, fontMetrics.height() * DEFAULT_ROWS)

    mainwin.spawn(DEFAULT_TTY_CMD)

    # Take advantage of how Qt lets any widget be a top-level window
    mainwin.show()
    app.exec_()