# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2022 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""Helper class to write Qt widget unittests."""

__authors__ = ["T. Vincent"]
__license__ = "MIT"
__date__ = "22/07/2022"


import gc
import logging
import unittest
import time
import functools
import sys
import os

_logger = logging.getLogger(__name__)

from PyMca5.PyMcaGui import PyMcaQt as qt

if qt.BINDING == 'PySide':
    from PySide.QtTest import QTest
    try:  # Available through PySide
        from PySide.shiboken import isValid  # noqa
        from PySide.shiboken import createdByPython  # noqa
        from PySide.shiboken import ownedByPython  # noqa
    except ImportError:  # Available through standalone shiboken package
        from Shiboken.shiboken import isValid  # noqa
        from Shiboken.shiboken import createdByPython  # noqa
        from Shiboken.shiboken import ownedByPython  # noqa
elif qt.BINDING == 'PySide2':
    from PySide2.QtTest import QTest
    try:
        from PySide2.shiboken2 import isValid  # noqa
        from PySide2.shiboken2 import createdByPython  # noqa
        from PySide2.shiboken2 import ownedByPython  # noqa
    except ImportError:
        from shiboken2 import isValid  # noqa
        from shiboken2 import createdByPython  # noqa
        from shiboken2 import ownedByPython  # noqa
elif qt.BINDING == 'PyQt5':
    from PyQt5.QtTest import QTest
    try:
        from PyQt5.sip import isdeleted as _isdeleted  # noqa
        from PyQt5.sip import ispycreated as createdByPython  # noqa
        from PyQt5.sip import ispyowned as ownedByPython  # noqa
    except ImportError:
        from sip import isdeleted as _isdeleted  # noqa
        from sip import ispycreated as createdByPython  # noqa
        from sip import ispyowned as ownedByPython  # noqa
    def isValid(obj):
        """Returns True if underlying C++ object is valid.

        :param QObject obj:
        :rtype: bool
        """
        return not _isdeleted(obj)

elif qt.BINDING == 'PyQt4':
    from PyQt4.QtTest import QTest
    from sip import isdeleted as _isdeleted  # noqa
    from sip import ispycreated as createdByPython  # noqa
    from sip import ispyowned as ownedByPython  # noqa
    def isValid(obj):
        """Returns True if underlying C++ object is valid.

        :param QObject obj:
        :rtype: bool
        """
        return not _isdeleted(obj)

elif qt.BINDING == 'PySide6':
    from PySide6.QtTest import QTest
    from shiboken6 import isValid, createdByPython, ownedByPython
else:
    raise ImportError('Unsupported Qt bindings')

# Qt4/Qt5 compatibility wrapper
if qt.BINDING in ('PySide', 'PyQt4'):
    _logger.info("QTest.qWaitForWindowExposed not available," +
                 "using QTest.qWaitForWindowShown instead.")

    def qWaitForWindowExposed(window, timeout=None):
        """Mimic QTest.qWaitForWindowExposed for Qt4."""
        QTest.qWaitForWindowShown(window)
        return True
else:
    qWaitForWindowExposed = QTest.qWaitForWindowExposed


def qWaitForWindowExposedAndActivate(window, timeout=None):
    """Waits until the window is shown in the screen.

    It also activates the window and raises it.

    See QTest.qWaitForWindowExposed for details.
    """
    if timeout is None:
        result = qWaitForWindowExposed(window)
    else:
        result = qWaitForWindowExposed(window, timeout)

    if result:
        # Makes sure window is active and on top
        window.activateWindow()
        window.raise_()

    return result


# Placeholder for QApplication
_qapp = None


class TestCaseQt(unittest.TestCase):
    """Base class to write test for Qt stuff.

    It creates a QApplication before running the tests.
    WARNING: The QApplication is shared by all tests, which might have side
    effects.

    After each test, this class is checking for widgets remaining alive.
    To allow some widgets to remain alive at the end of a test, set the
    allowedLeakingWidgets attribute to the number of widgets that can remain
    alive at the end of the test.
    With PySide, this test is not run for now as it seems PySide
    is leaking widgets internally.

    All keyboard and mouse event simulation methods call qWait(20) after
    simulating the event (as QTest does on Mac OSX).
    This was introduced to fix issues with continuous integration tests
    running with Xvfb on Linux.
    """

    DEFAULT_TIMEOUT_WAIT = 100
    """Default timeout for qWait"""

    TIMEOUT_WAIT = 0
    """Extra timeout in millisecond to add to qSleep, qWait and
    qWaitForWindowExposed.

    Intended purpose is for debugging, to add extra time to waits in order to
    allow to view the tested widgets.
    """

    @classmethod
    def exceptionHandler(cls, exceptionClass, exception, stack):
        import traceback
        message = (''.join(traceback.format_tb(stack)))
        template = 'Traceback (most recent call last):\n{2}{0}: {1}'
        message = template.format(exceptionClass.__name__, exception, message)
        cls._exceptions.append(message)

    @classmethod
    def setUpClass(cls):
        """Makes sure Qt is inited"""
        cls._oldExceptionHook = sys.excepthook
        sys.excepthook = cls.exceptionHandler

        global _qapp
        if _qapp is None:
            app = qt.QApplication.instance()
            if app is None:
                # Makes sure a QApplication exists and do it once for all
                _qapp = qt.QApplication([])
            else:
                import weakref
                _qapp = weakref.proxy(app)

    @classmethod
    def tearDownClass(cls):
        sys.excepthook = cls._oldExceptionHook

    def setUp(self):
        """Get the list of existing widgets."""
        self.allowedLeakingWidgets = 0
        self.__previousWidgets = self.qapp.allWidgets()
        self.__class__._exceptions = []

    def _currentTestSucceeded(self):
        if hasattr(self, '_outcome'):
            if hasattr(self, '_feedErrorsToResult'):
                # For Python 3.4 -3.10
                result = self.defaultTestResult()  # these 2 methods have no side effects
                if hasattr(self._outcome, 'errors'):
                    self._feedErrorsToResult(result, self._outcome.errors)
            else:
                # Python 3.11+
                result = self._outcome.result
        else:
            # For Python < 3.4
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)

        skipped = self.id() in [case.id() for case, _ in result.skipped]
        error = self.id() in [case.id() for case, _ in result.errors]
        failure = self.id() in [case.id() for case, _ in result.failures]
        return not error and not failure and not skipped

    def _checkForUnreleasedWidgets(self):
        """Test fixture checking that no more widgets exists."""
        gc.collect()

        widgets = [widget for widget in self.qapp.allWidgets()
                   if (widget not in self.__previousWidgets and
                       createdByPython(widget))]
        del self.__previousWidgets

        if qt.BINDING in ('PySide', 'PySide2', 'PySide6', 'PyQt5', 'PyQt4'):
            # TODO: many leaks with PyQt5 as well...
            return  # Do not test for leaking widgets

        allowedLeakingWidgets = self.allowedLeakingWidgets
        self.allowedLeakingWidgets = 0

        if widgets and len(widgets) <= allowedLeakingWidgets:
            _logger.info(
                '%s: %d remaining widgets after test' % (self.id(),
                                                         len(widgets)))

        if len(widgets) > allowedLeakingWidgets:
            txt = "[ "
            for w in widgets:
                if hasattr(w, "text"):
                    txt += "%s text=%s, " % (w, w.text())
                else:
                    txt += "%s, " % w
            txt += "]"
            raise RuntimeError(
                "Test ended with widgets alive: %s" % txt)

    def tearDown(self):
        if len(self.__class__._exceptions) > 0:
            messages = "\n".join(self.__class__._exceptions)
            raise AssertionError("Exception occured in Qt thread:\n" + messages)

        if self._currentTestSucceeded():
            self._checkForUnreleasedWidgets()

    @property
    def qapp(self):
        """The QApplication currently running."""
        return qt.QApplication.instance()

    # Proxy to QTest

    Press = QTest.Press
    """Key press action code"""

    Release = QTest.Release
    """Key release action code"""

    Click = QTest.Click
    """Key click action code"""

    QTest = property(lambda self: QTest,
                     doc="""The Qt QTest class from the used Qt binding.""")

    def keyClick(self, widget, key, modifier=qt.Qt.NoModifier, delay=-1):
        """Simulate clicking a key.

        See QTest.keyClick for details.
        """
        QTest.keyClick(widget, key, modifier, delay)
        self.qWait(20)

    def keyClicks(self, widget, sequence, modifier=qt.Qt.NoModifier, delay=-1):
        """Simulate clicking a sequence of keys.

        See QTest.keyClick for details.
        """
        QTest.keyClicks(widget, sequence, modifier, delay)
        self.qWait(20)

    def keyEvent(self, action, widget, key,
                 modifier=qt.Qt.NoModifier, delay=-1):
        """Sends a Qt key event.

        See QTest.keyEvent for details.
        """
        QTest.keyEvent(action, widget, key, modifier, delay)
        self.qWait(20)

    def keyPress(self, widget, key, modifier=qt.Qt.NoModifier, delay=-1):
        """Sends a Qt key press event.

        See QTest.keyPress for details.
        """
        QTest.keyPress(widget, key, modifier, delay)
        self.qWait(20)

    def keyRelease(self, widget, key, modifier=qt.Qt.NoModifier, delay=-1):
        """Sends a Qt key release event.

        See QTest.keyRelease for details.
        """
        QTest.keyRelease(widget, key, modifier, delay)
        self.qWait(20)

    def mouseClick(self, widget, button, modifier=None, pos=None, delay=-1):
        """Simulate clicking a mouse button.

        See QTest.mouseClick for details.
        """
        if modifier is None:
            modifier = qt.Qt.KeyboardModifiers()
        pos = qt.QPoint(pos[0], pos[1]) if pos is not None else qt.QPoint()
        QTest.mouseClick(widget, button, modifier, pos, delay)
        self.qWait(20)

    def mouseDClick(self, widget, button, modifier=None, pos=None, delay=-1):
        """Simulate double clicking a mouse button.

        See QTest.mouseDClick for details.
        """
        if modifier is None:
            modifier = qt.Qt.KeyboardModifiers()
        pos = qt.QPoint(pos[0], pos[1]) if pos is not None else qt.QPoint()
        QTest.mouseDClick(widget, button, modifier, pos, delay)
        self.qWait(20)

    def mouseMove(self, widget, pos=None, delay=-1):
        """Simulate moving the mouse.

        See QTest.mouseMove for details.
        """
        pos = qt.QPoint(pos[0], pos[1]) if pos is not None else qt.QPoint()
        QTest.mouseMove(widget, pos, delay)
        self.qWait(20)

    def mousePress(self, widget, button, modifier=None, pos=None, delay=-1):
        """Simulate pressing a mouse button.

        See QTest.mousePress for details.
        """
        if modifier is None:
            modifier = qt.Qt.KeyboardModifiers()
        pos = qt.QPoint(pos[0], pos[1]) if pos is not None else qt.QPoint()
        QTest.mousePress(widget, button, modifier, pos, delay)
        self.qWait(20)

    def mouseRelease(self, widget, button, modifier=None, pos=None, delay=-1):
        """Simulate releasing a mouse button.

        See QTest.mouseRelease for details.
        """
        if modifier is None:
            modifier = qt.Qt.KeyboardModifiers()
        pos = qt.QPoint(pos[0], pos[1]) if pos is not None else qt.QPoint()
        QTest.mouseRelease(widget, button, modifier, pos, delay)
        self.qWait(20)

    def qSleep(self, ms):
        """Sleep for ms milliseconds, blocking the execution of the test.

        See QTest.qSleep for details.
        """
        QTest.qSleep(ms + self.TIMEOUT_WAIT)

    @classmethod
    def qWait(cls, ms=None):
        """Waits for ms milliseconds, events will be processed.

        See QTest.qWait for details.
        """
        if ms is None:
            ms = cls.DEFAULT_TIMEOUT_WAIT

        if qt.BINDING in ('PySide', 'PySide2', 'PySide6'):
            # PySide has no qWait, provide a replacement
            timeout = int(ms)
            endTimeMS = int(time.time() * 1000) + timeout
            while timeout > 0:
                _qapp.processEvents(qt.QEventLoop.AllEvents,
                                        timeout)
                timeout = endTimeMS - int(time.time() * 1000)
        else:
            QTest.qWait(ms + cls.TIMEOUT_WAIT)

    def qWaitForWindowExposed(self, window, timeout=None):
        """Waits until the window is shown in the screen.

        See QTest.qWaitForWindowExposed for details.
        """
        result = qWaitForWindowExposedAndActivate(window, timeout)

        if self.TIMEOUT_WAIT:
            QTest.qWait(self.TIMEOUT_WAIT)

        return result

    _qobject_destroyed = False

    @classmethod
    def _aboutToDestroy(cls):
        cls._qobject_destroyed = True

    @classmethod
    def qWaitForDestroy(cls, ref):
        """
        Wait for Qt object destruction.

        Use a weakref as parameter to avoid any strong references to the
        object.

        It have to be used as following. Removing the reference to the object
        before calling the function looks to be expected, else
        :meth:`deleteLater` will not work.

        .. code-block:: python

            ref = weakref.ref(self.obj)
            self.obj = None
            self.qWaitForDestroy(ref)

        :param weakref ref: A weakref to an object to avoid any reference
        :return: True if the object was destroyed
        :rtype: bool
        """
        cls._qobject_destroyed = False
        if qt.BINDING == 'PyQt4':
            # Without this, QWidget will be still alive on PyQt4
            # (at least on Windows Python 2.7)
            # If it is not skipped on PySide, silx.gui.dialog tests will
            # segfault (at least on Windows Python 2.7)
            import gc
            gc.collect()
        qobject = ref()
        if qobject is None:
            return True
        qobject.destroyed.connect(cls._aboutToDestroy)
        qobject.deleteLater()
        qobject = None
        for _ in range(10):
            if cls._qobject_destroyed:
                break
            cls.qWait(10)
        else:
            _logger.debug("Object was not destroyed")

        return ref() is None

    def logScreenShot(self, level=logging.ERROR):
        """Take a screenshot and log it into the logging system if the
        logger is enabled for the expected level.

        The screenshot is stored in the directory "./build/test-debug", and
        the logging system only log the path to this file.

        :param level: Logging level
        """
        if not _logger.isEnabledFor(level):
            return
        basedir = os.path.abspath(os.path.join("build", "test-debug"))
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        filename = "Screenshot_%s.png" % self.id()
        filename = os.path.join(basedir, filename)

        if not hasattr(self.qapp, "primaryScreen"):
            # Qt4
            winId = qt.QApplication.desktop().winId()
            pixmap = qt.QPixmap.grabWindow(winId)
        else:
            # Qt5
            screen = self.qapp.primaryScreen()
            pixmap = screen.grabWindow(0)
        pixmap.save(filename)
        _logger.log(level, "Screenshot saved at %s", filename)


class SignalListener(object):
    """Util to listen a Qt event and store parameters
    """

    def __init__(self):
        self.__calls = []

    def __call__(self, *args, **kargs):
        self.__calls.append((args, kargs))

    def clear(self):
        """Clear stored data"""
        self.__calls = []

    def callCount(self):
        """
        Returns how many times the listener was called.

        :rtype: int
        """
        return len(self.__calls)

    def arguments(self, callIndex=None, argumentIndex=None):
        """Returns positional arguments optionally filtered by call count id
        or argument index.

        :param int callIndex: Index of the called data
        :param int argumentIndex: Index of the positional argument.
        """
        if callIndex is not None:
            result = self.__calls[callIndex][0]
            if argumentIndex is not None:
                result = result[argumentIndex]
        else:
            result = [x[0] for x in self.__calls]
            if argumentIndex is not None:
                result = [x[argumentIndex] for x in result]
        return result

    def karguments(self, callIndex=None, argumentName=None):
        """Returns positional arguments optionally filtered by call count id
        or name of the keyword argument.

        :param int callIndex: Index of the called data
        :param int argumentName: Name of the keyword argument.
        """
        if callIndex is not None:
            result = self.__calls[callIndex][1]
            if argumentName is not None:
                result = result[argumentName]
        else:
            result = [x[1] for x in self.__calls]
            if argumentName is not None:
                result = [x[argumentName] for x in result]
        return result

    def partial(self, *args, **kargs):
        """Returns a new partial object which when called will behave like this
        listener called with the positional arguments args and keyword
        arguments keywords. If more arguments are supplied to the call, they
        are appended to args. If additional keyword arguments are supplied,
        they extend and override keywords.
        """
        return functools.partial(self, *args, **kargs)


def getQToolButtonFromAction(action):
    """Return a QToolButton corresponding to a QAction.

    :param QAction action: The QAction from which to get QToolButton.
    :return: A QToolButton associated to action or None.
    """
    if qt.BINDING == "PySide6":
        widgets = action.associatedObjects()
    else:
        widgets = action.associatedWidgets()

    for widget in widgets:
        if isinstance(widget, qt.QToolButton):
            return widget
    return None


def findChildren(parent, kind, name=None):
    if qt.BINDING in ("PySide", "PySide2", "PySide6") and name is not None:
        result = []
        for obj in parent.findChildren(kind):
            if obj.objectName() == name:
                result.append(obj)
        return result
    else:
        return parent.findChildren(kind, name=name)
