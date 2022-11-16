from .PaIRS_pypacks import *

InitCheck=True   #False=Collap closed, True=opened
#fonts
font_italic=True
font_weight=QFont.DemiBold
backgroundcolor_changing=" background-color: rgb(255,230,230);"
color_changing="color: rgb(33,33,255); "+backgroundcolor_changing
color_changing_black="color: rgb(0,0,0); "+backgroundcolor_changing

def setSS(b,style):
    if type(b)==QLabel:
        ss="QLabel{"+style+"}"
    elif type(b)==QLineEdit:
        ss="QLineEdit{"+style+"}"
    else:
        ss=style
    return ss


class MyTabLabel(QtWidgets.QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        #self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.addfuncclick={}

    def mousePressEvent(self, event):
        for f in self.addfuncclick:
             self.addfuncclick[f]()
        return super().mousePressEvent(event)

#MyQLineEdit=QtWidgets.QLineEdit
class MyQLineEdit(QtWidgets.QLineEdit):
    def __init__(self,parent):
        super().__init__(parent)
        self.addlab=QtWidgets.QLabel()
        self.addwid=[]
        self.initFlag=True
        self.addfuncin={}#{'funcout': self.defaultFunc}
        self.addfuncout={}#{'funcout': self.defaultFunc}
        self.addfuncreturn={}#{'funcout': self.defaultFunc}
        
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event) # fundamental to preserve classical behaviour before adding the below
        self.showCompleter()

    def setup(self):
        if self.initFlag:
            self.initFlag=False
            self.font_changing = QtGui.QFont(self.font())
            self.font_changing.setItalic(font_italic)
            self.font_changing.setWeight(font_weight)
            children=self.parent().children()[:]
            self.bros=children+self.addwid
            for b in self.bros:
                if hasattr(b,'setStyleSheet'):
                    b.flagS=True
                    b.initialStyle=b.styleSheet()
                    b.setEnabled(False)
                    b.disabledStyle=b.styleSheet()
                    b.setEnabled(True)
                    b.setStyleSheet(setSS(b,b.initialStyle))
                else:
                    b.flagS=False
                if hasattr(b,'setFont'):
                    b.flagF=True
                    b.initialFont=b.font()
                else:
                    b.flagF=False


    def setup2(self):
        for b in self.bros:
            if hasattr(b,'bros'):
                self.bros=self.bros+b.bros
        self.bros=[*set(self.bros)]

    def focusInEvent(self, event):
        super().focusInEvent(event)
        for f in self.addfuncin:
            self.addfuncin[f]()
        self.focusInFun()
    
    def setFocus(self):
        super().setFocus()
        self.focusInFun()

    def focusInFun(self):
        self.showCompleter()
        if not self.font()==self.font_changing:
            self.setStyleSheet(setSS(self,self.initialStyle+" "+color_changing))
            self.setFont(self.font_changing)
            for b in self.bros:
                if (not b==self) and b.flagS:
                        b.setStyleSheet(setSS(b,b.initialStyle+" "+color_changing_black))
                 
    def focusOutEvent(self, event):
        super().focusOutEvent(event) # fundamental to preserve classical behaviour before adding the below
        for f in self.addfuncout:
            self.addfuncout[f]()
        self.focusOutFun()

    def clearFocus(self):
        super().clearFocus()
        self.focusOutFun()

    def focusOutFun(self):
        if self.font()==self.font_changing:
           for b in self.bros:
                if b.flagS:
                    b.setStyleSheet(setSS(b,b.initialStyle))
                if b.flagF:
                    b.setFont(b.initialFont)
        self.addlab.clear()
            
    def showCompleter(self):
        if self.completer():
            self.completer().complete()

class MyQLineEditNumber(MyQLineEdit):
    def __init__(self,parent):
        super().__init__(parent)       

    def keyPressEvent(self, event):
        #print(event.key())
        if event.key() in (32, #space
            44, #comma 
            16777219,16777223, #del, canc
            16777234,16777236, #left, right
            16777220 #return
            ) \
            or (event.key()>=48 and event.key()<=57):
            super().keyPressEvent(event)
        if event.key()==16777220:
            for f in self.addfuncreturn:
                self.addfuncreturn[f]()
        
class MyQCombo(QtWidgets.QComboBox):
    def wheelEvent(self, event):
        event.ignore()

#MyQSpin=QtWidgets.QSpinBox
class MyQSpin(QtWidgets.QSpinBox):
    def __init__(self,parent):
        super().__init__(parent)
        self.addwid=[]
        self.initFlag=True
        self.addfuncin={}#{'funcout': self.defaultFunc}
        self.addfuncout={}#{'funcout': self.defaultFunc}
        self.addfuncreturn={}#{'funcout': self.defaultFunc}
        
        self.setAccelerated(True)

    def defaultFunc(self):
        return

    def setup(self): 
        if self.initFlag:
            self.initFlag=False
            self.font_changing = QtGui.QFont(self.font())
            self.font_changing.setItalic(font_italic)
            self.font_changing.setWeight(font_weight)
            self.bros=[self]+self.addwid
            for b in self.bros:
                b.initialStyle=b.styleSheet()
                b.initialFont=b.font()

    def focusInEvent(self, event):
        super().focusInEvent(event) # fundamental to preserve classical behaviour before adding the below
        for f in self.addfuncin:
            self.addfuncin[f]()
        if not self.font()==self.font_changing:
           for b in self.bros:
                b.setStyleSheet(b.initialStyle+" "+color_changing)
                b.setFont(self.font_changing)

    def focusOutEvent(self, event):
        super().focusOutEvent(event) # fundamental to preserve classical behaviour before adding the below
        for f in self.addfuncout:
            self.addfuncout[f]()
        if self.font()==self.font_changing:
            for b in self.bros:
                b.setStyleSheet(b.initialStyle)
                b.setFont(b.initialFont)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key()==16777220:
            for f in self.addfuncreturn:
                self.addfuncreturn[f]()
    
    def wheelEvent(self, event):
        event.ignore()

class MyQSpinXW(MyQSpin):
    def __init__(self,parent):
        super().__init__(parent)
        self.Win=-1

    def focusInEvent(self, event):
        super().focusInEvent(event) # fundamental to preserve classical behaviour before adding the below
        if len(self.addwid)>0:
            self.Win=self.addwid[0].value()

class MyToolButton(QtWidgets.QToolButton):
    def __init__(self,parent):
        super().__init__(parent)

class MyQDoubleSpin(QtWidgets.QDoubleSpinBox):
    def __init__(self,parent):
        super().__init__(parent)
        self.addwid=[]
        self.initFlag=True
        self.addfuncin={}#{'funcout': self.defaultFunc}
        self.addfuncout={}#{'funcout': self.defaultFunc}
        self.addfuncreturn={}#{'funcout': self.defaultFunc}

        self.setAccelerated(True)

    def setup(self): 
        if self.initFlag:
            self.initFlag=False
            self.font_changing = QtGui.QFont(self.font())
            self.font_changing.setItalic(font_italic)
            self.font_changing.setWeight(font_weight)
            self.bros=[self]+self.addwid
            for b in self.bros:
                b.initialStyle=b.styleSheet()
                b.initialFont=b.font()

    def focusInEvent(self, event):
        super().focusInEvent(event) # fundamental to preserve classical behaviour before adding the below
        for f in self.addfuncin:
            self.addfuncin[f]()
        if not self.font()==self.font_changing:
           for b in self.bros:
                b.setStyleSheet(b.initialStyle+" "+color_changing)
                b.setFont(self.font_changing)

    def focusOutEvent(self, event):
        super().focusOutEvent(event) # fundamental to preserve classical behaviour before adding the below
        for f in self.addfuncout:
            self.addfuncout[f]()
        if self.font()==self.font_changing:
            for b in self.bros:
                b.setStyleSheet(b.initialStyle)
                b.setFont(b.initialFont)
    
    def wheelEvent(self, event):
        event.ignore()

class CollapsibleBox(QtWidgets.QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initFlag=True
        self.FlagPush=False
        self.dpix=5

    def setup(self,*args):
        if self.initFlag:
            if len(args):
                self.ind=args[0]
                self.stretch=args[1]
            else:
                self.ind=-1
                self.stretch=0
            self.initFlag=False
            self.toggle_button=self.findChild(QtWidgets.QToolButton)
            self.content_area=self.findChild(QtWidgets.QGroupBox)
            self.push_button=self.findChild(MyToolButton)

            self.content_area.setStyleSheet("QGroupBox{border: 1px solid gray; border-radius: 6px;}")
            self.OpenStyle=\
            "QToolButton { border: none; }\n"+\
            "QToolButton::hover{color: rgba(0,0,255,200);}"+\
            "QToolButton::focus{color: rgba(0,0,255,200);}"
            #"QToolButton::hover{border: none; border-radius: 6px; background-color: rgba(0, 0,128,32); }"
            self.ClosedStyle=\
            "QToolButton { border: 1px solid lightgray; border-radius: 6px }\n"+\
            "QToolButton::hover{ border: 1px solid rgba(0,0,255,200); border-radius: 6px; color: rgba(0,0,255,200);}"+\
            "QToolButton::focus{ border: 1px solid rgba(0,0,255,200); border-radius: 6px; color: rgba(0,0,255,200);}" #background-color: rgba(0, 0,128,32); }" 
            self.toggle_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

            self.heightToogle=self.toggle_button.minimumHeight()
            self.heightOpened=self.minimumHeight()
            self.heightArea=self.heightOpened-20
            self.toggle_button.clicked.connect(self.on_click)    
            self.toggle_button.setChecked(InitCheck)
            self.on_click()
            

    #@QtCore.pyqtSlot()
    def on_click(self):
        checked = self.toggle_button.isChecked()
        if checked:
            self.content_area.show()
            if self.FlagPush: 
                self.push_button.show()
            else:
                self.push_button.hide()
            self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
           
            self.toggle_button.setMinimumHeight(self.heightToogle)
            self.toggle_button.setMaximumHeight(self.heightToogle)
            self.setMinimumHeight(self.heightOpened)
            self.setMaximumHeight(int(self.heightOpened*1.5))
            self.content_area.setMinimumHeight(self.heightArea)
            self.content_area.setMaximumHeight(int(self.heightArea*1.5))

            self.toggle_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
            self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

            self.toggle_button.setStyleSheet(self.OpenStyle)
            if self.ind>0:
                self.parent().layout().setStretch(self.ind,self.stretch)
        else:
            
            self.content_area.hide()
            self.push_button.hide()
            self.toggle_button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
            
            self.toggle_button.setMinimumHeight(self.heightToogle+self.dpix)
            self.toggle_button.setMaximumHeight(self.heightToogle+self.dpix)
            self.setMinimumHeight(self.heightToogle+self.dpix*2)
            self.setMaximumHeight(self.heightToogle+self.dpix*2)
            self.content_area.setMinimumHeight(0)
            self.content_area.setMaximumHeight(0)

            self.toggle_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
            
            self.toggle_button.setStyleSheet(self.ClosedStyle)
            
            if self.ind>0:
                self.parent().layout().setStretch(self.ind,0)



class myQTreeWidget(QTreeWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.addfuncin={}#{'funcout': self.defaultFunc}
        self.addfuncout={}#{'funcout': self.defaultFunc}
        self.addfuncreturn={}#{'funcout': self.defaultFunc}

    def focusOutEvent(self, event):
        super().focusOutEvent(event) # fundamental to preserve classical behaviour before adding the below
        #self.setCurrentItem(QTreeWidgetItem())
        for f in self.addfuncout:
            self.addfuncout[f]()



        
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as pyplt
import matplotlib.image as mplimage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure as mplFigure
from mpl_toolkits.axes_grid1 import make_axes_locatable
 
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=8, height=8, dpi=100):
        self.fig = mplFigure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
