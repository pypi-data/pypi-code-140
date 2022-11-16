from .gPaIRS import *

def PaIRS():
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = gPaIRS()
    #object.show()
    sys.exit(app.exec())
