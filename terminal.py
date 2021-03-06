import sys, os, locale, struct
import subprocess
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QPalette, QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re
from ctypes import *
import msvcrt


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
    string_buffer = ''
    
    def __init__(self, *args, **kwargs):
        super(Terminal, self).__init__(*args, **kwargs)

        self.codec = locale.getdefaultlocale()

        pal = self.palette()
        pal.setColor(QPalette.Base, DEFAULT_TTY_BG)
        pal.setColor(QPalette.Text, DEFAULT_TTY_FG)
        self.setPalette(pal)
        self.setFont(DEFAULT_TTY_FONT)
        self.insertPlainText(' > ')

        self.setReadOnly(True)
    
    def cb_echo(self, pty_m):
        print('cb_echo')
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
            self.string_buffer = self.string_buffer[:-1] # remove last character
        elif char == '\r':                                # Enter
            self.backspace_budget = 0
            if(self.string_buffer == ''): # No command entered, go to nextline
                cursor.insertText(' > ')
            else:
                command_list = self.string_buffer.split(' ')
                if(command_list[0] == 'cls'):
                    self.clear()
                    self.reset_string_buffer()
                    cursor.insertText(' > ')
                    return
                if(command_list[0] == 'cmd'):
                    # breaks terminal and kills pipe while debugging
                    # Crashes program and gives this error in IDE terminal
                    # "The process tried to write to a nonexistent pipe.""
                    cursor.insertText("Don't go, Please stay here :(\r")# append()
                    cursor.insertText(' > ')
                    self.reset_string_buffer()
                    return

                # procc = subprocess.Popen(command_list, stdout=subprocess.PIPE, shell=True)
                # out, err = procc.communicate()
                # procc.kill()
                try:
                    cmd = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    cmd_out = cmd.stdout.read()
                    cmd_err = cmd.stderr.readline()
                    # print('CMD OUT: ',cmd_out)
                    # print('CMD ERR: ',cmd_err)

                    cmd.kill()
                    # out, err = procc.communicate()
                    # procc.kill()
                    if(cmd_out!=b''):
                        '''
                        Valid output
                        '''
                         # Process output
                        if(command_list[0] == 'tree'):
                            # Ref. : For encoding and buffer
                            # https://stackoverflow.com/questions/1259084/what-encoding-code-page-is-cmd-exe-using
                            # solved with https://superuser.com/questions/384248/how-can-i-store-windows-tree-command-output-in-a-file-and-retrieve-it-again
                            # Using CP437 Solved issue : https://en.wikipedia.org/wiki/Code_page_437
                            # Google search query : https://www.google.com/search?q=output+of+tree+command+encoded+in&rlz=1C1CHBD_enIN909IN910&oq=output+of+tree+command+encoded+in&aqs=chrome..69i57j33i160l4.7509j0j7&sourceid=chrome&ie=UTF-8
                            cursor.insertText(cmd_out.decode("CP437"))
                            cursor.insertText(' > ')
                            self.reset_string_buffer()
                            return

                        # self.append(out.decode("utf-8")) # Causes error with "tree" commmand
                        # Error message 
                        # Ref : UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc0 in position 75: invalid start byte    
                        # https://stackoverflow.com/questions/23772144/python-unicodedecodeerror-utf8-codec-cant-decode-byte-0xc0-in-position-0-i
                        # https://stackoverflow.com/questions/27453879/unicode-decode-error-how-to-skip-invalid-characters/27456542#27456542
                        #self.append(out.decode("ISO-8859-1")) # Causes error with "tree" commmand
                        cursor.insertText(cmd_out.decode("CP437"))
                        cursor.insertText(' > ')
                        self.reset_string_buffer()
                    elif(cmd_err!=b''):
                        '''
                        Error output
                        '''
                        cursor.insertText(cmd_err.decode("CP437"))
                        cursor.insertText(' > ')
                        self.reset_string_buffer()

                except OSError:
                    cursor.insertText("Invalid command, for now")
                    cursor.insertText(' > ')
                    self.reset_string_buffer()

        key_ascii = event.key()
        lower_case = key_ascii>=65 and key_ascii<=90
        upper_case = key_ascii>=97 and key_ascii<=122
        spacebar = key_ascii==32
        spl = [45, 46, 47, 33] # dot, forward & backward slash, hyphen, exclamation will see if others need to be added
        special_char = key_ascii in spl # for filenames
        if( lower_case or upper_case or spacebar or special_char):
            self.string_buffer += char

        # Regardless of what we do, send the character to the PTY
        # (Let the kernel's PTY implementation do most of the heavy lifting)
        #print("Codec", self.codec[1])
        #print("Char.encode", int.from_bytes(char.encode(self.codec[1]), "big"))
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
        os.close(int.from_bytes(b'', "big") )

        # Hook up an event handler for data waiting on the PTY
        # (Because I didn't feel like looking into whether QProcess can be
        #  integrated with PTYs as a subprocess.Popen alternative)
        self.notifier = QSocketNotifier(
            self.pty_m, QSocketNotifier.Read, self)
        self.notifier.activated.connect(self.cb_echo)
    
    def reset_string_buffer(self):
        self.string_buffer = ''

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainwin = Terminal()

#     # Cheap hack to estimate what 80x25 should be in pixels and resize to it
#     fontMetrics = mainwin.fontMetrics()
#     target_width = (fontMetrics.boundingRect(
#         REFERENCE_CHAR * DEFAULT_COLS
#     ).width() + app.style().pixelMetric(QStyle.PM_ScrollBarExtent))
#     mainwin.resize(target_width, fontMetrics.height() * DEFAULT_ROWS)

#     mainwin.spawn(DEFAULT_TTY_CMD)

#     # Take advantage of how Qt lets any widget be a top-level window
#     mainwin.show()
#     app.exec_()