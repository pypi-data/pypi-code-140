from .ui_Import_Tab import*
from .Import_Tab_threads import*
from .calcMin_threads import*
from .PaIRS_pypacks import*
from .addwidgets_ps import*

NUMTHREADS_CalcMin=1

class INPpar:
    def __init__(self):
        self.name = ''
        self.FlagValidPath = False
        self.path = myStandardPath(basefold)
        self.FlagValidRoot = False
        self.root = ''
        self.Pinfo = patternInfoList()
        self.pinfo = patternInfoList()
        self.nimg_eff = 0
        self.range_from = 0 
        self.range_to = 0
        self.selected = 0
        self.frame = 0
        self.flag_TR = False
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.W = 1
        self.H = 1
        self.flag_min = True

        self.fields={}
        for f,v in self.__dict__.items():
            if f!='fields' and f[0]!='_':
                self.fields[f]=v
        self.spin_fields=("range_from","range_to","selected","frame","x","y","w","h")
        self.TR_min_fields=("flag_TR","flag_min")

    def printPar(self):
        myprint(self.__dict__)

    def duplicate(self):
        newist=INPpar()
        for f in INPpar().fields:
            a=getattr(self,f)
            if type(a)==patternInfoList:
                setattr(newist,f,a.duplicate())
            else:
                setattr(newist,f,copy.deepcopy(a))
        newist.setFields()
        return newist

    def copyfrom(self,newist):
        for f in INPpar().fields:
            a=getattr(newist,f)
            if type(a)==patternInfoList:
                setattr(self,f,a.duplicate())
            else:
                setattr(self,f,copy.deepcopy(a))
        self.setFields()

    def copyfromdiz(self,newist,diz):
        for f in diz:
            a=getattr(newist,f)
            if type(a)==patternInfoList:
                setattr(self,f,a.duplicate())
            else:
                setattr(self,f,copy.deepcopy(a))
        self.setFields()
  
    def setFields(self):
        for f in INPpar().fields:
            self.fields[f]=getattr(self,f)

class uiINPpar(INPpar):

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
                instance.fields[self.name]=self.value
                if instance.FlagAddFunc:
                    for f in instance.addfunc:
                        instance.addfunc[f](self.name)

    @classmethod     
    def __init__(self):
        super().__init__(self)
        self.FlagAddFunc=True
        self.FlagAddINPpar=True
        self.addfunc={}
        for field, value in INPpar().fields.items():
            setattr(self, field, self._ReactingProp([field, value]))
            #setattr(self, field, value)
  
class Import_Tab(QWidget):
    
    class Import_Tab_Signals(QObject):
        add_par=Signal()
        update_par=Signal()
        set_Image_List=Signal()

        indProc=Signal(int)
        pause_calcMin=Signal()
        completed_calcMin=Signal()
    

    def closeEvent(self, event):
        self.Path_threadpool.clear()
        return super().closeEvent(event)

    def __init__(self,parent):
        super().__init__(parent)

        self.signals=self.Import_Tab_Signals()

        ui=Ui_ImportTab()
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

        ui.spin_range_from.addwid=[ui.spin_selected]
        ui.spin_range_to.addwid=[ui.spin_selected]
        ui.spin_x.addwid=[ui.spin_w]
        ui.spin_y.addwid=[ui.spin_h]

        ui.edits=self.findChildren(MyQLineEdit)
        for child in ui.edits:
            child.setup()
        for child in ui.edits:
            child.setup2()
        ui.spins=self.findChildren(MyQSpin)
        for child in ui.spins:
            child.setup()
        ui.dspins=self.findChildren(MyQDoubleSpin)
        for child in ui.dspins:
            child.setup()
        self.ui=ui

        #for callbacks
        self.mapx  = QPixmap(''+ icons_path +'redx.png')
        self.mapv  = QPixmap(''+ icons_path +'greenv.png')
        self.mapw  = QPixmap(''+ icons_path +'waiting_c.png')
        self.Lab_warning=QPixmap(u""+ icons_path +"warning.png")

        self.list_Path_Root=["edit_path","button_path","edit_root","button_import"]
        self.list_Spins=["spin_range_from","spin_range_to","spin_selected","spin_frame","spin_x","spin_y","spin_w","spin_h"]
        self.list_Image_Opt=["check_TR_sequence","button_min","button_resize"]
        self.list_List_Images=["list_images"]
        self.list_All=self.list_Path_Root[:]+self.list_Spins[:]+self.list_Image_Opt[:]+self.list_List_Images[:]

        self.icon_play = QIcon()
        self.icon_play.addFile(u""+ icons_path +"play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_pause = QIcon()
        self.icon_pause.addFile(u""+ icons_path +"pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_done = QIcon()
        self.icon_done.addFile(u""+ icons_path +"done.png", QSize(), QIcon.Normal, QIcon.Off)
        self.movie_wait = QMovie("waiting.gif")
        
        #Callbacks
        self.ui.edit_path.textChanged.connect(self.edit_path_changing)
        self.ui.edit_path.returnPressed.connect(self.edit_path_callback)
        self.ui.edit_path.editingFinished.connect(self.edit_path_finished)
        self.ui.edit_root.textChanged.connect(self.edit_root_changing)
        self.ui.edit_root.returnPressed.connect(self.edit_root_callback)
        self.ui.edit_root.editingFinished.connect(self.edit_root_finished)
        
        self.ui.spin_range_from.valueChanged.connect(self.spin_range_from_callback)
        self.ui.spin_range_to.valueChanged.connect(self.spin_range_to_callback)
        self.ui.spin_selected.valueChanged.connect(self.spin_selected_callback)
        self.ui.spin_frame.valueChanged.connect(self.spin_frame_callback)
        self.ui.list_images.currentRowChanged.connect(self.list_images_callback)
        self.ui.check_TR_sequence.stateChanged.connect(self.check_TR_callback)
        self.ui.button_min.clicked.connect(self.button_min_callback)

        self.ui.spin_x.textChanged.connect(self.spin_x_callback)
        self.ui.spin_x.valueChanged.connect(self.spin_x_callback)
        self.ui.spin_y.valueChanged.connect(self.spin_y_callback)
        self.ui.spin_y.textChanged.connect(self.spin_y_callback)
        self.ui.spin_w.valueChanged.connect(self.spin_w_callback)
        self.ui.spin_w.textChanged.connect(self.spin_w_callback)
        self.ui.spin_h.valueChanged.connect(self.spin_h_callback)
        self.ui.spin_h.textChanged.connect(self.spin_h_callback)

        self.ui.button_path.clicked.connect(self.button_path_callback)
        self.ui.button_import.clicked.connect(self.button_import_callback)
        self.ui.button_resize.clicked.connect(self.button_resize_callback)
        
        self.ui.button_pause_min.clicked.connect(self.button_pause_min_callback)
        self.ui.button_restart_min.clicked.connect(self.button_restart_min_callback)
        
        #Controls
        ui.button_back.clicked.connect(self.button_back_callback)
        ui.button_forward.clicked.connect(self.button_forward_callback)
        self.INPpar_base=INPpar()
        self.INPpar=uiINPpar()
        self.ParPointer=self.INPpar

        for s in ui.spins+ui.dspins:
            if not s.objectName() in ('spin_selected','spin_frame'):
                s.addfuncin['spin_funcin']=lambda sp=s: self.spin_funcin(sp)
                s.addfuncout['spin_funcout']=lambda sp=s: self.spin_funcout(sp)

        #Initializing
        self.INPpar_prev=[]
        self.INPpar_ind=0
        self.INPpar.FlagAddINPpar=True

        self.Path_threadpool = QThreadPool() 
        self.Path_worker=None
        self.list_Image_Files=[]
        self.list_eim=[]
        self.list_Image_items=[]
        self.isWorkerKilled=[True]

        self.Min_threadpool = QThreadPool()
        self.calcMin_workers=[]
        self.MIN_threadpool = QThreadPool() 
        if NUMTHREADS_CalcMin>0:
            self.MIN_threadpool.setMaxThreadCount(NUMTHREADS_CalcMin)
        myprint("Multithreading with maximum %d threads" % self.MIN_threadpool.maxThreadCount())
        self.indWorker=0
        self.flag_comp_min=False
        self.flag_min=self.INPpar.flag_min=False
        self.i_min=-1
        self.flag_pause_min=True 
        self.Im_min_a=np.array([])
        self.Im_min_b=np.array([])
        self.list_pim=[]

        self.signals.pause_calcMin.connect(self.calcMinPaused_reaction)
        self.signals.completed_calcMin.connect(self.calcMinCompleted)   
        self.ui.check_subtract.stateChanged.connect(self.check_subtract_callback)
        self.ui.check_subtract_2.stateChanged.connect(self.check_subtract_callback)
        self.ui.check_subtract_2.hide()

        self.ui.edit_path.setText(basefold)
        self.getPinfoFromPath(self.INPpar.path,'') 
        self.INPpar.FlagAddINPpar=True

        self.INPpar_preproc=self.INPpar
        self.check_preproc()

        self.add_INPpar('initial')
        self.ui.button_forward.hide()
        self.ui.button_back.hide()

        
#*************************************************** INPpars and controls
    def setINPpar_prev(self):
        self.setINPpar_item(self.INPpar_prev[self.INPpar_ind])
        self.display_controls()

    def setINPpar_item(self,INPpar_item):
        self.flag_comp_min=False
        self.setRoot(INPpar_item,False,-1)
        self.INPpar.copyfrom(INPpar_item)
        self.setINPpar()
        
    def display_controls(self):
        if len(self.INPpar_prev)>1:
            self.ui.button_forward.show()
            self.ui.button_back.show()
        else:
            self.ui.button_forward.hide()
            self.ui.button_back.hide()
        if self.INPpar_ind==0:
            self.ui.button_forward.setEnabled(False)
        else:
            self.ui.button_forward.setEnabled(True)
        if self.INPpar_ind==len(self.INPpar_prev)-1:
            self.ui.button_back.setEnabled(False)
        else:
            self.ui.button_back.setEnabled(True)
        if self.INPpar_ind==0:
            self.ui.label_number.setText('')
        else:
            self.ui.label_number.setText("(-"+str(self.INPpar_ind)+")")

    def add_INPpar(self,name):
        if self.INPpar.FlagAddINPpar:
            myprint(name)
            INPpar_new=INPpar()
            INPpar_new.copyfrom(self.INPpar)
            self.INPpar_prev.insert(0,INPpar_new)
            self.INPpar_ind=0
            self.signals.add_par.emit()
            self.display_controls()

    def button_back_callback(self):
        self.INPpar_ind+=1
        self.setINPpar_prev()

    def button_forward_callback(self):
        self.INPpar_ind-=1
        self.setINPpar_prev()

    def spin_funcin(self,spin):
        self.spin_value=spin.value()

    def spin_funcout(self,spin):
        if self.spin_value!=spin.value():
            self.add_INPpar(spin.objectName())
            self.check_resize()

    def check_resize(self):
        if self.INPpar.W!=self.ui.spin_w.value() or \
            self.INPpar.H!=self.ui.spin_h.value():
            self.ui.button_resize.show()
        else:
            self.ui.button_resize.hide()

#*************************************************** From Parameters to UI
    def setINPpar(self):
        FlagAddINPpar=self.INPpar.FlagAddINPpar
        self.INPpar.FlagAddINPpar=False
        self.ChangeText_path(self.INPpar.path)
        self.checkPath()
        self.ChangeText_root(self.INPpar.root)
        self.checkRootFromList()
        self.setRootCompleter()
        self.ui.check_TR_sequence.setChecked(self.INPpar.flag_TR)
        self.ui.check_subtract_2.setChecked(self.INPpar.flag_min)
        self.setMinMaxSpin()
        self.setValueSpin()
        self.ui.button_min.setChecked(self.flag_comp_min) 
        self.INPpar.FlagAddINPpar=FlagAddINPpar
        self.check_preproc()

    def ChangeText_path(self,text): 
        text=myStandardPath(text)
        self.ui.edit_path.setText(text)
    
    def checkPath(self):
        self.INPpar.FlagValidPath=os.path.exists(self.INPpar.path)
        self.setPathLabel()
        
    def setPathLabel(self):
        if self.INPpar.FlagValidPath:
            self.ui.label_check_path.setPixmap(self.mapv)
            self.ui.label_check_path.setToolTip("This path exists! 😃")
        else:
            self.ui.label_check_path.setPixmap(self.mapx)
            self.ui.label_check_path.setToolTip("This path does not exist! 😞")

    def ChangeText_root(self,text,*args):
        text=myStandardRoot(text)
        text=text.replace(';',' ; ')
        self.ui.edit_root.setText(text)
              
    def checkRootFromList(self):
        if  not len(self.list_eim):
            self.INPpar.FlagValidRoot=0
        else:
            FlagExistAll=all(self.list_eim)
            if FlagExistAll:
                self.INPpar.FlagValidRoot=1
            else:
                self.INPpar.FlagValidRoot=-1
        self.setRootLabel()
        
    def setRootLabel(self):
        if self.INPpar.FlagValidRoot==0:
            self.ui.label_check_root.setPixmap(self.mapx)
            self.ui.label_check_root.setToolTip("There are no files with this filename root in the selected path! 😞")
        elif self.INPpar.FlagValidRoot==1:
            self.ui.label_check_root.setPixmap(self.mapv)
            self.ui.label_check_root.setToolTip("Files correctly identified! 😃")
        elif self.INPpar.FlagValidRoot==-1:
            self.ui.label_check_root.setPixmap(self.Lab_warning)
            self.ui.label_check_root.setToolTip("Some files seem missing: please, check! 🧐")

    def setRootCompleter(self):
        self.edit_root_completer=QCompleter(self.INPpar.Pinfo.root)
        self.edit_root_completer.setCompletionMode(QCompleter.CompletionMode(1))
        self.edit_root_completer.setModelSorting(QCompleter.ModelSorting(2))
        self.edit_root_completer.setWidget(self.ui.edit_root)
        self.ui.edit_root.setCompleter(self.edit_root_completer)

    def setMinMaxSpin(self):
        value_range_from=self.INPpar.range_from
        value_range_to=self.INPpar.range_to
        value_selected=self.INPpar.selected
        d=self.INPpar.nimg_eff-1
        self.ui.spin_range_from.setMinimum(0)
        self.ui.spin_range_from.setMaximum(d)
        self.ui.spin_range_to.setMinimum(0)
        self.ui.spin_range_to.setMaximum(d)
        self.ui.spin_selected.setMinimum(0)
        self.ui.spin_selected.setMaximum(d)
        self.ui.spin_frame.setMinimum(0)
        self.ui.spin_frame.setMaximum(1)
        self.ui.spin_x.setMinimum(0)
        self.ui.spin_x.setMaximum(self.INPpar.W-1)
        self.ui.spin_y.setMinimum(0)
        self.ui.spin_y.setMaximum(self.INPpar.H-1)
        self.ui.spin_w.setMinimum(1)
        self.ui.spin_w.setMaximum(self.INPpar.W)
        self.ui.spin_h.setMinimum(1)
        self.ui.spin_h.setMaximum(self.INPpar.H)
        self.INPpar.range_from=value_range_from
        self.INPpar.range_to=value_range_to
        self.INPpar.selected=value_selected
    
    def setValueSpin(self):
        self.ui.spin_range_from.setValue(self.INPpar.range_from)
        self.ui.spin_range_to.setValue(self.INPpar.range_to)
        self.ui.spin_selected.setValue(self.INPpar.selected)
        self.ui.spin_frame.setValue(self.INPpar.frame)
        self.selectListItem()
        self.ui.spin_x.setValue(self.INPpar.x)
        self.ui.spin_y.setValue(self.INPpar.y)
        self.ui.spin_w.setValue(self.INPpar.w)
        self.ui.spin_h.setValue(self.INPpar.h)
        self.check_resize()

    def DisableAll(self,*args):
        if len(args):
            flag=args[0]
        else:
            flag=False #some widgets were removed
        for nobj in range(0,len(self.list_All)):
            obj=getattr(self.ui,self.list_All[nobj])
            obj.setEnabled(False)

    def EnableAll(self,*args):
        if len(args):
            flag=args[0]
        else:
            flag=False #some widgets were removed
        for nobj in range(0,len(self.list_All)):
            obj=getattr(self.ui,self.list_All[nobj])
            obj.setEnabled(True)

    def Disable_ImgObjects(self):
        self.setMinMaxSpin()
        for nobj in range(len(self.INPpar.spin_fields)):
            obj=getattr(self.ui,self.list_Spins[nobj])
            obj.setEnabled(False)
            field_value=getattr(self.INPpar_base,self.INPpar.spin_fields[nobj])
            obj.setValue(field_value)
        self.ui.list_images.setEnabled(False)
        self.ui.list_images.clear()
        for nobj in range(len(self.INPpar.TR_min_fields)):
            obj=getattr(self.ui,self.list_Image_Opt[nobj])
            obj.setEnabled(False)
            #field_value=getattr(self.INPpar_base,self.INPpar.TR_min_fields[nobj])
            #obj.setChecked(field_value)

    def Enable_ImgObjects(self):
        for nobj in range(len(self.list_Spins)):
            obj=getattr(self.ui,self.list_Spins[nobj])
            obj.setEnabled(True)
        self.ui.list_images.setEnabled(True)
        for nobj in range(len(self.list_Image_Opt)):
            obj=getattr(self.ui,self.list_Image_Opt[nobj])
            obj.setEnabled(True)

    def check_preproc(self):
        if not self.flag_comp_min:
            self.ui.w_progress_min.hide()
            """
            self.flag_min=False
            self.ui.progress_min.setMinimum(0)
            self.ui.progress_min.setMaximum(0)
            self.ui.progress_min.setValue(0)
            self.flag_pause_min=True
            """
        else:
            self.ui.w_progress_min.show()
            self.flag_min=True
            self.ui.check_subtract.setChecked(self.flag_min)
            if self.i_min==len(self.list_Image_Files):
                self.ui.label_pause_min.show()
                self.ui.button_pause_min.hide()
                self.ui.button_restart_min.setEnabled(True)
            else:
                self.ui.label_pause_min.hide()
                self.ui.button_pause_min.show()
                if not self.flag_pause_min:
                    self.ui.button_pause_min.setIcon(self.icon_pause)
                    self.ui.button_restart_min.setEnabled(False)
                else:
                    self.ui.button_pause_min.setIcon(self.icon_play)
                    self.ui.button_restart_min.setEnabled(True)
        self.update()

#*************************************************** Path and Images utilities
    def setINPpar_prev_async(self,ind_prev):
        if ind_prev>=0:
            #myprint('*** updating previous INPpar')
            ind_curr=len(self.INPpar_prev)
            self.INPpar_prev[ind_curr-ind_prev-1].copyfrom(self.INPpar)
            self.signals.update_par.emit()
        #else:
            #myprint('### not updating previous INPpar')

    def PathWorker_finished(self,typeofWorker,ind_prev):
        if typeofWorker==1:
            self.checkPath()
        elif typeofWorker in (2,3):
            self.setRootLabel()
        self.isWorkerKilled[0]=True
        if ind_prev>=0:
            ind_curr=len(self.INPpar_prev)
            del self.INPpar_prev[ind_curr-ind_prev-1]
        self.funFinish()
  
    def getPinfoFromPath(self,path,target,*args):
        if len(args):
            ind_prev=args[0]
        else:
            ind_prev=len(self.INPpar_prev)

        self.INPpar.path=path     
        self.ui.edit_path.setText(self.INPpar.path)   

        self.ui.label_check_path.setPixmap(self.mapw)
        self.ui.edit_root.setEnabled(False)
        self.ui.button_import.setEnabled(False)
        self.ui.button_back.setEnabled(False)
        self.ui.button_forward.setEnabled(False)
        self.Disable_ImgObjects()

        if not self.isWorkerKilled[0]:
            self.funFinish=lambda: self.getPinfoFromPath(path,target,ind_prev)
            self.Path_worker.die()
        else:
            self.funFinish=lambda: None
            self.isWorkerKilled[0]=False
            self.Path_worker=analysePath_Worker(path)
            self.Path_worker.signals.result.connect(lambda p: self.selectRootInPath(p,target,ind_prev))
            self.Path_threadpool.start(self.Path_worker)        
      
    @Slot(patternInfoList,str)
    def selectRootInPath(self,Pinfo=patternInfoList,target=str,ind_prev=int):
        flag=Pinfo.pattern!=None
        self.ui.edit_root.setEnabled(True)
        self.ui.button_import.setEnabled(True)
        self.ui.button_back.setEnabled(True)
        self.ui.button_forward.setEnabled(True)
        if flag:
            self.isWorkerKilled[0]=True
            self.checkPath()
            self.INPpar.Pinfo=Pinfo.duplicate()
            if len(self.INPpar.Pinfo.pattern):
                if target:
                    vk=[]
                    vnimg=[]
                    for k in range(len(self.INPpar.Pinfo.pa)):
                        if self.INPpar.Pinfo.pa[k].match(target):
                            vk.append(k)
                            vnimg.append(self.INPpar.Pinfo.nimg_tot[k])
                    k=vk[np.argmax(np.asarray(vnimg))]    
                else:
                    k=np.argmax(np.asarray(Pinfo.nimg_tot))
                self.INPpar.pinfo=self.INPpar.Pinfo.extractPinfo(k)
                self.INPpar.root=self.INPpar.pinfo.root
                self.INPpar.FlagValidRoot=True
            else:
                self.INPpar.pinfo=patternInfoList()
                self.INPpar.root=''
                self.INPpar.FlagValidRoot=False
            self.ui.edit_root.setText(self.INPpar.root)
            self.setRootCompleter()
            self.setINPpar_prev_async(ind_prev)
            self.setRoot(self.INPpar,True,ind_prev)
        else:
            self.PathWorker_finished(1,ind_prev)
        
    def setRoot(self,INPpar_prev,flagDefault,*args):
        if len(args):
            ind_prev=args[0]
        else:
            ind_prev=len(self.INPpar_prev)
            
        self.ui.label_check_root.setPixmap(self.mapw)
        self.Disable_ImgObjects()

        if not self.isWorkerKilled[0]:
            self.funFinish=lambda: self.setRoot(INPpar_prev,flagDefault,ind_prev)
            self.Path_worker.die()
        else:
            if INPpar_prev.FlagValidRoot:
                self.funFinish=lambda: None
                self.isWorkerKilled[0]=False
                self.Path_worker=createListImages_Worker(INPpar_prev.path,INPpar_prev.pinfo,INPpar_prev.flag_TR)
                self.Path_worker.signals.result.connect(lambda r: self.setInfoImages(INPpar_prev,flagDefault,r,ind_prev))
                self.Path_threadpool.start(self.Path_worker)
            else:
                if not len(INPpar_prev.pinfo.root): INPpar_prev.pinfo.root=''
                self.INPpar.root=INPpar_prev.pinfo.root
                self.ui.edit_root.setText(self.INPpar.root)
                self.setInfoImagesFromINPpar(INPpar_prev,flagDefault,[])

    @Slot(list,int)
    def setInfoImages(self,INPpar,flagDefault,results,ind_prev=int):
        flag=len(results)
        if flag:
            self.isWorkerKilled[0]=True
            #results=[list_Image_Files, list_eim, list_Image_items, nimg_eff, w, h]
            self.setInfoImagesFromINPpar(INPpar,flagDefault,results)
            self.Enable_ImgObjects()
            self.setINPpar_prev_async(ind_prev)
        else:
            self.PathWorker_finished(2,ind_prev)
    
    def setInfoImagesFromINPpar(self,INPpar_prev,flagDefault,results):
        if not len(results):
            results=[[],[],[],0,0,0]
        if flagDefault:
            self.INPpar.nimg_eff=results[3]
            self.INPpar.range_from=0
            self.INPpar.range_to=self.INPpar.nimg_eff

            self.INPpar.x=self.INPpar.y=self.ParPointer.x=self.ParPointer.y=0
            self.INPpar.w=self.INPpar.W=results[4]
            self.INPpar.h=self.INPpar.H=results[5]
            self.ParPointer.w=self.ParPointer.W=results[4]
            self.ParPointer.h=self.ParPointer.H=results[5]
            self.setMinMaxSpin()
            self.setValueSpin()
        else:
            diz=('nimg_eff','range_from','range_to','x','y','w','h','W','H')
            self.INPpar.copyfromdiz(INPpar_prev,diz)

        self.list_Image_Files=results[0]
        self.list_eim=results[1]
        self.list_Image_items=results[2]
        self.checkRootFromList()
        self.ui.edit_root.setEnabled(True)
        self.setListImages()
        self.i_min=-1
        self.flag_comp_min=False
        self.ui.button_min.setChecked(self.flag_comp_min)
        self.check_preproc()
  
    def setListImages(self):
        self.ui.list_images.clear()
        ind_in=self.INPpar.range_from*2
        ind_fin=(self.INPpar.range_to+1)*2
        self.ui.list_images.addItems(self.list_Image_items[ind_in:ind_fin])
        self.selectListItem()
        self.signals.set_Image_List.emit()

    def getpinfofromRoot(self,path,pattern,*args):
        if len(args):
            ind_prev=args[0]
        else:
            ind_prev=len(self.INPpar_prev)

        self.ui.label_check_root.setPixmap(self.mapw)
        self.Disable_ImgObjects()

        if not self.isWorkerKilled[0]:
            self.funFinish=lambda: self.getpinfofromRoot(path,pattern,ind_prev)
            self.Path_worker.die()
        else:
            self.funFinish=lambda: None
            self.isWorkerKilled[0]=False
            self.Path_worker=analyseRoot_Worker(path,pattern)
            self.Path_worker.signals.result.connect(lambda p: self.setNewpinfo(p,ind_prev))
            self.Path_threadpool.start(self.Path_worker)        

    @Slot(patternInfoVar)
    def setNewpinfo(self,pinfo=patternInfoVar,ind_prev=int):
        flag=pinfo.nimg_tot>-1
        if flag:
            self.isWorkerKilled[0]=True
            if pinfo.nimg_tot>1:
                if pinfo.root in self.INPpar.Pinfo.root:
                    k=self.INPpar.Pinfo.root.index(pinfo.root)
                else:
                    self.INPpar.Pinfo=pinfo.addto(self.INPpar.Pinfo)
                    k=len(self.INPpar.Pinfo.pattern)-1
                self.INPpar.pinfo=self.INPpar.Pinfo.extractPinfo(k)
                self.INPpar.root=self.INPpar.pinfo.root
                self.ui.edit_root.setText(self.INPpar.root)
                self.setRootCompleter()
                self.setINPpar_prev_async(ind_prev)
                self.setRoot(self.INPpar,True,ind_prev)
            else:
                self.INPpar.root=pinfo.root
                self.ui.edit_root.setText(self.INPpar.root)
                self.setInfoImagesFromINPpar(self.INPpar_base,False,[])        
                self.setINPpar_prev_async(ind_prev)    
        else:
            self.PathWorker_finished(3,ind_prev)

#*************************************************** Edit path and root
    def edit_path_changing(self): 
        self.ui.label_check_path.setPixmap(QPixmap()) 
    
    def edit_path_finished(self): 
        self.ui.edit_path.setText(self.INPpar.path)
        self.setPathLabel()

    def edit_path_callback(self,*args):
        FlagAddINPpar= self.INPpar.FlagAddINPpar
        self.INPpar.FlagAddINPpar=False
        
        currpath=myStandardPath(self.ui.edit_path.text())
        if currpath==myStandardPath(self.INPpar.path):
            self.INPpar.FlagAddINPpar=FlagAddINPpar
            return 
        self.ui.label_check_path.setPixmap(self.mapw)
        self.repaint()

        self.reset_preproc()

        self.INPpar.path=currpath
        self.getPinfoFromPath(currpath,'')
        self.ui.edit_path.setFocus()
        self.ui.edit_root.clearFocus()

        self.INPpar.FlagAddINPpar=FlagAddINPpar
        self.add_INPpar('path')
 
    def button_path_callback(self):
        FlagAddINPpar= self.INPpar.FlagAddINPpar
        self.INPpar.FlagAddINPpar=False
        directory = str(QFileDialog.getExistingDirectory(QWidget(),\
            "Choose a folder", dir=self.INPpar.path,options=QFileDialog.Option.DontUseNativeDialog))
        currpath='{}'.format(directory)
        if not currpath=='':
            currpath=myStandardPath(currpath)
            directory_path = myStandardPath(os.getcwd())
            if directory_path in currpath:
                currpath=currpath.replace(directory_path,'./')
            self.ui.edit_path.setText(currpath)
            self.edit_path_callback()
            self.INPpar.FlagAddINPpar=FlagAddINPpar
            self.add_INPpar('path')
        else:
            self.INPpar.FlagAddINPpar=FlagAddINPpar

    def edit_root_changing(self):
         self.ui.label_check_root.setPixmap(QPixmap()) 
    
    def edit_root_finished(self): 
        self.ui.edit_root.setText(self.INPpar.root)
        self.setRootLabel()

    def edit_root_callback(self):
        FlagAddINPpar= self.INPpar.FlagAddINPpar
        self.INPpar.FlagAddINPpar=False

        entry=self.ui.edit_root.text()
        if entry.replace(" ","")==self.INPpar.root.replace(" ",""):
            self.INPpar.FlagAddINPpar=FlagAddINPpar
            self.setRootLabel()
            return
        self.INPpar.root=entry
        self.ui.edit_root.setText(self.INPpar.root)
       
        if self.INPpar.root=='':
            self.setRoot(self.INPpar,True)
            self.INPpar.FlagAddINPpar=FlagAddINPpar
            self.add_INPpar('root')
            return
        self.ui.label_check_root.setPixmap(self.mapw)
        self.repaint()


        if entry in self.INPpar.Pinfo.root:
            k=self.INPpar.Pinfo.root.index(entry)
            self.INPpar.pinfo=self.INPpar.Pinfo.extractPinfo(k)
            self.INPpar.root=self.INPpar.pinfo.root
            self.ui.edit_root.setText(self.INPpar.root)
            self.INPpar.FlagValidRoot=True
            self.setRoot(self.INPpar,True)
        else:
            self.getpinfofromRoot(self.INPpar.path,entry)
                        
        #self.checkRootFromList()
        self.INPpar.FlagAddINPpar=FlagAddINPpar
        self.add_INPpar('root')
    
    def button_import_callback(self):
        FlagAddINPpar= self.INPpar.FlagAddINPpar
        self.INPpar.FlagAddINPpar=False
        self.ui.label_check_root.setPixmap(self.mapw)
        filename, _ = QFileDialog.getOpenFileName(QWidget(),\
            "Select an image file of the sequence", filter=text_filter, dir=self.INPpar.path,\
                options=QFileDialog.Option.DontUseNativeDialog)
        filename=myStandardRoot('{}'.format(str(filename)))
        if not filename=='':
            directory_path = myStandardPath(os.getcwd())
            currpath, target = os.path.split(filename)
            currpath=myStandardPath(currpath)
            if directory_path in currpath:
                currpath=currpath.replace(directory_path,'./')
            if currpath==myStandardPath(self.ui.edit_path.text()):
                vk=[]
                vnimg=[]
                for k in range(len(self.INPpar.Pinfo.pa)):
                    if self.INPpar.Pinfo.pa[k].match(target):
                        vk.append(k)
                        vnimg.append(self.INPpar.Pinfo.nimg_tot[k])
                k=vk[np.argmax(np.asarray(vnimg))]                
                self.ui.edit_root.setText(self.INPpar.Pinfo.root[k])
                self.edit_root_callback()
            else:
                self.getPinfoFromPath(currpath,target)
                self.reset_preproc()
        else:
             self.setRootLabel()
        self.INPpar.FlagAddINPpar=FlagAddINPpar
        self.add_INPpar('root')

#*************************************************** Image set controls
    def spin_range_from_callback(self):
        if self.ui.spin_range_from.hasFocus():
            self.spin_range_from_action()
            
    def spin_range_from_action(self):
        value=self.ui.spin_range_from.value()
        self.INPpar.range_from=value
        if self.INPpar.selected<value:
            self.INPpar.selected=value
            self.ui.spin_selected.setValue(value)
        self.ui.spin_range_to.setMinimum(value)
        self.ui.spin_selected.setMinimum(value)
        self.setListImages()

    def spin_range_to_callback(self):
            if self.ui.spin_range_to.hasFocus():
                self.spin_range_to_action()
                
    def spin_range_to_action(self):
        value=self.ui.spin_range_to.value()
        self.INPpar.range_to=value
        if self.INPpar.selected>value:
            self.INPpar.selected=value
            self.ui.spin_selected.setValue(value)
        self.ui.spin_range_from.setMaximum(value)
        self.ui.spin_selected.setMaximum(value)
        self.setListImages()

    def spin_selected_callback(self):
        if self.ui.spin_selected.hasFocus():
            self.spin_selected_action()
            
    def spin_selected_action(self):
        self.INPpar.selected=self.ui.spin_selected.value()
        self.selectListItem()

    def selectListItem(self):
        ind=2*(self.INPpar.selected-self.INPpar.range_from)+self.INPpar.frame
        self.ui.list_images.setCurrentRow(ind)

    def spin_frame_callback(self):
        if self.ui.spin_frame.hasFocus():
            self.spin_frame_action()
            
    def spin_frame_action(self):
        self.INPpar.frame=self.ui.spin_frame.value()
        self.selectListItem()

    def list_images_callback(self):
        ind=self.ui.list_images.currentRow()
        if ind==-1: ind=0
        self.ui.spin_selected.setValue(int(ind/2)+self.INPpar.range_from)
        self.INPpar.selected=self.ui.spin_selected.value()
        self.ui.spin_frame.setValue(ind%2)
        self.INPpar.frame=self.ui.spin_frame.value()
        #self.add_INPpar('list')

#*************************************************** Sequence type and pre-proc
    def check_TR_callback(self):
        if self.ui.check_TR_sequence.hasFocus():
            FlagAddINPpar=self.INPpar.FlagAddINPpar
            self.INPpar.FlagAddINPpar=False
            self.INPpar.flag_TR=self.ui.check_TR_sequence.isChecked()
            self.setRoot(self.INPpar,True)
            self.INPpar.FlagAddINPpar=FlagAddINPpar
            self.add_INPpar('check_TR')

    def button_min_callback(self):
        self.flag_comp_min=self.ui.button_min.isChecked()
        if self.flag_comp_min:
            if self.i_min<0:
                self.flag_pause_min=False
                self.check_preproc()
                self.initializeMinThread()
                self.startMinThread()
            else:
                self.check_preproc()
                self.reinitializeMinThread()
                self.launchMinThreadWorkers()
        else:
            self.check_preproc()
            
    def initializeMinThread(self):
        threadpool=self.MIN_threadpool
        indWorker=self.indWorker
        par0=MINpar()
        par0.path=self.INPpar.path
        ind_in=self.INPpar.range_from*2
        ind_fin=(self.INPpar.range_to+1)*2
        par0.list_Image_Files=self.list_Image_Files[ind_in:ind_fin]
        par0.list_eim=self.list_eim[ind_in:ind_fin]
        par0.list_pim=[0*int(i) for i in self.list_eim]
        self.list_pim=par0.list_pim
        par0.flag_TR=self.INPpar.flag_TR
        par0.i=-1
        par0.NumThreads=threadpool.maxThreadCount()
        calcMin_workers=[]

        if par0.flag_TR: fac=2
        else: fac=1
        
        for i in range(par0.NumThreads):
            par0.i=i*fac
            calcMin_workers.append(calcMin_Worker(par0,indWorker,-1))
            calcMin_workers[i].signals.progress.connect(self.progress_min_update)
            calcMin_workers[i].signals.result.connect(self.calcMinPaused)
        #return calcMin_workers
        self.calcMin_workers=calcMin_workers

    def startMinThread(self):
        del self.Im_min_a, self.Im_min_b
        self.Im_min_a=np.array([])
        self.Im_min_b=np.array([])
        self.i_min=0

        par=self.calcMin_workers[0].par
        if par.flag_TR: fac=2
        else: fac=1
        self.ui.progress_min.setMinimum(0)
        self.ui.progress_min.setMaximum(int(len(par.list_Image_Files)/fac))
        self.ui.progress_min.setValue(self.i_min) 

        self.launchMinThreadWorkers()

    def launchMinThreadWorkers(self):
        self.DisableAll()
        for i in range(self.calcMin_workers[0].par.NumThreads):
            self.ui.button_pause_min.clicked.connect(self.calcMin_workers[i].die)
            self.signals.indProc.connect(self.calcMin_workers[i].updateIndProc)
            self.MIN_threadpool.start(self.calcMin_workers[i])
        self.indProc=0
        self.signals.indProc.emit(self.indProc)

    def reinitializeMinThread(self):
        calcMin_workers=[]
        for i in range(len(self.calcMin_workers)):
            par=self.calcMin_workers[i].par
            indWorker=self.calcMin_workers[i].indWorker
            calcMin_workers.append(calcMin_Worker(par,indWorker,-1))
            calcMin_workers[i].signals.progress.connect(self.progress_min_update)
            calcMin_workers[i].signals.result.connect(self.calcMinPaused)
        #return calcMin_workers
        self.calcMin_workers=calcMin_workers

    @Slot(int,int,object,int)
    def progress_min_update(self,ind,pim,Imin,flag_TR):
        self.i_min+=1
        self.list_pim[ind]=pim
        self.ui.progress_min.setValue(self.i_min)

    @Slot(int,object,int,int)
    def calcMinPaused(self,ind,Imin,flag_TR,nimg_proc):
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
        self.signals.pause_calcMin.emit()

        if self.i_min==nimg_proc:
            self.signals.completed_calcMin.emit()

    def calcMinPaused_reaction(self):
        self.ui.button_restart_min.setEnabled(True)
        
    def calcMinCompleted(self):
        self.ui.progress_min.setValue(self.i_min)
        self.EnableAll()
        self.flag_pause_min=True
        self.ui.button_pause_min.hide()
        self.ui.label_pause_min.show()
        self.ui.button_restart_min.setEnabled(True)

    def button_pause_min_callback(self):
        if self.flag_pause_min:
            self.ui.button_pause_min.setIcon(self.icon_pause)
            self.flag_pause_min=False
            self.ui.button_restart_min.setEnabled(False)
            self.reinitializeMinThread()
            self.launchMinThreadWorkers()
        else:
            self.EnableAll()
            self.ui.button_pause_min.setIcon(self.icon_play)
            self.flag_pause_min=True
            self.ui.button_restart_min.setEnabled(True)
    
    def button_restart_min_callback(self):
        self.i_min=-1
        self.check_preproc()
        self.initializeMinThread()
        self.startMinThread()
        self.ui.button_pause_min.setIcon(self.icon_pause)
        self.flag_pause_min=False

    def check_subtract_callback(self):
        self.flag_min=self.INPpar.flag_min=self.ui.check_subtract.isChecked()

    def reset_preproc(self):
        self.flag_comp_min=False
        self.i_min=-1
        self.check_preproc()
    

#*************************************************** Image sizes
    def spin_x_callback(self):
        if self.ui.spin_x.hasFocus():
            self.INPpar.x=self.ui.spin_x.value()
            dx=self.INPpar.W-self.INPpar.x
            self.ui.spin_w.setMaximum(dx)
            if self.ui.spin_x.Win<dx:
                dx=self.ui.spin_x.Win
            self.INPpar.w=dx
            self.ui.spin_w.setValue(dx)
            
    def spin_y_callback(self):
        if self.ui.spin_y.hasFocus():
            self.INPpar.y=self.ui.spin_y.value()
            dy=self.ui.spin_y.Win-self.INPpar.y
            self.ui.spin_h.setMaximum(dy)
            if self.ui.spin_y.Win<dy:
                dy=self.ui.spin_y.Win
            self.INPpar.h=dy    
            self.ui.spin_h.setValue(dy)
            
    def spin_w_callback(self):
        if self.ui.spin_w.hasFocus():
            self.INPpar.w=self.ui.spin_w.value()

    def spin_h_callback(self):
        if self.ui.spin_h.hasFocus():
            self.INPpar.h=self.ui.spin_h.value()

    def button_resize_callback(self):
        FlagAddINPpar=self.INPpar.FlagAddINPpar
        self.INPpar.FlagAddINPpar=False
        self.ui.spin_x.setValue(0)
        self.ui.spin_y.setValue(0)
        self.ui.spin_w.setMaximum(self.INPpar.W)
        self.ui.spin_w.setValue(self.INPpar.W)
        self.ui.spin_h.setMaximum(self.INPpar.H)
        self.ui.spin_h.setValue(self.INPpar.H)
        self.check_resize()
        self.INPpar.FlagAddINPpar=FlagAddINPpar
        self.add_INPpar('button_resize')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Import_Tab(None)
    object.show()
    sys.exit(app.exec())

