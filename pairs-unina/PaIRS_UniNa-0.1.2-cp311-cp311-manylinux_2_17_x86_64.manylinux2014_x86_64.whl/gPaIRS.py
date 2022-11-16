from .ui_gPairs import *
from .ui_infoPaIRS import *
from .gPaIRS_threads import *
from .calcMin_threads import *
from .PaIRS_pypacks import *
from .addwidgets_ps import *
from .__init__ import __version__

version=__version__
#version='0.1.0'
lastcfgname=foldPaIRS+'lastuicfg.pairs.cfg'
NUMTHREADS_gPaIRS=1
#NUMTHREADS_PIV=cpu_count(logical=False)-1
NUMTHREADS_PIV=cpu_count(logical=True)-2
if NUMTHREADS_PIV<1: NUMTHREADS_PIV=1
Flag_GRAPHICS=False
Flag_UNDOCKWDIGETS=False

class treeToSave:
    def __init__(self,TREpar):
        self.ind=[]
        self.name=[]
        self.data=[]
        self.icon=[]

        for j,n in enumerate(('past','current','future')):
            indj=j-1
            for i in getattr(TREpar,n):
                self.ind.append(indj)
                self.name.append(i.text(0))
                self.data.append(i.data(0,Qt.UserRole))

class itemTreePar:
    def __init__(self,name,typeW):
        self.name=name
        self.icon=''
        self.typeW=typeW
        self.flagRun=0  #0:not launched yet, 1:completed, -1:interrupted
        self.PIVpar=PIVpar()
        self.MINpar=MINpar()
        self.Log=''

class GPApar:
    def __init__(self):
        self.name        		= ''    
        self.FlagUndocked       = False
        self.FlagAllTabs 		= True                   
        self.lastTab    		= 0    
        self.FlagInput          = True
        self.FlagOutput         = True
        self.FlagProcess        = True
        self.FlagLog            = True
        self.FlagVis            = True    
    
        self.fields={}
        for f,v in self.__dict__.items():
            if f!='fields':
                self.fields[f]=v

    def printPar(self):
            myprint(self.fields)

    def duplicate(self):
        newist=GPApar()
        for a in self.fields:
            setattr(newist,a,getattr(self,a))
        newist.setFields()
        return newist

    def copyfrom(self,newist):
        for a in self.fields:
            setattr(self,a,getattr(newist,a))
        self.setFields()

    def copyfromdiz(self,newist,diz):
        for a in diz:
            setattr(self,a,getattr(newist,a))
        self.setFields()

    def setFields(self):
        for f in self.fields:
            self.fields[f]=getattr(self,f)

class uiGPApar(GPApar):

    class _ReactingProp:
        def __init__(self, name_value):
            self.name=name_value[0]
            self.value=name_value[1]
        def __get__(self, instance, owner=None):
            return self.value
        def __set__(self, instance, value):
            if type(value) is np.ndarray:
                check=False
                if np.size(value)!=np.size(self.value):
                    check=True
                else:
                    check=any(value!=self.value)
            else:
                check=value != self.value
            if check:
                self.value = value
                instance.fields[self.name]=value
                if instance.FlagAddFunc:
                    for f in instance.addfunc:
                        instance.addfunc[f](self.name)
                
    def __init__(self):
        super().__init__()
        fields=GPApar().fields
        fields_to_del=[]
        for f in self.fields:
            if not f in fields:
                fields_to_del.append(f)
        for f in fields_to_del:
            del self.fields[f]
        self.FlagAddFunc=False
        self.FlagAddGPApar=True
        self.addfunc={}
        for field, value in self.fields.items():
            setattr(self, field, self._ReactingProp([field, value]))
            setattr(self, field, value)

class FloatingObject(QMainWindow):
        def closeEvent(self, event):
            if not self.gui.GPApar.FlagUndocked: return
            if self.FlagDockAll:
                self.gui.button_dock_callback()
            else:
                self.button.setChecked(False)
                setattr(self.gui.GPApar,'Flag'+self.name,False)
                self.hide()   
            
        def __init__(self,parent,tab,FlagShow,FlagDockAll,xshift,*args):
            super().__init__()
            self.gui=parent
            self.name=''
            self.button=None
            self.tab=tab
            self.FlagShow=FlagShow
            self.FlagDockAll=FlagDockAll
            self.setup(xshift,args)
            
        def setup(self,xshift,*args):
            if len(args): flag=args[0]
            else: flag=True
            tab=self.tab
            FlagHeight=False
            if type(tab)==CollapsibleBox:
                self.setWindowTitle(tab.toggle_button.text())
                self.setWindowIcon(self.gui.windowIcon())
                parent=tab
            elif tab.objectName()=='f_VisTab':
                self.name=self.gui.ui.name_tab.text().replace(' ','')
                self.setWindowTitle(self.name)
                self.setWindowIcon(self.gui.ui.icon.pixmap())
                parent=tab
                FlagHeight=flag
            elif type(tab) in (Import_Tab,Export_Tab,Process_Tab,Tree_Tab,Log_Tab):
                self.name=tab.ui.name_tab.text().replace(' ','')
                self.setWindowTitle(tab.ui.name_tab.text())
                self.setWindowIcon(tab.ui.icon.pixmap())
                parent=tab.parent()
                FlagHeight=flag
            else:
                self.setWindowTitle(self.gui.windowTitle())
                self.setWindowIcon(self.gui.windowIcon())
                parent=tab
            #layout = QVBoxLayout()
            #layout.addWidget(parent)
            #layout.setContentsMargins(0,0,0,0)
            #layout.setStretch(0,1)
            #self.setLayout(layout)
            if type(parent.parent()) in (QSplitter,QLayout):
                self.lay=parent.parent()
            else:
                self.lay=parent.parent().layout()
            self.setCentralWidget(parent)
            geo=parent.geometry()
            geoP=self.gui.geometry()
            x=geoP.x()+int(geoP.width()*0.5)-int(geo.width()*0.5)+xshift
            y=geoP.y()+int(geoP.height()*0.5)-int(geo.height()*0.5)
            if FlagHeight:
                self.setGeometry(x,y,geo.width(),geoP.height())
            else:
                self.setGeometry(x,y,geo.width(),geo.height())
            #self.setGeometry(x,y,geo.width(),geo.height())
            self.setBaseSize(parent.baseSize())
            self.setAutoFillBackground(False) 
            self.setMaximumWidth(parent.maximumWidth())
            self.setMinimumWidth(parent.minimumWidth())
            parent.show()
            self.pa=parent

            if self.FlagShow:
                self.show()

            if self.name:
                self.button=getattr(self.gui.ui,'button_'+self.name)

class FloatingWidget(FloatingObject):
        def closeEvent(self, event):
            self.lay.addWidget(self.pa)
            self.close()
            

class infoPaIRS(QMainWindow):
    def __init__(self):
        super().__init__()
        ui=Ui_InfoPaiRS()
        ui.setupUi(self)
        self.ui=ui

class gPaIRS(QMainWindow):       
    
    def closeEvent(self, event):
        self.hide()
        if type(event)==bool:
            if event:
                self.closeAll()
        else:
            if not self.FlagRun:
                self.save_uicfg(lastcfgname)
                self.closeAll()
            else:
                self.Closing=True
                self.signals.kill.emit()

    def closeAll(self):
        if hasattr(self,"floatings"):
            for w in self.floatings:
                w.close()
        if hasattr(self,"floatw"):
            for w in self.floatw:
                w.close()
        self.close()

    class gPaIRS_signals(QObject):
        kill=Signal()
        goOn=Signal(int)
        indProc=Signal(int)
        stopped=Signal()

    def __init__(self):
        super().__init__()

        self.signals=self.gPaIRS_signals()
        self.Stopped=True
        self.Closing=False
        self.signals.stopped.connect(self.stopProcs)
        
        ui=Ui_gPairs()
        ui.setupUi(self)
        self.ui=ui
        self.setWindowTitle(f'PaIRS (v{version})')

        font=self.font()
        font.setFamily(fontName)
        self.setFont(font)
        c=self.findChildren(QObject)
        for w in c:
            if hasattr(w,'setFont'):
                font=w.font()
                font.setFamily(fontName)
                w.setFont(font)
            if hasattr(w,'statusTip'):
                w.setStatusTip(w.toolTip())
        logfont=self.font()
        #logfont.setFamily('Consolas')
        logfont.setFamily('Courier')
        logfont.setPointSize(10)
        ui.w_LogTab.ui.log.setFont(logfont)
        #self.ui.f_Tree_Process.hide()
        
        #for callbacks
        self.ui.w_ExportTab.OUTpar.x=self.ui.w_ImportTab.INPpar.x
        self.ui.w_ExportTab.OUTpar.y=self.ui.w_ImportTab.INPpar.y
        self.ui.w_ExportTab.OUTpar.w=self.ui.w_ImportTab.INPpar.w
        self.ui.w_ExportTab.OUTpar.h=self.ui.w_ImportTab.INPpar.h
        self.ui.w_ExportTab.OUTpar.W=self.ui.w_ImportTab.INPpar.W
        self.ui.w_ExportTab.OUTpar.H=self.ui.w_ImportTab.INPpar.H
        self.ui.w_ExportTab.setOUTpar()
        self.ui.w_ImportTab.ParPointer=self.ui.w_ExportTab.OUTpar
        self.ui.w_ImportTab.ui.spin_x=self.ui.w_ExportTab.ui.spin_x
        self.ui.w_ImportTab.ui.spin_y=self.ui.w_ExportTab.ui.spin_y
        self.ui.w_ImportTab.ui.spin_w=self.ui.w_ExportTab.ui.spin_w
        self.ui.w_ImportTab.ui.spin_h=self.ui.w_ExportTab.ui.spin_h
        self.ui.w_ImportTab.ui.w_SizeImg.hide()
        self.ui.w_ImportTab.signals.update_par.connect(self.updateOUTpar_prev)

        self.ui.w_ImportTab.ui.edit_path.textChanged.connect(self.change_edit_path)

        color_tuple=(0.95,0.95,0.95,0)
        clrgb=[int(i*255) for i in color_tuple]
        self.ui.plot.fig.set_facecolor(color_tuple)
        #self.ui.f_Vis.setStyleSheet(self.ui.f_Vis.styleSheet()+\
        #'QFrame{background-color:'+ f'rgba({clrgb[0]},{clrgb[1]},{clrgb[2]},{clrgb[3]})' +'}')
        self.ui.w_ImportTab.ui.spin_selected.valueChanged.connect(\
            lambda: self.update_image_on_interaction(self.ui.w_ImportTab.ui.spin_selected))
        self.ui.w_ImportTab.ui.spin_frame.valueChanged.connect(\
            lambda: self.update_image_on_interaction(self.ui.w_ImportTab.ui.spin_frame))
        self.ui.w_ImportTab.ui.list_images.currentRowChanged.connect(\
            lambda: self.update_image_on_interaction(self.ui.w_ImportTab.ui.list_images))
        for s in self.ui.w_ExportTab.ui.spins:
            if s.objectName() in ('spin_x','spin_y','spin_h','spin_w'):
                s.addfuncout['spin_update_image']=lambda sp=s: self.spin_update_image(sp)      
                #s.valueChanged.connect(self.update_image)
        self.ui.w_ExportTab.ui.button_resize.clicked.connect(self.update_image)
        self.ui.w_ExportTab.ui.button_rot_clock.clicked.connect(self.update_image)
        self.ui.w_ExportTab.ui.button_rot_counter.clicked.connect(self.update_image)
        self.ui.w_ExportTab.ui.button_mirror_x.clicked.connect(self.update_image)
        self.ui.w_ExportTab.ui.button_mirror_y.clicked.connect(self.update_image)
        self.ui.w_ExportTab.ui.button_reset_rot_flip.clicked.connect(self.update_image)

        for s in self.ui.w_ProcessTab.ui.edits:
            s.addfuncin['update_image_Win']=self.update_image_Wind 
            s.addfuncreturn['update_image_Win']=self.update_image_Wind       
            s.addfuncout['update_image_Win']=self.update_image          
            #s.valueChanged.connect(self.update_image)

        self.icon_docked = QIcon()
        self.icon_docked.addFile(u""+ icons_path +"menu_docked.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_vert = QIcon()
        self.icon_vert.addFile(u""+ icons_path +"menu_vert.png", QSize(), QIcon.Normal, QIcon.Off)
        
        self.icon_dock_tabs = QIcon()
        self.icon_dock_tabs.addFile(u""+ icons_path +"dock_tabs.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_undock_tabs = QIcon()
        self.icon_undock_tabs.addFile(u""+ icons_path +"undock_tabs.png", QSize(), QIcon.Normal, QIcon.Off)

        self.FlagRun=False
        self.GPApar_base=GPApar()
        self.GPApar=uiGPApar()

        self.widnames=['Input','Output','Process','Log','Vis']
        self.tabnames=['Import','Export','Process','Log','Vis'] #+'Tab'
        for j,wn in enumerate(self.widnames):
            if self.GPApar.FlagAllTabs:
                setattr(self.GPApar,"Flag"+wn,True)
            else:
                if j: setattr(self.GPApar,"Flag"+wn,False)
                else: setattr(self.GPApar,"Flag"+wn,True)
        ui.button_Input.clicked.connect(lambda: self.button_Tab_callback('Input'))
        ui.button_Output.clicked.connect(lambda: self.button_Tab_callback('Output'))
        ui.button_Process.clicked.connect(lambda: self.button_Tab_callback('Process'))
        ui.button_Log.clicked.connect(lambda: self.button_Tab_callback('Log'))
        ui.button_Vis.clicked.connect(lambda: self.button_Tab_callback('Vis'))
        ui.button_Shape.clicked.connect(self.button_Shape_callback)
        ui.button_dock.clicked.connect(self.button_dock_callback)
        
        self.createMainSplitter()
        self.createSecondarySplitter()

        self.checkTabs()
        self.ui.button_delete.hide()
        self.ui.button_pause.hide()
        self.ui.progress_Proc.hide()
        
        self.PaIRS_threadpool=QThreadPool()
        if NUMTHREADS_gPaIRS:
            self.PaIRS_threadpool.setMaxThreadCount(NUMTHREADS_gPaIRS)
        self.NumThreads= self.PaIRS_threadpool.maxThreadCount() 

        self.PIV_manager=[]
        self.workers=[]
        
        toolbar = NavigationToolbar(self.ui.plot, self)
        self.ui.lay_w_Plot.addWidget(toolbar)
        self.flagInitImg=False
        self.ui.w_ImportTab.signals.set_Image_List.connect(self.createFig)
        self.hide()
        self.flagBeginning=True
        self.ui.w_ImportTab.signals.set_Image_List.connect(self.initLastCfg)
        
        self.ui.w_Tree.clearTree()
        self.ui.w_Tree.signals.selection.connect(self.updateGuiFromTree)
        self.ui.w_Tree.selectCurrent()

        self.ui.w_ImportTab.ui.check_subtract_2.show()
        self.ui.w_ImportTab.ui.button_min.hide()

        self.ui.w_Tree.ui.button_min.clicked.connect(lambda: self.addProc(self.addMinProc))
        self.ui.w_Tree.ui.button_PIV.clicked.connect(lambda: self.addProc(self.addPIVProc))
        self.ui.w_ImportTab.signals.pause_calcMin.disconnect()
        self.ui.w_ImportTab.signals.completed_calcMin.disconnect()
        self.ui.w_ImportTab.signals.completed_calcMin.connect(self.finish_MINproc)

        self.Im_min_a=np.array([])
        self.Im_min_b=np.array([])
        self.ui.w_ImportTab.list_pim=[]

        ui.button_Run.clicked.connect(self.button_pause_callback)
        ui.button_pause.clicked.connect(self.button_pause_callback)
        ui.button_delete.clicked.connect(self.button_delete_callback)

        ui.actionNew.triggered.connect(self.new_uicfg)
        ui.actionSave.triggered.connect(self.save_uicfg)
        ui.actionLoad.triggered.connect(self.load_uicfg)
        ui.aExit.triggered.connect(self.close)
        ui.actionAbout.triggered.connect(self.about)
        ui.actionGuide.triggered.connect(self.guide)

        self.minW=self.centralWidget().minimumWidth()
        self.maxW=self.centralWidget().maximumWidth()

        self.ui.w_ProcessTab.ui.w_Nogueira.hide()

    
    def createMainSplitter(self):
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.ui.w_Managing_Tabs)
        self.main_splitter.addWidget(self.ui.w_Operating_Tabs)
        self.main_splitter.setCollapsible(0,False)
        self.main_splitter.setCollapsible(1,False)
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 1)
        self.ui.main_lay.addWidget(self.main_splitter)

    def createSecondarySplitter(self):
        self.secondary_splitter = QSplitter(Qt.Horizontal)
        for i,wn in enumerate(self.tabnames):
            wdgt=getattr(self.ui,f'f_{wn}Tab')
            self.secondary_splitter.addWidget(wdgt)
            self.secondary_splitter.setCollapsible(i,False)
        self.secondary_splitter.addWidget(self.ui.f_empty)
        self.secondary_splitter.setCollapsible(i+1,False)
        self.ui.flay.addWidget(self.secondary_splitter)

#*************************************************** Menus
    def contextMenuEvent(self, event):
        
        if Flag_UNDOCKWDIGETS:
            contextMenu = QMenu(self)
            extract = contextMenu.addAction("Undock a widget")
            action = contextMenu.exec(self.mapToGlobal(event.pos()))
            if action == extract:
                self.gettext()

    def gettext(self):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setWindowTitle("Undock a widget")
        dialog.setLabelText("Enter the widget name:")
        dialog.setTextValue("")
        le = dialog.findChild(QtWidgets.QLineEdit)
        
        words = ["self.ui.w_ImportTab", "self.ui.w_ExportTab", 
        "self.ui.w_ProcessTab", 
        "self.ui.w_ProcessTab.ui.CollapBox_IntWind",
        "self.ui.w_ProcessTab.ui.CollapBox_FinIt",
        "self.ui.w_ProcessTab.ui.CollapBox_top",
        "self.ui.w_ProcessTab.ui.CollapBox_Interp",
        "self.ui.w_ProcessTab.ui.CollapBox_Validation",
        "self.ui.w_ProcessTab.ui.CollapBox_Windowing",
        "self.ui.f_VisTab", "self.ui.w_Tree","self.ui.w_LogTab",
        "self.ui.w_Buttons"]
        completer = QtWidgets.QCompleter(words, le)
        completer.setCompletionMode(QCompleter.CompletionMode(1))
        le.setCompleter(completer)

        geom = dialog.frameGeometry()
        geom.moveCenter(QtGui.QCursor.pos())
        dialog.setGeometry(geom)
        dialog.resize(500,dialog.height())

        ok, text = (
            dialog.exec() == QtWidgets.QDialog.Accepted,
            dialog.textValue(),
        )

        c=dialog.findChildren(QObject)
        for w in c:
            if hasattr(w,'setFont'):
                font=w.font()
                font.setFamily(fontName)
                w.setFont(font)

        if ok:
            try:
                if not hasattr(self,"floatw"):
                    self.floatw=[]
                ts=text.split('.')
                parent=".".join(ts[:-1])
                child=ts[-1]
                tab=getattr(eval(parent),child)
                self.floatw.append(FloatingWidget(self,tab,True,False,0))
                pass
            except:
                pass

    def guide(self):
        url = QUrl("http://wpage.unina.it/astarita/PaIRS/PaIRS-UniNa-Guide.pdf")
        QDesktopServices.openUrl(url)

    def about(self):
        self.aboutDialog=infoPaIRS()
        infotext=self.aboutDialog.ui.info.text().replace('#.#.#',version)
        self.aboutDialog.ui.info.setText(infotext)

        c=self.aboutDialog.findChildren(QObject)
        for w in c:
            if hasattr(w,'setFont'):
                font=w.font()
                font.setFamily(fontName)
                w.setFont(font)
        self.aboutDialog.show()

    def save_uicfg(self,*args):
        if len(args):
            filename=args[0]
        else:
            filename, _ = QFileDialog.getSaveFileName(QWidget(),\
                "Select location and name of the file to save", 
                    dir=self.ui.w_ImportTab.INPpar.path+"uicfg",\
                    options=QFileDialog.Option.DontUseNativeDialog)
            filename=myStandardRoot('{}'.format(str(filename)))
            if not filename: return
            filename=filename+'.pairs.cfg'
        if os.path.exists(filename) and not len(args):
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            Message='The file already exists. Do you want to overwrite it?'
            dlg.setText(str(Message))

            dlg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            dlg.setIcon(QMessageBox.Warning)
            dlg.setFont(self.font())
            button = dlg.exec()
        else:
            button=QMessageBox.Yes
        if button==QMessageBox.Yes:
            self.updateCurrentItem()
            t=treeToSave(self.ui.w_Tree.TREpar)
            var = [self.GPApar.duplicate(), t]
            filename=myStandardRoot(filename)
            with open(filename, 'wb') as file:
                pickle.dump(var, file)
                myprint(f'\nSaving {filename}')

    def load_uicfg(self,*args):
        if len(args):
            filename=args[0]
        else:
            filename, _ = QFileDialog.getOpenFileName(QWidget(),\
                "Select an image file of the sequence", filter='*.pairs.cfg',\
                    dir=self.ui.w_ImportTab.INPpar.path,\
                    options=QFileDialog.Option.DontUseNativeDialog)
            if not filename: return
        with open(filename, 'rb') as file:
            var = pickle.load(file)
            self.hide()
            self.ui.w_Tree.clearAllTree()
            t=var[1]
            flag0i=True
            for i in range(len(t.ind)):
                if not t.ind[i]:
                    self.ui.w_ImportTab.INPpar_prev[0].copyfrom(t.data[i].PIVpar.INP)
                    self.ui.w_ExportTab.OUTpar_prev[0].copyfrom(t.data[i].PIVpar.OUT)
                    self.ui.w_ProcessTab.PROpar_prev[0].copyfrom(t.data[i].PIVpar.PRO)
                icon,flag0i=self.detIcon(t.ind[i],t.data[i].flagRun,flag0i)
                self.ui.w_Tree.TREpar.addItem2Tree(t.ind[i],\
                t.name[i],t.data[i],icon)
            self.ui.w_Tree.setTREpar()
            self.ui.w_Tree.selectCurrent()
            self.GPApar.copyfrom(var[0])
            self.GPApar.FlagUndocked=False
            self.checkTabs()
            self.show()

    def detIcon(self,ind,flagRun,flag0i):
        icon=QIcon()
        t=self.ui.w_Tree.TREpar
        if ind==-1:
            if flagRun==-1: icon=t.cancelled_Icon
            elif flagRun==+1: icon=t.done_Icon
        elif ind==1: 
            if flag0i: 
                icon=t.running_Icon
                flag0i=False
            else: icon=t.waiting_Icon
        return icon,flag0i

    def new_uicfg(self):
        self.hide()
        self.ui.w_Tree.clearTree()
        self.ui.w_ImportTab.INPpar_prev.clear()
        self.ui.w_ExportTab.OUTpar_prev.clear()
        self.ui.w_ProcessTab.PROpar_prev.clear()
        data=self.ui.w_Tree.TREpar.current[0].data(0,Qt.UserRole)
        self.ui.w_ImportTab.INPpar_prev.append(data.PIVpar.INP)
        self.ui.w_ExportTab.OUTpar_prev.append(data.PIVpar.OUT)
        self.ui.w_ProcessTab.PROpar_prev.append(data.PIVpar.PRO)
        self.ui.w_ImportTab.INPpar_ind=0
        self.ui.w_ImportTab.display_controls()
        self.ui.w_ExportTab.OUTpar_ind=0
        self.ui.w_ExportTab.display_controls()
        self.ui.w_ProcessTab.PROpar_ind=0
        self.ui.w_ProcessTab.display_controls()

        self.flagInitImg=False
        self.ui.w_ImportTab.signals.set_Image_List.connect(self.createFig)
        self.ui.w_Tree.setTREpar()
        self.ui.w_Tree.selectCurrent()
        self.GPApar=GPApar()
        self.checkTabs()
        self.show()

    def initLastCfg(self):
        if self.flagBeginning:
            self.flagBeginning=False
            if os.path.exists(lastcfgname):
                self.load_uicfg(lastcfgname)
            self.show()

#*************************************************** TREE functionalities
    def updateOUTpar_prev(self):
        self.ui.w_ExportTab.OUTpar_prev[0].copyfromdiz(\
            self.ui.w_ImportTab.INPpar_prev[0],('x','y','w','h','W','H'))

    def updateCurrentItem(self):
        name='current'
        typeW=0
        data=itemTreePar(name,typeW)
        data.PIVpar.INP.copyfrom(self.ui.w_ImportTab.INPpar_prev[0])
        data.PIVpar.OUT.copyfrom(self.ui.w_ExportTab.OUTpar_prev[0])
        data.PIVpar.PRO.copyfrom(self.ui.w_ProcessTab.PROpar_prev[0])
        self.ui.w_Tree.ui.tree_current.clear()
        del self.ui.w_Tree.TREpar.current[0]
        self.ui.w_Tree.addItem(0,name,data,QIcon(),False)
        self.ui.w_Tree.TREpar.flagRun=data.flagRun

    @Slot(int,int,QTreeWidgetItem,int)
    def updateGuiFromTree(self,indTree_prev,indTree,item,column):
        if item!=None:
            if indTree==0:
                self.updateCurrentItem()
                item=self.ui.w_Tree.TREpar.current[0]
                item.setSelected(True)   
                self.ui.w_Tree.ui.tree_current.setFocus()
                self.ui.w_Tree.ui.tree_current.setCurrentItem(item)
            if not self.FlagRun:
                if indTree==-1:
                    self.resetProc(self.ui.w_Tree.ui.tree_past)
                    self.setProgressBar(self.ui.w_Tree.ui.tree_past)
                elif indTree==1:
                    self.resetProc(self.ui.w_Tree.ui.tree_future)
                    self.setProgressBar(self.ui.w_Tree.ui.tree_future)
            data=item.data(column,Qt.UserRole)
            #first export since it depends on Import
            self.ui.w_ExportTab.OUTpar.FlagAddOUTpar=False
            self.ui.w_ExportTab.setOUTpar_item(data.PIVpar.OUT)
            self.ui.w_ExportTab.OUTpar.FlagAddOUTpar=True

            self.ui.w_ImportTab.INPpar.FlagAddINPpar=False
            self.ui.w_ImportTab.setINPpar_item(data.PIVpar.INP)
            self.ui.w_ImportTab.INPpar.FlagAddINPpar=True

            self.ui.w_ProcessTab.PROpar.FlagAddPROpar=False
            self.ui.w_ProcessTab.setPROpar_item(data.PIVpar.PRO) 
            self.ui.w_ProcessTab.PROpar.FlagAddPROpar=True
            
            self.ui.w_LogTab.ui.log.setText(data.Log)

            self.ui.w_Tree.TREpar.flagRun=data.flagRun
            self.ui.w_Tree.checkButtons() 
            if data.flagRun==1:
                self.ui.w_Tree.ui.button_restore.hide()
            if len(self.ui.w_Tree.TREpar.future)==0:
                self.ui.button_Run.hide()
                self.ui.button_pause.hide()
                if len(self.ui.w_Tree.TREpar.past)==0 or indTree==0:
                    self.ui.progress_Proc.hide()
                else:
                    self.ui.progress_Proc.show()
            else:
                if indTree==0:
                    self.ui.button_Run.hide()
                    self.ui.progress_Proc.hide()
                    self.ui.button_pause.hide()
                else:
                    if indTree==1 and data.flagRun==0:
                        self.ui.button_Run.show()
                        self.ui.button_pause.hide()
                        self.ui.progress_Proc.hide()
                    else:
                        self.ui.button_Run.hide()
                        self.ui.button_pause.show()
                        if self.FlagRun:
                            self.ui.button_pause.setIcon(self.ui.w_ImportTab.icon_pause)
                        else:
                            self.ui.button_pause.setIcon(self.ui.w_ImportTab.icon_play)
                        self.ui.progress_Proc.show()
                    

    def addMinProc(self):
        typeW=1
        name=f"Minimum computation ({self.ui.w_ImportTab.INPpar.path})"
        data=itemTreePar(name,typeW)
        data.PIVpar.INP.copyfrom(self.ui.w_ImportTab.INPpar)
        data.PIVpar.OUT.copyfrom(self.ui.w_ExportTab.OUTpar)
        data.PIVpar.PRO.copyfrom(self.ui.w_ProcessTab.PROpar)

        data.MINpar.path=data.PIVpar.INP.path
        ind_in=data.PIVpar.INP.range_from*2
        ind_fin=(data.PIVpar.INP.range_to+1)*2
        data.MINpar.list_Image_Files=copy.deepcopy(self.ui.w_ImportTab.list_Image_Files[ind_in:ind_fin])
        data.MINpar.list_eim=copy.deepcopy(self.ui.w_ImportTab.list_eim[ind_in:ind_fin])
        data.MINpar.list_pim=[0*int(i) for i in data.MINpar.list_eim]
        data.MINpar.flag_TR=data.PIVpar.INP.flag_TR
        data.MINpar.i=-1
        
        if data.MINpar.flag_TR:
            data.MINpar.nimg_proc=int(len(data.MINpar.list_Image_Files)/2)+1
        else:
            data.MINpar.nimg_proc=len(data.MINpar.list_Image_Files)
        data.MINpar.NumThreads=min([self.NumThreads, data.MINpar.nimg_proc])
        
        if len(self.ui.w_Tree.TREpar.future):
            self.ui.w_Tree.addItem(1,data.name,data,self.ui.w_Tree.TREpar.waiting_Icon)
        else:
            self.ui.w_Tree.addItem(1,data.name,data,self.ui.w_Tree.TREpar.running_Icon)

    def addPIVProc(self):
        typeW=2
        name=f"PIV computation ({self.ui.w_ImportTab.INPpar.path})"
        data=itemTreePar(name,typeW)
        data.PIVpar.INP.copyfrom(self.ui.w_ImportTab.INPpar)
        data.PIVpar.OUT.copyfrom(self.ui.w_ExportTab.OUTpar)
        data.PIVpar.PRO.copyfrom(self.ui.w_ProcessTab.PROpar)
        ind_in=self.ui.w_ImportTab.INPpar.range_from*2
        ind_fin=(self.ui.w_ImportTab.INPpar.range_to+1)*2
        data.PIVpar.list_Image_Files=copy.deepcopy(self.ui.w_ImportTab.list_Image_Files[ind_in:ind_fin])
        data.PIVpar.list_eim=copy.deepcopy(self.ui.w_ImportTab.list_eim[ind_in:ind_fin])
        data.PIVpar.i=-1
        
        data.PIVpar.nimg=int(len(data.PIVpar.list_Image_Files)/2)
        data.PIVpar.list_pim=[]
        for i in range(data.PIVpar.nimg):
            data.PIVpar.list_pim.append(0)
        
        data.PIVpar.NumThreads=min([self.NumThreads, data.PIVpar.nimg])
        if data.PIVpar.NumThreads==2: data.PIVpar.NumThreads=1
        data.PIVpar.NumThreads_PIV=NUMTHREADS_PIV

        if len(self.ui.w_Tree.TREpar.future):
            self.ui.w_Tree.addItem(1,data.name,data,self.ui.w_Tree.TREpar.waiting_Icon)
        else:
            self.ui.w_Tree.addItem(1,data.name,data,self.ui.w_Tree.TREpar.running_Icon)

    def run(self):
        self.Stopped=False
        self.ui.w_Tree.FlagPause=False
        self.ui.progress_Proc.show()
        self.ui.button_pause.setIcon(self.ui.w_ImportTab.icon_pause)
        self.ui.button_pause.show()
        
        #self.ui.button_delete.show()
        self.ui.button_Run.hide()
        self.ui.w_Tree.ui.tree_future.setCurrentItem(self.ui.w_Tree.TREpar.future[0])
        self.ui.w_Tree.TREpar.indTree=self.ui.w_Tree.selectTree(\
            self.ui.w_Tree.ui.tree_future)
        self.ui.w_Tree.ui.tree_future.setFocus()
        self.initializeWorkers()
        self.resetProc(self.ui.w_Tree.ui.tree_future)
        self.setProgressBar(self.ui.w_Tree.ui.tree_future)
        self.indProc=0
        self.signals.indProc.emit(self.indProc)

    def updateIndProc(self):
        self.UpdatingImage=True
        i=self.ui.w_Tree.TREpar.future[0] #.currentItem()
        data=i.data(0,Qt.UserRole)
        data.flagRun=1
        self.ui.w_Tree.TREpar.flagRun=data.flagRun
        self.ui.w_Tree.removeFromTree()

        if len(self.ui.w_Tree.TREpar.future):
            i=self.ui.w_Tree.TREpar.future[0]
            data=i.data(0,Qt.UserRole)
            self.resetProc(self.ui.w_Tree.ui.tree_future)
            self.setProgressBar(self.ui.w_Tree.ui.tree_future)
            self.indProc+=1
            self.signals.indProc.emit(self.indProc)
        else:
            self.button_delete_callback()
            self.ui.w_Tree.selectCurrent()

    def resetProc(self,tree):
        i=tree.currentItem()#TREpar.future[0]
        data=i.data(0,Qt.UserRole)
        if data.typeW==1: #minimum
            par=data.MINpar
            self.list_pim=par.list_pim
            self.ibar=self.icont=0
            for pim in par.list_pim:
                if pim: self.ibar+=1
            self.Im_min_a=par.Imin[0]
            self.Im_min_b=par.Imin[1]
        elif data.typeW==2: #PIV
            par=data.PIVpar
            self.list_pim=par.list_pim
            self.ibar=self.icont=0
            for pim in par.list_pim:
                if pim: self.ibar+=1
            self.ibar=0
            for pim in par.list_pim:
                if pim: self.ibar+=1

    def setProgressBar(self,tree):
        i=tree.currentItem()#TREpar.future[0]
        data=i.data(0,Qt.UserRole)
        if data.typeW==1: #minimum
            par=data.MINpar
            self.ui.progress_Proc.setMinimum(0)
            self.ui.progress_Proc.setMaximum(par.nimg_proc)
            self.ui.progress_Proc.setValue(self.ibar) 
        elif data.typeW==2: #PIV
            par=data.PIVpar
            self.ui.progress_Proc.setMinimum(0)
            self.ui.progress_Proc.setMaximum(par.nimg)
            self.ui.progress_Proc.setValue(self.ibar) 
        
    
    def initializeWorkers(self):
        self.indWorker=-1
        self.indProc=-1
        future=self.ui.w_Tree.TREpar.future
        for i in future:
            self.indWorker+=1
            data=i.data(0,Qt.UserRole)
            if data.typeW==1: #minimum
                self.initializeMinProc(data)
            elif data.typeW==2: #PIV
                self.initializePIVProc(data)

    def initializeMinProc(self,data):
        par0=data.MINpar
        if par0.flag_TR: fac=2
        else: fac=1
        
        currpath=myStandardPath(data.PIVpar.OUT.path+data.PIVpar.OUT.subfold)
        if not os.path.exists(currpath): 
            os.mkdir(currpath)

        calcMin_workers=[]
        for j in range(par0.NumThreads):
            par0.i=j*fac
            calcMin_workers.append(calcMin_Worker(par0,self.indWorker,self.indProc))
            calcMin_workers[j].signals.progress.connect(self.progress_MINproc)
            calcMin_workers[j].signals.result.connect(self.pause_MINproc)
            self.ui.button_pause.clicked.connect(calcMin_workers[j].die)
            self.signals.kill.connect(calcMin_workers[j].die)
            #self.ui.button_delete.clicked.connect(calcMin_workers[j].die)
            self.signals.indProc.connect(calcMin_workers[j].updateIndProc)
            self.PaIRS_threadpool.start(calcMin_workers[j])

    @Slot(int,int,object,int,str)
    def progress_MINproc(self,ind,pim,Imin,flag_TR,stampa):
        self.ui.w_LogTab.logWrite(stampa)
        self.ibar+=1
        self.list_pim[ind]=pim
        self.ui.progress_Proc.setValue(self.ibar)

    @Slot(int,object,int,int)
    def pause_MINproc(self,icont,Imin,flag_TR,nimg_proc):
        self.icont+=icont
        if flag_TR:
            if not np.size(self.Im_min_a):
                self.Im_min_a=Imin[0]
            elif np.size(Imin[0]):
                self.Im_min_a=np.minimum(self.Im_min_a,Imin[0])
            self.Im_min_b=self.Im_min_a
        else:
            if not np.size(self.Im_min_a):
                self.Im_min_a=Imin[0]
            elif np.size(Imin[0]):
                self.Im_min_a=np.minimum(self.Im_min_a,Imin[0])
            if not np.size(self.Im_min_b):
                self.Im_min_b=Imin[1]
            elif np.size(Imin[1]):
                self.Im_min_b=np.minimum(self.Im_min_b,Imin[1])
        self.storeMinimum()

        if self.icont==nimg_proc:
            self.finish_MINproc()
        myprint('***** Stop signal *****')
        self.signals.stopped.emit()
            
    def finish_MINproc(self):
        i=self.ui.w_Tree.TREpar.future[0]
        data=i.data(0,Qt.UserRole)
        currpath=myStandardPath(data.PIVpar.OUT.path+data.PIVpar.OUT.subfold)
        root=myStandardRoot(data.PIVpar.OUT.root)
        ext=data.PIVpar.INP.pinfo.ext
        frame='ab'
        for j,f in enumerate(frame):
            nameout=f"{currpath}{root}_{f}_min{ext}"
            im = Image.fromarray(data.MINpar.Imin[j])
            im.save(nameout)
        self.updateIndProc()    

    def storeMinimum(self):
        i=self.ui.w_Tree.TREpar.future[0]
        data=i.data(0,Qt.UserRole)
        data.list_pim=copy.deepcopy(self.list_pim)
        data.MINpar.Imin=[self.Im_min_a,self.Im_min_b]
        data.flagRun=-1
        data.Log=self.ui.w_LogTab.ui.log.toPlainText()
        self.ui.w_Tree.TREpar.flagRun=-1
     
    def initializePIVProc(self,data):
        par0=data.PIVpar
        currpath=myStandardPath(data.PIVpar.OUT.path+data.PIVpar.OUT.subfold)
        if not os.path.exists(currpath): 
            os.mkdir(currpath)

        if par0.NumThreads>1:
            PIV_manager=PIV_Manager(par0,self.indWorker,self.indProc)
            PIV_manager.signals.result.connect(self.progress_PIVproc)
            PIV_manager.signals.finished.connect(self.pause_PIVproc)
            self.ui.button_pause.clicked.connect(PIV_manager.die)
            self.signals.kill.connect(PIV_manager.die)
            #self.ui.button_delete.clicked.connect(PIV_manager.die)
            self.signals.indProc.connect(PIV_manager.updateIndProc)
            self.PaIRS_threadpool.start(PIV_manager)
            PIV_workers=[]
            par0.NumThreads-=1
            for j in range(par0.NumThreads):
                par0.i+=1
                PIV_workers.append(PIV_Worker(par0,self.indWorker,self.indProc))
                PIV_workers[j].signals.progress.connect(PIV_manager.save_vector_fields)
                self.signals.indProc.connect(PIV_workers[j].updateIndProc)
                PIV_manager.signals.kill.connect(PIV_workers[j].die)
                self.PaIRS_threadpool.start(PIV_workers[j])
        else:
            par0.i+=1
            PIV_worker=PIV_Worker(par0,self.indWorker,self.indProc)
            PIV_worker.signals.result.connect(self.progress_PIVproc)
            PIV_worker.signals.finished.connect(self.pause_PIVproc)
            self.ui.button_pause.clicked.connect(PIV_worker.die)
            self.signals.kill.connect(PIV_worker.die)
            #self.ui.button_delete.clicked.connect(PIV_worker.die)
            self.signals.indProc.connect(PIV_worker.updateIndProc)
            PIV_worker.signals.progress.connect(PIV_worker.save_vector_fields)
            self.PaIRS_threadpool.start(PIV_worker)

            #PIV_worker.indProc=PIV_worker.indWorker
            #PIV_worker.run()

    @Slot(int,int,int,int,np.ndarray,np.ndarray,np.ndarray,np.ndarray,str)
    def progress_PIVproc(self,i,icont,indProc,pim,x,y,u,v,stampa):
        self.ui.w_LogTab.logWrite(stampa+'\n')
        self.ui.progress_Proc.setValue(icont)
        if pim==1:
            #myprint(f'plotting the field  #{icont}')
            if Flag_GRAPHICS:
                self.ui.w_ImportTab.ui.list_images.setCurrentRow(int(i*2))
                self.ui.w_ImportTab.selectListItem()
                self.showImg_quiv(x,y,u,v)

    @Slot(object)
    def pause_PIVproc(self,par):
        #myprint(f'plotting the average field! ({par.cont}/{par.nimg})')
        self.storePIV(par)
        if par.icont==par.nimg: #save and continue
            if Flag_GRAPHICS:
                self.ui.w_ImportTab.ui.list_images.setCurrentRow(int(par.icont*2))
                self.ui.w_ImportTab.selectListItem()
                self.showImg_quiv(par.x,par.y,par.u,par.v)
            self.updateIndProc()
        else: 
            self.signals.kill.emit()
        myprint('***** Stop signal *****')
        self.signals.stopped.emit()
           
    def storePIV(self,par):
        i=self.ui.w_Tree.TREpar.future[0]
        data=i.data(0,Qt.UserRole)
        data.PIVpar.list_pim=copy.deepcopy(par.list_pim)
        self.list_pim=data.PIVpar.list_pim
        data.PIVpar.icont=self.ibar=par.icont
        data.PIVpar.cont=par.cont
        data.PIVpar.x=par.x.copy()
        data.PIVpar.y=par.y.copy()
        data.PIVpar.u=par.u.copy()
        data.PIVpar.v=par.v.copy()
        data.PIVpar.sn=par.sn.copy()
        data.PIVpar.Info=par.Info.copy()   
        data.Log=self.ui.w_LogTab.ui.log.toPlainText()
        data.flagRun=-1  
        self.ui.w_Tree.TREpar.flagRun=-1
            
    def stopProcs(self):
        self.Stopped=True
        if self.Closing:
            self.save_uicfg(lastcfgname)
            self.closeEvent(True)
        
#*************************************************** Connecting tabs
    def change_edit_path(self):
        if self.ui.w_ExportTab.OUTpar.FlagSameAsInput:
            self.ui.w_ExportTab.ui.edit_path.setText(self.ui.w_ImportTab.ui.edit_path.text())
            self.ui.w_ExportTab.OUTpar.path=self.ui.w_ExportTab.ui.edit_path.text()
            self.ui.w_ExportTab.OUTpar_prev[0].path=self.ui.w_ExportTab.ui.edit_path.text()
            self.ui.w_ExportTab.checkPath()
            self.ui.w_ExportTab.checkSubFold()
            self.ui.w_ExportTab.checkRoot()

    def spin_update_image(self,spin):
        if self.ui.w_ExportTab.spin_value!=spin.value():
            self.update_image()

#*************************************************** Modify UI
    def checkTabs(self):
        if self.GPApar.FlagUndocked:
            self.ui.button_Shape.hide()
            self.ui.button_dock.setIcon(self.icon_dock_tabs)
            for i,wn in enumerate(self.widnames):
                flag=getattr(self.GPApar,f"Flag{wn}")
                if flag:
                    self.floatings[i].show()
                else:
                    self.floatings[i].hide()
        else:
            self.ui.button_dock.setIcon(self.icon_undock_tabs)
            self.ui.button_Shape.show()
            if self.GPApar.FlagAllTabs:
                self.ui.button_Shape.setIcon(self.icon_docked)
                cont=0
                nb=len(self.widnames)
                for wn in self.widnames:
                    flag=getattr(self.GPApar,f"Flag{wn}")
                    if not flag: cont+=1
                    button=getattr(self.ui,f"button_{wn}")
                    button.setChecked(flag)
                    self.button_Tab_action(wn)
                if cont==nb:
                    wn=self.widnames[self.GPApar.lastTab]
                    flag=True
                    button=getattr(self.ui,f"button_{wn}")
                    button.setChecked(flag)
                    setattr(self.GPApar,f"Flag{wn}",flag)
                    self.button_Tab_action(wn)
            else:
                self.ui.button_Shape.setIcon(self.icon_vert)
                widname=self.widnames[self.GPApar.lastTab]
                for wn in self.widnames:
                    if wn==widname:
                        flag=True
                    else:
                        flag=False
                    button=getattr(self.ui,f"button_{wn}")
                    button.setChecked(flag)
                    setattr(self.GPApar,f"Flag{wn}",flag)
                    self.button_Tab_action(wn)

    def button_Tab_callback(self,name):
        b=getattr(self.ui,"button_"+name)
        flagname="Flag"+name
        setattr(self.GPApar,flagname,b.isChecked())
        self.GPApar.lastTab=self.widnames.index(name)
        self.checkTabs()

    def button_Tab_action(self,name):
        flagname="Flag"+name
        flag=getattr(self.GPApar,flagname)
        tabname="f_"+self.tabnames[self.widnames.index(name)]+"Tab"
        tab=getattr(self.ui,tabname)
        if flag:
            tab.show()
        else:
            tab.hide()

    def button_Shape_callback(self):
        self.GPApar.FlagAllTabs=not self.GPApar.FlagAllTabs
        #if self.GPApar.FlagAllTabs:
        #    for wn in self.widnames:
        #        setattr(self.GPApar,f"Flag{wn}",True)
        self.checkTabs()
    
    def button_dock_callback(self):
        self.GPApar.FlagUndocked= not self.GPApar.FlagUndocked
        if self.GPApar.FlagUndocked:
            self.floatings=[]
            for i,wn in enumerate(self.tabnames):
                flag=getattr(self.GPApar,f"Flag{self.widnames[i]}")
                if wn=='Vis':
                    wname="f_"+wn+"Tab"
                else:
                    wname="w_"+wn+"Tab"
                wid=getattr(self.ui,wname)
                self.floatings.append(FloatingObject(self,wid,flag,False,(i-2)*100))
            self.floatings.append(FloatingObject(self,self.ui.w_Buttons,True,True,0))
            dpix=50
            self.centralWidget().setMaximumWidth(self.ui.f_Tree_Process.maximumWidth())
            self.centralWidget().setMinimumWidth(self.ui.f_Tree_Process.minimumWidth()+dpix)
            self.setMaximumWidth(self.ui.f_Tree_Process.maximumWidth())
            self.setMinimumWidth(self.ui.f_Tree_Process.minimumWidth()+dpix)
            self.ui.w_Operating_Tabs.hide()
        else:
            for i,wn in enumerate(self.tabnames):
                tabname="f_"+wn+"Tab"
                tab=getattr(self.ui,tabname)
                self.secondary_splitter.addWidget(tab)    
                self.secondary_splitter.setCollapsible(i,False)
            self.ui.oplay.insertWidget(0,self.ui.w_Buttons)
            for i in range(len(self.floatings)):
                self.floatings[i].close()
            self.floatings=[]
            self.centralWidget().setMaximumWidth(self.maxW)
            self.centralWidget().setMinimumWidth(self.minW)
            self.setMaximumWidth(self.maxW)
            self.setMinimumWidth(self.minW)
            self.ui.w_Operating_Tabs.show()
        self.resize(self.size())
            
        self.checkTabs()

#*************************************************** Displaying images
    def ind2NameImg(self):
        INP=self.ui.w_ImportTab.INPpar
        if self.ui.w_ImportTab.INPpar.FlagValidPath and self.ui.w_ImportTab.INPpar.FlagValidRoot:
            ind=INP.selected*2+INP.frame
            nameimg=INP.path+self.ui.w_ImportTab.list_Image_Files[ind]
        else:
            nameimg='' #'./'+ icons_path +'logo_PaIRS.png'
        return nameimg

    def createFig(self):
        if not self.flagInitImg:
            self.ui.w_ImportTab.signals.set_Image_List.connect(self.update_image)

            self.rect=[]
            self.nameimg=self.ind2NameImg()
            if self.nameimg:
                self.img = mplimage.imread(self.nameimg)
            else:
                self.img=None
            self.showMyImg()

    def update_image_on_interaction(self,w):
        if w.hasFocus():
            self.update_image()

    def update_image(self):
        if self.flagInitImg:
            nameimg=self.ind2NameImg()
            if self.nameimg!=nameimg:
                self.nameimg=nameimg
                if self.nameimg:
                    self.img = mplimage.imread(self.nameimg)
                else:
                    self.img=None
            self.showMyImg()
        self.UpdatingImage=False
            
    def update_image_Wind(self):
        #self.showMyImg()
        self.showMyRect()

    def showMyImg(self):
        self.ui.plot.axes.cla()
        #if self.ui.w_ExportTab.ui.spin_x.isEnabled():
        if self.nameimg:
            OUT = self.ui.w_ExportTab.OUTpar
            img = transfIm(OUT,self.img)[0]
            #else:
            #    img=self.img
            self.imgshow=self.ui.plot.axes.imshow(img)
            self.imgshow.set_cmap(mpl.colormaps['gray'])
            divider = make_axes_locatable(self.ui.plot.axes)
            cax = divider.append_axes("right", size="5%", pad=0.05) 
            if self.flagInitImg:
                self.cb.remove()
            else:
                self.flagInitImg=True
            self.cb=self.ui.plot.fig.colorbar(self.imgshow,cax=cax) 
            self.imgshow.set_clim(0,np.mean(img)+2*np.std(img))
        self.ui.plot.draw()

    def showMyRect(self):
        colors='rgbymc'
        lwidth=1
        nov_hor=3
        nov_vert=3

        Vect = self.ui.w_ProcessTab.PROpar.Vect
        nw=len(Vect[0])
        xin0=yin0=0
        xmax=ymax=0
        self.rect=[]
        for k in range(nw):
            for i in range(nov_vert):
                yin=yin0+i*Vect[3][k]
                for j in range(nov_hor):
                    xin=xin0+j*Vect[1][k]
                    kk=i+j*nov_vert
                    if kk%2: lst=':'
                    else: lst='-'
                    kc=k%len(colors)
                    rect = mpl.patches.Rectangle((xin, yin), Vect[0][k], Vect[2][k],\
                        linewidth=lwidth, edgecolor=colors[kc], facecolor=colors[kc],\
                            alpha=0.25,linestyle=lst)
                    self.ui.plot.axes.add_patch(rect)
                    rect2 = mpl.patches.Rectangle((xin, yin), Vect[0][k], Vect[2][k],\
                        linewidth=lwidth, edgecolor=colors[kc], facecolor='none',\
                            alpha=1,linestyle=lst)
                    self.ui.plot.axes.add_patch(rect2)
                    points=self.ui.plot.axes.plot(xin+ Vect[0][k]/2,yin+ Vect[2][k]/2,\
                        'o',color=colors[kc])
                    if not kk: text=self.ui.plot.axes.text(xin+5,yin+5,str(k),\
                        horizontalalignment='left',verticalalignment='top',\
                        fontsize='large',color='w',fontweight='bold')
                    self.rect=self.rect+[rect,rect2,points,text]
            xmaxk=xin+Vect[0][k]
            ymaxk=yin+Vect[2][k]
            if xmaxk>xmax: xmax=xmaxk
            if ymaxk>ymax: ymax=ymaxk
            if k==nw-1: continue
            if ymaxk+Vect[2][k+1]+(nov_vert-1)*Vect[3][k+1]<self.ui.w_ExportTab.OUTpar.h:
                yin0=ymaxk
            else:
                yin0=0
                xin0=xmax
        self.ui.plot.draw()

    def showImg_quiv(self,x,y,u,v):
        self.ui.plot.axes.cla()
        if self.flagInitImg:
            self.cb.remove()
        else:
            self.flagInitImg=True
        OUT = self.ui.w_ExportTab.OUTpar
        img = transfIm(OUT,self.img)[0]
        M = np.sqrt(u*u+v*v) 
        qq=self.ui.plot.axes.quiver(x,y,u,v,M,cmap=pyplt.cm.jet)
        self.imgshow=self.ui.plot.axes.imshow(img)
        self.imgshow.set_cmap(mpl.colormaps['gray'])
        divider = make_axes_locatable(self.ui.plot.axes)
        cax = divider.append_axes("right", size="5%", pad=0.05) 
        self.cb=self.ui.plot.fig.colorbar(qq, cmap=pyplt.cm.jet, cax=cax) 
        self.ui.plot.draw()

#*************************************************** RUN
    def addProc(self,fun):
        OUT=self.ui.w_ExportTab.OUTpar
        FlagValidInput=all([self.ui.w_ImportTab.ui.list_images.isEnabled,\
            self.ui.w_ImportTab.INPpar.FlagValidPath,self.ui.w_ImportTab.INPpar.FlagValidRoot])
        FlagValid=all([FlagValidInput,\
            OUT.FlagValidPath,OUT.FlagValidSubFold,OUT.FlagValidRoot,\
            ])
        if FlagValid:
            fun()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            Message=""
            flag=2
            if not FlagValidInput:
                Message=Message+"Please, select a valid set of images to process!\n"
                flag=flag-1
            if not OUT.FlagValidPath:
                furtherMess="choose a valid output folder path"
                Message,flag=self.furtherMessage(Message,flag,furtherMess)
            if not OUT.FlagValidSubFold:
                furtherMess="choose a valid output subfolder path"
                Message,flag=self.furtherMessage(Message,flag,furtherMess)
            if not OUT.FlagValidRoot:
                furtherMess="choose a valid root of the output filename"
                Message,flag=self.furtherMessage(Message,flag,furtherMess)
            if flag==2: 
                Message=Message+"!"
                flag=flag-1
            else: 
                Message=Message+".\n"

            dlg.setText(str(Message))

            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Warning)
            dlg.setFont(self.font())
            button = dlg.exec()
        self.repaint()

    def furtherMessage(self,Message,flag,furtherMess):
        if flag==2: 
            Message=Message+"Please, "
        elif flag==1:
            Message=Message+"!\n\nFURTHERMORE:\n- "
        elif flag==0: 
            Message=Message+".\n- "
        else:
            Message=Message+";\n- "
        Message=Message+furtherMess
        flag=flag-1
        return Message,flag

    def button_pause_callback(self):
        self.FlagRun= not self.FlagRun
        self.ui.w_Tree.FlagPause = not self.FlagRun
        if self.FlagRun:
            self.ui.w_Tree.ui.button_min.hide()
            self.ui.w_Tree.ui.button_PIV.hide()
            self.ui.button_pause.setIcon(self.ui.w_ImportTab.icon_pause)
            self.ui.button_Input.hide()
            self.ui.button_Output.hide()
            self.ui.button_Process.hide()
            self.ui.f_ImportTab.hide()
            self.ui.f_ExportTab.hide()
            self.ui.f_ProcessTab.hide()
            self.ui.w_Tree.ui.tree_past.setEnabled(False)
            self.ui.w_Tree.ui.tree_current.setEnabled(False)
            self.ui.w_Tree.ui.tree_past.setEnabled(False)
            self.ui.w_Tree.signals.selection.disconnect(self.updateGuiFromTree)
            self.update()
            time.sleep(.5)

            self.run()
        else:
            self.ui.w_Tree.ui.button_min.show()
            self.ui.w_Tree.ui.button_PIV.show()
            self.ui.button_pause.setIcon(self.ui.w_ImportTab.icon_play)
            self.ui.button_Input.show()
            self.ui.button_Output.show()
            self.ui.button_Process.show()
            self.ui.f_ImportTab.show()
            self.ui.f_ExportTab.show()
            self.ui.f_ProcessTab.show()
            self.ui.w_Tree.ui.tree_past.setEnabled(True)
            self.ui.w_Tree.ui.tree_current.setEnabled(True)
            self.ui.w_Tree.ui.tree_past.setEnabled(True)
            self.ui.w_Tree.signals.selection.connect(self.updateGuiFromTree)

    def button_delete_callback(self):
        self.button_pause_callback()
        self.ui.progress_Proc.hide()
        self.ui.button_pause.hide()
        #self.ui.button_delete.hide()
        self.ui.button_Run.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = gPaIRS()
    #object.show()
    sys.exit(app.exec())
