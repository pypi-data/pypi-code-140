from ctypes import Structure, byref, sizeof, windll
from ctypes.wintypes import DWORD, HWND, LPARAM, RECT, UINT

import win32api
import win32con
import win32gui

from qtpy.QtCore import QOperatingSystemVersion
from qtpy.QtGui import QGuiApplication
# should use PyQt5 for using QtWin, since Qt6 ditched it
from PyQt5.QtWinExtras import QtWin
from win32comext.shell import shellcon


def isMaximized(hWnd):
    windowPlacement = win32gui.GetWindowPlacement(hWnd)
    if not windowPlacement:
        return False

    return windowPlacement[1] == win32con.SW_MAXIMIZE

def isFullScreen(hWnd):
    if not hWnd:
        return False
    winRect = win32gui.GetWindowRect(hWnd)
    if not winRect:
        return False
    monitorInfo = getMonitorInfo(hWnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    if not monitorInfo:
        return False
    monitorRect = monitorInfo["Monitor"]
    return all(i == j for i, j in zip(winRect, monitorRect))

def getMonitorInfo(hWnd, dwFlags):
    monitor = win32api.MonitorFromWindow(hWnd, dwFlags)
    if not monitor:
        return

    return win32api.GetMonitorInfo(monitor)

def getResizeBorderThickness(hWnd):
    window = findWindow(hWnd)
    if not window:
        return 0

    result = win32api.GetSystemMetrics(win32con.SM_CXSIZEFRAME) + win32api.GetSystemMetrics(92)

    if result > 0:
        return result

    thickness = 8 if QtWin.isCompositionEnabled() else 4
    return round(thickness*window.devicePixelRatio())

def findWindow(hWnd):
    if not hWnd:
        return

    windows = QGuiApplication.topLevelWindows()
    if not windows:
        return

    for window in windows:
        if window and int(window.winId()) == hWnd:
            return window

def isGreaterEqualVersion(version):
    return QOperatingSystemVersion.current() >= version

def isGreaterEqualWin8_1():
    return isGreaterEqualVersion(QOperatingSystemVersion.Windows8_1)


class APPBARDATA(Structure):
    _fields_ = [
        ('cbSize',            DWORD),
        ('hWnd',              HWND),
        ('uCallbackMessage',  UINT),
        ('uEdge',             UINT),
        ('rc',                RECT),
        ('lParam',            LPARAM),
    ]


class Taskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def isAutoHide():
        appbarData = APPBARDATA(sizeof(APPBARDATA), 0,
                                0, 0, RECT(0, 0, 0, 0), 0)
        taskbarState = windll.shell32.SHAppBarMessage(
            shellcon.ABM_GETSTATE, byref(appbarData))

        return taskbarState == shellcon.ABS_AUTOHIDE

    @classmethod
    def getPosition(cls, hWnd):
        if isGreaterEqualWin8_1():
            monitorInfo = getMonitorInfo(
                hWnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not monitorInfo:
                return cls.NO_POSITION

            monitor = RECT(*monitorInfo['Monitor'])
            appbarData = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor, 0)
            positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
            for position in positions:
                appbarData.uEdge = position
                if windll.shell32.SHAppBarMessage(11, byref(appbarData)):
                    return position

            return cls.NO_POSITION

        appbarData = APPBARDATA(sizeof(APPBARDATA), win32gui.FindWindow(
            "Shell_TrayWnd", None), 0, 0, RECT(0, 0, 0, 0), 0)
        if appbarData.hWnd:
            windowMonitor = win32api.MonitorFromWindow(
                hWnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not windowMonitor:
                return cls.NO_POSITION

            taskbarMonitor = win32api.MonitorFromWindow(
                appbarData.hWnd, win32con.MONITOR_DEFAULTTOPRIMARY)
            if not taskbarMonitor:
                return cls.NO_POSITION

            if taskbarMonitor == windowMonitor:
                windll.shell32.SHAppBarMessage(
                    shellcon.ABM_GETTASKBARPOS, byref(appbarData))
                return appbarData.uEdge

        return cls.NO_POSITION