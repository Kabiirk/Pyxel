#source: https://github.com/Opticos/GWSL-Source/blob/master/blur.py , https://www.cnblogs.com/zhiyiYo/p/14659981.html , https://github.com/ifwe/digsby/blob/master/digsby/src/gui/vista.py
# FULL CREDIT TO : 
# https://github.com/Peticali/PythonBlurBehind for code inspiration
import os
import platform
import ctypes
from PyQt5 import QtCore

from PyQt5.QtGui import QColor, QFont

if platform.system() == 'Darwin':
    from AppKit import *

    def MacBlur(QWidget,Material=NSVisualEffectMaterialPopover,TitleBar:bool=True):
        #WIP, trying to implement CGSSetWindowBackgroundBlurRadius too
        frame = NSMakeRect(0, 0, QWidget.width(), QWidget.height())
        view = objc.objc_object(c_void_p=QWidget.winId().__int__())

        visualEffectView = NSVisualEffectView.new()
        visualEffectView.setAutoresizingMask_(NSViewWidthSizable|NSViewHeightSizable) #window resizable
        #visualEffectView.setWantsLayer_(True)
        visualEffectView.setFrame_(frame)
        visualEffectView.setState_(NSVisualEffectStateActive)
        visualEffectView.setMaterial_(Material) #https://developer.apple.com/documentation/appkit/nsvisualeffectmaterial
        visualEffectView.setBlendingMode_(NSVisualEffectBlendingModeBehindWindow)

        window = view.window()
        content = window.contentView()

        try:
            from PyQt5.QtWidgets import QMacCocoaViewContainer
            
        except:
            print('You need PyQt5')
            exit()
            
        container = QMacCocoaViewContainer(0,QWidget)
        content.addSubview_positioned_relativeTo_(visualEffectView, NSWindowBelow, container)  

        if TitleBar:
            #TitleBar with blur
            window.setTitlebarAppearsTransparent_(True)
            window.setStyleMask_(window.styleMask() | NSFullSizeContentViewWindowMask)

        #appearance = NSAppearance.appearanceNamed_('NSAppearanceNameVibrantDark')
        #window.setAppearance_(appearance)


if platform.system() == 'Windows':
    from ctypes.wintypes import  DWORD, BOOL, HRGN, HWND
    user32 = ctypes.windll.user32
    dwm = ctypes.windll.dwmapi


    class ACCENTPOLICY(ctypes.Structure):
        _fields_ = [
            ("AccentState", ctypes.c_uint),
            ("AccentFlags", ctypes.c_uint),
            ("GradientColor", ctypes.c_uint),
            ("AnimationId", ctypes.c_uint)
        ]


    class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.POINTER(ctypes.c_int)),
            ("SizeOfData", ctypes.c_size_t)
        ]


    class DWM_BLURBEHIND(ctypes.Structure):
        _fields_ = [
            ('dwFlags', DWORD), 
            ('fEnable', BOOL),  
            ('hRgnBlur', HRGN), 
            ('fTransitionOnMaximized', BOOL) 
        ]


    class MARGINS(ctypes.Structure):
        _fields_ = [("cxLeftWidth", ctypes.c_int),
                    ("cxRightWidth", ctypes.c_int),
                    ("cyTopHeight", ctypes.c_int),
                    ("cyBottomHeight", ctypes.c_int)
                    ]


    SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
    SetWindowCompositionAttribute.argtypes = (HWND, WINDOWCOMPOSITIONATTRIBDATA)
    SetWindowCompositionAttribute.restype = ctypes.c_int


def ExtendFrameIntoClientArea(HWND):
    margins = MARGINS(-1, -1, -1, -1)
    dwm.DwmExtendFrameIntoClientArea(HWND, ctypes.byref(margins))


def Win7Blur(HWND,Acrylic):
    if Acrylic == False:
        DWM_BB_ENABLE = 0x01
        bb = DWM_BLURBEHIND()
        bb.dwFlags = DWM_BB_ENABLE
        bb.fEnable = 1
        bb.hRgnBlur = 1
        dwm.DwmEnableBlurBehindWindow(HWND, ctypes.byref(bb))
    else:
        ExtendFrameIntoClientArea(HWND)


def HEXtoRGBAint(HEX:str):
    alpha = HEX[7:]
    blue = HEX[5:7]
    green = HEX[3:5]
    red = HEX[1:3]

    gradientColor = alpha + blue + green + red
    return int(gradientColor, base=16)


def blur(hwnd, hexColor=False, Acrylic=False, Dark=False):
    accent = ACCENTPOLICY()
    accent.AccentState = 3 #Default window Blur #ACCENT_ENABLE_BLURBEHIND

    gradientColor = 0
    
    if hexColor != False:
        gradientColor = HEXtoRGBAint(hexColor)
        accent.AccentFlags = 2 #Window Blur With Accent Color #ACCENT_ENABLE_TRANSPARENTGRADIENT
    
    if Acrylic:
        accent.AccentState = 4 #UWP but LAG #ACCENT_ENABLE_ACRYLICBLURBEHIND
        if hexColor == False: #UWP without color is translucent
            accent.AccentFlags = 2
            gradientColor = HEXtoRGBAint('#12121240') #placeholder color
    
    accent.GradientColor = gradientColor
    
    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19 #WCA_ACCENT_POLICY
    data.SizeOfData = ctypes.sizeof(accent)
    data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.POINTER(ctypes.c_int))
    
    SetWindowCompositionAttribute(int(hwnd), data)
    
    if Dark: 
        data.Attribute = 26 #WCA_USEDARKMODECOLORS
        SetWindowCompositionAttribute(int(hwnd), data)


def BlurLinux(WID): #may not work in all distros (working in Deepin)
    import os

    c = "xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id " + str(WID)
    os.system(c)


def GlobalBlur(HWND,hexColor=False,Acrylic=False,Dark=False,QWidget=None):
    release = platform.release()
    system = platform.system()

    if system == 'Windows':
        print('Windows')
        if release == 'Vista':
            print('Winblur')
            Win7Blur(HWND,Acrylic)
        else:
            release = int(float(release))
            if release == 10 or release == 8 or release == 11: #idk what windows 8.1 spits, if is '8.1' int(float(release)) will work...
                print('blur')
                blur(HWND,hexColor,Acrylic,Dark)
            else:
                print('Winblur 2')
                Win7Blur(HWND,Acrylic)
    
    if system == 'Linux':
        BlurLinux(HWND)

    if system == 'Darwin':
        MacBlur(QWidget)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *

    class MainWindow(QWidget):
        def __init__(self):
            super(MainWindow, self).__init__()
            #self.setWindowFlags(Qt.FramelessWindowHint)
            self.backspace_buffer = 0
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.resize(500, 400)
            
            hWnd = self.winId()
            #print(hWnd)
            #l = QLabel('Can you see me?', self)
            layout = QVBoxLayout()
            self.t = QTextEdit(parent=self)
            self.t.installEventFilter(self)
            self.t.setStyleSheet("QTextEdit { background-color: rgba(0, 0, 0, 0); border: 0 }")
            self.t.setTextColor(QColor('#FFFFFF'))
            font = QFont("Consolas", 10)
            self.t.setFont(font)
            self.cursor = self.t.textCursor()
            self.cursor.insertText(str(os.getcwd())+" > ")
            layout.addWidget(self.t)
            self.setLayout(layout)
            #t.setText('PyTerm >')
            GlobalBlur(hWnd,hexColor='#12121299',Dark=True,QWidget=self)
            

            self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

        def eventFilter(self, obj, event):
            if event.type() == QtCore.QEvent.KeyPress and obj is self.t:
                if event.key() == QtCore.Qt.Key_Return and self.t.hasFocus():
                    self.backspace_buffer = 0
                    self.cursor.insertText(str(os.getcwd())+" > ")
                if event.key() == QtCore.Qt.Key_Backspace and self.t.hasFocus():
                    self.backspace_buffer -= 1
                if (event.key() != QtCore.Qt.Key_Backspace and event.key() != QtCore.Qt.Key_Return)and self.t.hasFocus():
                    self.backspace_buffer += 1
                    print(self.backspace_buffer)
                    
            return super().eventFilter(obj, event)

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    #blur(mw.winId())
    #ExtendFrameIntoClientArea(mw.winId())

    sys.exit(app.exec_())