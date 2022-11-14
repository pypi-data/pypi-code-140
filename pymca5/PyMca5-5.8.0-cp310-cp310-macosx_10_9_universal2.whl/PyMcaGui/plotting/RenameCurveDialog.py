#/*##########################################################################
# Copyright (C) 2004-2015 V.A. Sole, European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
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
#############################################################################*/
__author__ = "V.A. Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
from PyMca5.PyMcaGui import PyMcaQt as qt

class RenameCurveDialog(qt.QDialog):
    def __init__(self, parent = None, current="", curves = []):
        qt.QDialog.__init__(self, parent)
        self.setWindowTitle("Rename Curve %s" % current)
        self.curves = curves
        layout = qt.QVBoxLayout(self)
        self.lineEdit = qt.QLineEdit(self)
        self.lineEdit.setText(current)
        self.hbox = qt.QWidget(self)
        self.hboxLayout = qt.QHBoxLayout(self.hbox)
        self.hboxLayout.addWidget(qt.HorizontalSpacer(self.hbox))
        self.okButton    = qt.QPushButton(self.hbox)
        self.okButton.setText('OK')
        self.hboxLayout.addWidget(self.okButton)
        self.cancelButton = qt.QPushButton(self.hbox)
        self.cancelButton.setText('Dismiss')
        self.hboxLayout.addWidget(self.cancelButton)
        self.hboxLayout.addWidget(qt.HorizontalSpacer(self.hbox))
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.hbox)
        self.okButton.clicked.connect(self.preAccept)
        self.cancelButton.clicked.connect(self.reject)

    def preAccept(self):
        text = str(self.lineEdit.text())
        addedText = ""
        if len(text):
            if text not in self.curves:
                self.accept()
                return
            else:
                addedText = "Curve already exists."
        text = "Invalid Curve Name"
        msg = qt.QMessageBox(self)
        msg.setIcon(qt.QMessageBox.Critical)
        msg.setWindowTitle(text)
        text += "\n%s" % addedText
        msg.setText(text)
        msg.exec()

    def getText(self):
        return str(self.lineEdit.text())


if __name__ == "__main__":
   app = qt.QApplication([])
   w=RenameCurveDialog(None, 'curve1', ['curve1', 'curve2', 'curve3'])
   ret = w.exec()
   if ret == qt.QDialog.Accepted:
       print("newcurve = %s" % str(w.lineEdit.text()))
   else:
       print("keeping old curve")
