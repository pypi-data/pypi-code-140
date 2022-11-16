from .ui_Log_Tab import*
from .PaIRS_pypacks import*
from .addwidgets_ps import*

class Log_Tab(QWidget):

    def __init__(self,parent):
        super().__init__(parent)

        ui=Ui_LogTab()
        ui.setupUi(self)

        font=self.font()
        font.setFamily(fontName)
        self.setFont(font)
        c=self.findChildren(QObject)
        for w in c:
            if hasattr(w,'setFont'):
                font=w.font()
                font.setFamily(fontName)
                w.setFont(font)
        self.ui=ui

        
        ui.log.setText('')
        self.logWrite('Welcome to PaIRS interface!\nEnjoy it!\n\n')


    def logWrite(self, text):
        cursor = self.ui.log.textCursor() 
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.log.setTextCursor(cursor)
        self.ui.log.ensureCursorVisible()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Log_Tab(None)
    object.show()
    sys.exit(app.exec())
