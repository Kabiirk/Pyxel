import logging
import sys
import threading

from term import TextMode
from term import get_default_text_attribute
from term import DEFAULT_FG_COLOR_IDX, DEFAULT_BG_COLOR_IDX
from term import Cell, Line
from term_char_width import char_width
from terminal import Terminal
from charset_mode import translate_char, translate_char_british
from screen_buffer import ScreenBuffer

LOGGER = logging.getLogger('term_gui')
TAB_MAX = 999


class TerminalGUI(Terminal):
    def __init__(self, cfg):
        Terminal.__init__(self, cfg)

        self.term_widget = None
        self.session = None

        self.col = 0
        self.row = 0

        self.remain_buffer = []

        self.cur_line_option = get_default_text_attribute()
        self.saved_screen_buffer, self.saved_cursor, \
            self.saved_cur_line_option = \
            ScreenBuffer(), (0, 0), get_default_text_attribute()

        self.status_line = []
        self.status_line_mode = 0

        self.charset_modes_translate = [None, None]
        self.charset_mode = 0

        self._saved_charset_modes_translate = [None, None]
        self._saved_charset_mode = 0

        self._data_lock = threading.RLock()
        self._screen_buffer = ScreenBuffer()

        self._dec_mode = False
        self._force_column = False
        self._force_column_count = 80

        self._origin_mode = False
        self._saved_origin_mode = False

        self._tab_stops = {}
        self._set_default_tab_stops()

        self._cursor_visible = True

    def _set_default_tab_stops(self):
        tab_width = self.get_tab_width()

        for i in range(0, TAB_MAX, tab_width):
            self._tab_stops[i] = True
