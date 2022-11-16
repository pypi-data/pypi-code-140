from .PaIRS_pypacks import *
from .ui_Export_Tab import*

outType_items={
    'binary': '.bin',
    'tecplot (binary)': '.plt', 
    #'tecplot (ASCII)':  '.plt',
}

class OUTpar:
    def __init__(self):
        self.name        		= ''    
        self.FlagSameAsInput      = True                 
        self.FlagValidPath  	= True                  
        self.path        		= basefold                    
        self.FlagSubFold 		= True                  
        self.FlagValidSubFold 	= 1                 
        self.subfold     		= 'out_PaIRS/'                       
        self.FlagSave    		= True                  
        self.FlagValidRoot    	= True                   
        self.root        		= 'out'                 
        self.ndig        		= 5                
        self.outType     		= 0                    
        self.saveAll     		= 0                     
        self.FlagImages  		= True                    
        self.x           		= 0                
        self.y           		= 0                 
        self.w           		= 0                 
        self.h           		= 0                  
        self.W           		= 1                
        self.H           		= 1                 
        self.aimop        		= [0]
        self.bimop        		= [0]
        self.vecop        		= [0]    
        self.xres        		= float(1.000)                   
        self.pixAR       		= float(1.000)                     
        self.dt          		= float(1000)       
        self.FlagAddFunc        = False
        self.FlagAddOUTpar      = True

        self.fields={}
        for f,v in self.__dict__.items():
            if f!='fields' and f[0]!='_':
                self.fields[f]=v


    def printPar(self):
        myprint(self.fields)

    def duplicate(self):
        newist=OUTpar()
        for f in self.fields:
            a=getattr(self,f)
            setattr(newist,f,copy.deepcopy(a))
        newist.setFields()
        return newist

    def copyfrom(self,newist):
        for f in OUTpar().fields:
            a=getattr(newist,f)
            setattr(self,f,copy.deepcopy(a))
        self.setFields()

    def copyfromdiz(self,newist,diz):
        for f in diz:
            a=getattr(newist,f)
            setattr(self,f,copy.deepcopy(a))
        self.setFields()

    def setFields(self):
        for f in OUTpar().fields:
            self.fields[f]=getattr(self,f)

class uiOUTpar(OUTpar):

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
                
    @classmethod
    def __init__(self):
        super().__init__(self)
        self.FlagAddFunc=True
        self.FlagAddOUTpar=True
        self.addfunc={}
        for field, value in OUTpar().fields.items():
            setattr(self, field, self._ReactingProp([field, value]))

class Export_Tab(QWidget):
    
    class Export_Tab_signals(QObject):
        add_par=Signal()

    def __init__(self,parent):
        super().__init__(parent)

        self.signals=self.Export_Tab_signals()

        ui=Ui_ExportTab()
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

        ui.CollapBoxes=self.findChildren(CollapsibleBox)
        for cb in ui.CollapBoxes:
            cb.setup()
            cb.initFlag=True

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

        ui.combo_out_type.clear()
        for item in outType_items:
            ui.combo_out_type.addItem(item)

        #for callbacks
        self.mapx  = QPixmap(''+ icons_path +'redx.png')
        self.mapv  = QPixmap(''+ icons_path +'greenv.png')
        self.mapw  = QPixmap(''+ icons_path +'waiting_c.png')
        self.Lab_warning=QPixmap(u""+ icons_path +"warning.png")

        self.aim_qtim,self.bim_qtim,self.aim,self.bim,self.v,self.vmat=self.allocateQPixmap()
        self.ui.aim.setPixmap(self.aim)  
        self.ui.aim_2.setPixmap(self.aim) 
        self.ui.bim.setPixmap(self.bim)  
        self.ui.bim_2.setPixmap(self.bim)
        for i in range(3):
            for j in range(3):
                a=getattr(self.ui,f'v{i+1:d}{j+1:d}')
                a.setPixmap(self.v[i][j])
                a=getattr(self.ui,f'v{i+1:d}{j+1:d}_2')
                a.setPixmap(self.v[i][j])
        
        self.rotate_counter = QTransform().rotate(-90)
        self.rotate_clock   = QTransform().rotate(+90)
        self.mirror_x       = QTransform().scale(1,-1)
        self.mirror_y       = QTransform().scale(-1,1)        

        """
        self.icon_play = QIcon()
        self.icon_play.addFile(u""+ icons_path +"play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_pause = QIcon()
        self.icon_pause.addFile(u""+ icons_path +"pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_done = QIcon()
        self.icon_done.addFile(u""+ icons_path +"done.png", QSize(), QIcon.Normal, QIcon.Off)
        """

        #Callbacks
        self.ui.check_save.toggled.connect(self.check_save_callback)
        self.ui.edit_root.textChanged.connect(self.edit_root_changing)
        self.ui.edit_root.returnPressed.connect(self.edit_root_callback)
        self.ui.combo_out_type.activated.connect(self.combo_out_type_callback)
        self.ui.combo_saveall.activated.connect(self.combo_saveall_callback)
        self.ui.check_same_as_input.toggled.connect(self.check_same_as_input_callback)
        self.ui.edit_path.textChanged.connect(self.edit_path_changing)
        self.ui.edit_path.returnPressed.connect(self.edit_path_callback)
        self.ui.button_path.clicked.connect(self.button_path_callback)
        self.ui.check_subfold.toggled.connect(self.check_subfold_callback)
        self.ui.edit_path_subfold.textChanged.connect(self.edit_path_subfold_changing)
        self.ui.edit_path_subfold.returnPressed.connect(self.edit_path_subfold_callback)
        

        self.ui.spin_x.textChanged.connect(self.spin_x_callback)
        self.ui.spin_x.valueChanged.connect(self.spin_x_callback)
        self.ui.spin_y.valueChanged.connect(self.spin_y_callback)
        self.ui.spin_y.textChanged.connect(self.spin_y_callback)
        self.ui.spin_w.valueChanged.connect(self.spin_w_callback)
        self.ui.spin_w.textChanged.connect(self.spin_w_callback)
        self.ui.spin_h.valueChanged.connect(self.spin_h_callback)
        self.ui.spin_h.textChanged.connect(self.spin_h_callback)
        self.ui.button_resize.clicked.connect(self.button_resize_callback)

        self.ui.button_rot_counter.clicked.connect(self.button_rot_counter_callback)
        self.ui.button_rot_clock.clicked.connect(self.button_rot_clock_callback)
        self.ui.button_mirror_x.clicked.connect(self.button_mirror_x_callback)
        self.ui.button_mirror_y.clicked.connect(self.button_mirror_y_callback)
        self.ui.button_rotv_counter.clicked.connect(self.button_rotv_counter_callback)
        self.ui.button_rotv_clock.clicked.connect(self.button_rotv_clock_callback)
        self.ui.button_flip_u.clicked.connect(self.button_flip_u_callback)
        self.ui.button_flip_v.clicked.connect(self.button_flip_v_callback)
        self.ui.button_reset_rot_flip.clicked.connect(self.button_reset_callback)  
        
        self.ui.spin_x_res.valueChanged.connect(self.spin_x_res_callback)
        self.ui.spin_y_res.valueChanged.connect(self.spin_y_res_callback)
        self.ui.spin_dt.valueChanged.connect(self.spin_dt_callback)

        #Controls
        ui.button_back.clicked.connect(self.button_back_callback)
        ui.button_forward.clicked.connect(self.button_forward_callback)

        self.OUTpar_base=OUTpar()
        self.OUTpar=uiOUTpar()

        for s in ui.spins+ui.dspins:
            if not s.objectName() in ('spin_selected','spin_frame'):
                s.addfuncin['spin_funcin']=lambda sp=s: self.spin_funcin(sp)
                s.addfuncout['spin_funcout']=lambda sp=s: self.spin_funcout(sp)

        #Initializing
        self.OUTpar_prev=[]
        self.OUTpar_ind=0
        self.OUTpar.FlagAddOUTpar=False
        self.setOUTpar()
        self.OUTpar.FlagAddOUTpar=True

        self.OUTpar_preproc=self.OUTpar

        self.add_OUTpar('initial')
        self.ui.button_forward.hide()
        self.ui.button_back.hide()
  
#*************************************************** Rotation and flip
    def allocateQPixmap(self):
        aim_qtim=ImageQt(''+ icons_path +'axes.png')
        bim_qtim=ImageQt(''+ icons_path +'background.png')
        aim=QPixmap.fromImage(aim_qtim)
        bim=QPixmap.fromImage(bim_qtim)
        v=[[[],[],[]],[[],[],[]],[[],[],[]]]
        for i in range(3):
            for j in range(3):
                v[i][j]=QPixmap.fromImage(ImageQt(''+ icons_path +''+f'v{i+1:d}{j+1:d}.png'))
        ind=np.linspace(0,2,num=3,endpoint=True)
        ind=ind.astype(int)
        vmat=np.meshgrid(ind,ind,indexing='ij')
        return aim_qtim, bim_qtim, aim, bim, v, vmat

    def reallocateQPixmap(self):
        aim=QPixmap.fromImage(self.aim_qtim)
        bim=QPixmap.fromImage(self.bim_qtim)
        v=[v[:] for v in self.v] 
        vmat=self.vmat.copy()
        return aim, bim, v, vmat

    def RotMirror(self,addop):
        if addop[0]!=0:
            self.OUTpar.aimop=self.OUTpar.aimop+[addop[0]]
            Itransf=np.eye(2,2)
            Itransf=self.imTransf_op2I(Itransf,self.OUTpar.aimop,False)
            self.OUTpar.aimop=self.imTransf_I2op(Itransf)
        if addop[1]!=0:
            self.OUTpar.bimop=self.OUTpar.bimop+[addop[1]]
            Itransf=np.eye(2,2)
            Itransf=self.imTransf_op2I(Itransf,self.OUTpar.bimop,False)
            self.OUTpar.bimop=self.imTransf_I2op(Itransf)
        if addop[2]!=0:
            self.OUTpar.vecop=self.OUTpar.vecop+[addop[2]]
            Itransf=np.eye(2,2)
            Itransf=self.imTransf_op2I(Itransf,self.OUTpar.vecop,False)
            self.OUTpar.vecop=self.imTransf_I2op(Itransf)
        if any(addop):
            aim,bim,v=self.RotMirror_Pixmaps()
            self.ui.aim_2.setPixmap(aim) 
            self.ui.bim_2.setPixmap(bim)
            for i in range(3):
                for j in range(3):
                    a=getattr(self.ui,f'v{i+1:d}{j+1:d}_2')
                    a.setPixmap(v[i][j])
        #self.displayImgEx() 
      
    def RotMirror_Pixmaps(self):
        #aim_qtim,bim_qtim,aim_rot,bim_rot,v_rot,vmat_rot = self.allocateQPixmap()
        aim_rot,bim_rot,v_rot,vmat_rot = self.reallocateQPixmap()
        for op in self.OUTpar.bimop:
            if op==1:
                bim_rot=bim_rot.transformed(self.rotate_counter)
            elif op==-1:
                bim_rot=bim_rot.transformed(self.rotate_clock)
            elif op==3:
                bim_rot=bim_rot.transformed(self.mirror_x)
            elif op==2:
                bim_rot=bim_rot.transformed(self.mirror_y)

            vmat_rot2=vmat_rot.copy()
            if op==1:  #rot 90 counter
                vmat_rot2[0]=np.rot90(vmat_rot[0],1)
                vmat_rot2[1]=np.rot90(vmat_rot[1],1)
            elif op==-1: #rot 90 clock
                vmat_rot2[0]=np.rot90(vmat_rot[0],-1)
                vmat_rot2[1]=np.rot90(vmat_rot[1],-1)
            elif op==3: #flip
                vmat_rot2[0]=np.flipud(vmat_rot[0])
                vmat_rot2[1]=np.flipud(vmat_rot[1])
            elif op==2:
                vmat_rot2[0]=np.fliplr(vmat_rot[0])
                vmat_rot2[1]=np.fliplr(vmat_rot[1])
                
            v_rot2=[v[:] for v in v_rot]  #deepcopy
            if op:
                for i in range(3):
                    for j in range(3):
                        if op==1:
                            v_rot[i][j]=v_rot2[vmat_rot2[0][i,j]][vmat_rot2[1][i,j]]
                        elif op==-1:
                            v_rot[i][j]=v_rot2[vmat_rot2[0][i,j]][vmat_rot2[1][i,j]]
                        elif op==3:
                            v_rot[i][j]=v_rot2[vmat_rot2[0][i,j]][vmat_rot2[1][i,j]]
                        elif op==2:
                            v_rot[i][j]=v_rot2[vmat_rot2[0][i,j]][vmat_rot2[1][i,j]]
            del vmat_rot2, v_rot2 

        for op in self.OUTpar.aimop:
            if op==1:
                aim_rot=aim_rot.transformed(self.rotate_counter)
            elif op==-1:
                aim_rot=aim_rot.transformed(self.rotate_clock)
            elif op==3:
                aim_rot=aim_rot.transformed(self.mirror_x)
            elif op==2:
                aim_rot=aim_rot.transformed(self.mirror_y)

        for op in self.OUTpar.vecop:  
            if op:
                for i in range(3):
                    for j in range(3):
                        if op==1:
                            v_rot[i][j]=v_rot[i][j].transformed(self.rotate_counter)
                        elif op==-1:
                            v_rot[i][j]=v_rot[i][j].transformed(self.rotate_clock)
                        elif op==3:
                            v_rot[i][j]=v_rot[i][j].transformed(self.mirror_x)
                        elif op==2:
                            v_rot[i][j]=v_rot[i][j].transformed(self.mirror_y)

        return aim_rot, bim_rot, v_rot

    def imTransf_op2I(self,I,op,flagInv):
        for i in range(len(op)):
            if op[i]==1:   #rotation counter
                I=self.matRot90(I.copy(),flagInv)
            elif op[i]==-1:  #clock
                I=self.matRot90(I.copy(), not flagInv)
            elif op[i]==3 or op[i]==2:  
                I=self.matMirror(I.copy(),op[i]-2)
        return I
            
    def matRot90(self,I,flagInv):
        #RH =(I[0,0]==I[1,1]) and (I[0,1]==-I[1,0])
        #if not RH: flagInv= not flagInv
        if not flagInv:  #direct counter
            a=I[0:np.size(I,0),0].copy()
            I[0:np.size(I,0),0]=-I[0:np.size(I,0),1]
            I[0:np.size(I,0),1]=+a   
        else:
            a=I[0:np.size(I,0),0].copy()
            I[0:np.size(I,0),0]=+I[0:np.size(I,0),1]
            I[0:np.size(I,0),1]=-a    
        return I

    def matMirror(self,I,ind):
        #ind=1 mirror_x, ind=0 mirror_y 
        I[0:np.size(I,0),ind]=-I[0:np.size(I,0),ind]
        return I
            
    def imTransf_I2op(self,I):
        op=[0]
        RHim= I[0,0]==I[1,1] and I[1,0]==-I[0,1]
        if RHim:
            if I[0,0]==1: op=[0]
            elif I[0,0]==-1: op=[1,1]
            elif I[0,1]==1: op=[1]
            elif I[0,1]==-1: op=[-1]
        else:
            if I[0,0]==1: op=[3]
            elif I[0,0]==-1: op=[2]
            elif I[0,1]==1: op=[1,2]
            elif I[0,1]==-1: op=[1,3]
        return op

    def button_rot_counter_callback(self): 
        self.RotMirror([0,1,1])
        self.add_OUTpar('rot90')

    def button_rot_clock_callback(self):
        self.RotMirror([0,-1,-1])
        self.add_OUTpar('rot-90')

    def button_mirror_x_callback(self):
        self.RotMirror([0,3,3])
        self.add_OUTpar('mirror_X')

    def button_mirror_y_callback(self):
        self.RotMirror([0,2,2])
        self.add_OUTpar('mirror_Y')

    def button_rotv_counter_callback(self):
        self.RotMirror([1,0,1])
        self.add_OUTpar('rot90_V')

    def button_rotv_clock_callback(self):
        self.RotMirror([-1,0,-1])
        self.add_OUTpar('rot-90_V')

    def button_flip_v_callback(self):
        self.RotMirror([3,0,3])
        self.add_OUTpar('mirror_Y_V')

    def button_flip_u_callback(self):
        self.RotMirror([2,0,2])
        self.add_OUTpar('mirror_X_V')
    
    def button_reset_callback(self):
        FlagAddOUTpar= self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.OUTpar.aimop=[0]
        self.OUTpar.bimop=[0]
        self.OUTpar.vecop=[0]
        self.RotMirror([-2,-2,-2])
        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
        self.add_OUTpar('reset')


#*************************************************** OUTpars and controls
    def setOUTpar_prev(self):
        self.setOUTpar_item(self.OUTpar_prev[self.OUTpar_ind])
        self.display_controls()
    
    def setOUTpar_item(self,OUTpar_item):
        self.OUTpar.copyfrom(OUTpar_item)
        self.setOUTpar()
        
    def display_controls(self):
        if len(self.OUTpar_prev)>1:
            self.ui.button_forward.show()
            self.ui.button_back.show()
        else:
            self.ui.button_forward.hide()
            self.ui.button_back.hide()
        if self.OUTpar_ind==0:
            self.ui.button_forward.setEnabled(False)
        else:
            self.ui.button_forward.setEnabled(True)
        if self.OUTpar_ind==len(self.OUTpar_prev)-1:
            self.ui.button_back.setEnabled(False)
        else:
            self.ui.button_back.setEnabled(True)
        if self.OUTpar_ind==0:
            self.ui.label_number.setText('')
        else:
            self.ui.label_number.setText("(-"+str(self.OUTpar_ind)+")")

    def add_OUTpar(self,name):
        FlagAdd=self.OUTpar.FlagAddOUTpar
        if len(self.OUTpar_prev):
            if self.OUTpar_prev[0].fields==self.OUTpar.fields:
                FlagAdd=False
        if FlagAdd:
            myprint(name)
            OUTpar_new=OUTpar()
            OUTpar_new.copyfrom(self.OUTpar)
            self.OUTpar_prev.insert(0,OUTpar_new)
            self.OUTpar_ind=0
            self.signals.add_par.emit()
            self.display_controls()

    def button_back_callback(self):
        self.OUTpar_ind+=1
        self.setOUTpar_prev()

    def button_forward_callback(self):
        self.OUTpar_ind-=1
        self.setOUTpar_prev()

    def spin_funcin(self,spin):
        self.spin_value=spin.value()

    def spin_funcout(self,spin):
        if self.spin_value!=spin.value():
            self.add_OUTpar(spin.objectName())
            self.check_resize()

    def check_resize(self):
        if self.OUTpar.W!=self.ui.spin_w.value() or \
            self.OUTpar.H!=self.ui.spin_h.value():
            self.ui.button_resize.show()
        else:
            self.ui.button_resize.hide()

#*************************************************** From Parameters to UI
    def setOUTpar(self):
        FlagAddOUTpar=self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.ui.check_save.setChecked(self.OUTpar.FlagSave)
        self.check_save_action()
        self.ChangeText_root(self.OUTpar.root,self.ui.w_edit_root)
        self.checkRoot()
        self.ui.check_same_as_input.setChecked(self.OUTpar.FlagSameAsInput)
        self.ChangeText_path(self.OUTpar.path,self.ui.w_edit_path)
        self.checkPath()
        self.ui.check_subfold.setChecked(self.OUTpar.FlagSubFold)
        self.check_subfold_action()
        self.ChangeText_path(self.OUTpar.subfold,self.ui.w_edit_path_subfold)
        self.checkSubFold()
        self.RotMirror([-2,-2,-2])
        self.check_Images()
        self.setResolution()
        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar    
        
    def ChangeText_path(self,text,w): 
        label=w.findChild(QLabel)
        label.setPixmap(QPixmap())
        text=myStandardPath(text)
        edit=w.findChild(MyQLineEdit)
        edit.setText(text)

    def ChangeText_root(self,text,w): 
        label=w.findChild(QLabel)
        label.setPixmap(QPixmap())
        text=myStandardRoot(text)
        edit=w.findChild(MyQLineEdit)
        edit.setText(text)
 
    def check_subfold_action(self):
        if not self.OUTpar.FlagSubFold:
            self.ui.w_OutputSubfold_name.hide()
        else:
            self.ui.w_OutputSubfold_name.show()
            self.ChangeText_path(self.OUTpar.subfold,self.ui.w_edit_path_subfold)
            self.edit_path_subfold_callback()
     
    def check_save_action(self):
        if not self.OUTpar.FlagSave:
            self.ui.w_SaveResults.hide()
            self.ui.w_OutputFold_Button.hide()
            self.ui.w_OutputSubfold.hide()
        else:
            self.ui.w_SaveResults.show()
            self.ChangeText_root(self.OUTpar.root)
            self.ui.combo_out_type.setCurrentIndex(self.OUTpar.outType)
            self.ui.combo_saveall.setCurrentIndex(self.OUTpar.saveAll)
            self.ui.w_OutputFold_Button.show()
            self.ui.w_OutputSubfold.show()

    def ChangeText_root(self,text,*args):
        self.ui.label_check_root.setPixmap(QPixmap())
        self.ui.edit_root.setText(text)

    def check_Images(self):
        if not self.OUTpar.FlagImages:
            self.ui.CollapBox_Flip.hide()
            self.ui.w_Resolution.hide()
        else:
            self.ui.CollapBox_Flip.show()
            self.ui.w_Resolution.show()
            self.setMinMaxSpin()
            self.ui.spin_x.setValue(self.OUTpar.x)
            self.ui.spin_y.setValue(self.OUTpar.y)
            self.ui.spin_w.setValue(self.OUTpar.w)
            self.ui.spin_h.setValue(self.OUTpar.h)
            self.check_resize()

    def setMinMaxSpin(self):
        self.ui.spin_x.setMinimum(0)
        self.ui.spin_x.setMaximum(self.OUTpar.W-1)
        self.ui.spin_y.setMinimum(0)
        self.ui.spin_y.setMaximum(self.OUTpar.H-1)
        self.ui.spin_w.setMinimum(1)
        self.ui.spin_w.setMaximum(self.OUTpar.W)
        self.ui.spin_h.setMinimum(1)
        self.ui.spin_h.setMaximum(self.OUTpar.H)
  
    def check_resize(self):
        if self.OUTpar.W!=self.ui.spin_w.value() or \
            self.OUTpar.H!=self.ui.spin_h.value():
            self.ui.button_resize.show()
        else:
            self.ui.button_resize.hide()

    def displayImgEx(self):
        if all([not i for i in self.OUTpar.imop]):
            self.ui.w_Im_ex_2.hide()
            self.ui.label_Im_example.setText("No transformation")
        else:
            self.ui.w_Im_ex_2.show()
            self.ui.label_Im_example.setText("Original")

    def adjustResLabel(self):
        Velx=float(1000/(self.OUTpar.xres*self.OUTpar.dt))
        Vely=float(Velx/self.OUTpar.pixAR)
        self.ui.label_Res_x.setText(f"X: {Velx:.6g} m/s")
        self.ui.label_Res_y.setText(f"Y: {Vely:.6g} m/s")

    def setResolution(self):
        self.ui.spin_x_res.setValue(self.OUTpar.xres)
        self.ui.spin_y_res.setValue(self.OUTpar.pixAR)
        self.ui.spin_dt.setValue(self.OUTpar.dt)
        self.adjustResLabel()

#*************************************************** Edit path and root
#******************** path
    def check_same_as_input_callback(self):
        self.OUTpar.FlagSameAsInput=self.ui.check_same_as_input.isChecked()
        if self.OUTpar.FlagSameAsInput:
            self.ui.w_OutputFold.setEnabled(False)
            self.ui.w_button_path.setEnabled(False)
        else:
            self.ui.w_OutputFold.setEnabled(True)
            self.ui.w_button_path.setEnabled(True)

    def edit_path_changing(self): 
         self.ui.label_check_path.setPixmap(QPixmap()) 

    def edit_path_callback(self):
        FlagAddOUTpar= self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.ui.edit_path.setEnabled(True)

        currpath=myStandardPath(self.ui.edit_path.text())
        if currpath==myStandardPath(self.OUTpar.path):
            self.ui.label_check_path.setPixmap(QPixmap())
            self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
            return 
        self.ChangeText_path(currpath,self.ui.w_edit_path)
              
        self.OUTpar.path=currpath        
        self.checkPath()
        
        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
        self.add_OUTpar('path')
    
    def checkPath(self):
        self.OUTpar.FlagValidPath=os.path.exists(self.OUTpar.path)
        if self.OUTpar.FlagValidPath:
            self.ui.label_check_path.setPixmap(self.mapv)
            self.ui.label_check_path.setToolTip("This path exists! 😃")
        else:
            self.ui.label_check_path.setPixmap(self.mapx)
            self.ui.label_check_path.setToolTip("This path does not exist! 😞")

    def button_path_callback(self):
        directory = str(QFileDialog.getExistingDirectory(QWidget(),\
            "Choose a folder", dir=self.OUTpar.path,options=QFileDialog.Option.DontUseNativeDialog))
        currpath='{}'.format(directory)
        if not currpath=='':
            currpath=myStandardPath(currpath)
            directory_path = myStandardPath(os.getcwd())
            if directory_path in currpath:
                currpath=currpath.replace(directory_path,'./')
            self.ui.edit_path.setText(currpath)
            self.edit_path_callback()

#******************** subfold
    def check_subfold_callback(self):
        self.OUTpar.FlagSubFold=self.ui.check_subfold.isChecked()
        self.check_subfold_action()

    def edit_path_subfold_changing(self): 
         self.ui.label_check_path_subfold.setPixmap(QPixmap()) 

    def edit_path_subfold_callback(self):
        FlagAddOUTpar= self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.ui.edit_path_subfold.setEnabled(True)

        subfold=myStandardPath(self.ui.edit_path_subfold.text())
        if subfold==myStandardPath(self.OUTpar.path):
            self.ui.label_check_path_subfold.setPixmap(QPixmap())
            self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
            return  
        self.ChangeText_path(subfold,self.ui.w_edit_path_subfold)

        self.OUTpar.subfold=subfold
        self.checkSubFold()

        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
        self.add_OUTpar('subfold')

    def checkSubFold(self):
        if self.OUTpar.FlagValidPath:
            currpath=myStandardPath(self.OUTpar.path)
        else:
            currpath='./'
        currpath=myStandardPath(currpath+self.OUTpar.subfold)
        if  self.OUTpar.FlagValidPath and os.path.exists(currpath):
            self.ui.label_check_path_subfold.setPixmap(self.Lab_warning)
            self.ui.label_check_path_subfold.setToolTip("Current path already exists! 😰")
            self.OUTpar.FlagValidSubFold=-1
        else:
            try:
                os.mkdir(currpath)
            except:
                self.ui.label_check_path_subfold.setPixmap(self.mapx)
                self.ui.label_check_path_subfold.setToolTip("Pathname not admitted! 😞")
                self.OUTpar.FlagValidSubFold=0
            else:
                os.rmdir(currpath)
                self.ui.label_check_path_subfold.setPixmap(self.mapv)
                self.ui.label_check_path_subfold.setToolTip("Pathname admitted! 😃")
                self.OUTpar.FlagValidSubFold=1

#******************** root
    def check_save_callback(self):
        self.OUTpar.FlagSave=self.ui.check_save.isChecked()
        self.check_save_action()

    def edit_root_changing(self):
         self.ui.label_check_root.setPixmap(QPixmap()) 
        
    def edit_root_callback(self):
        FlagAddOUTpar= self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.ui.label_check_root.setPixmap(self.mapw)
        self.ui.edit_root.setEnabled(True)
        self.repaint()

        entry=myStandardRoot(self.ui.edit_root.text())
        if entry==myStandardRoot(self.OUTpar.root):
            self.ui.label_check_root.setPixmap(QPixmap())
            self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
            return
        self.ChangeText_root(entry)

        self.OUTpar.root=entry
        self.checkRoot()

        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
        self.add_OUTpar('root')

    def checkRoot(self):
        sdig='\\d{'+str(self.OUTpar.ndig)+'}'
        ext=outType_items[self.ui.combo_out_type.itemText(self.OUTpar.outType)]
        expr=myStandardRoot(self.OUTpar.path+self.OUTpar.subfold+self.OUTpar.root+'_'+sdig+ext)
        pa=re.compile(expr)
        FlagExistPath=False
        FlagCreateSubFold=False
        if self.OUTpar.FlagValidPath:
            currpath=myStandardPath(self.OUTpar.path)
            if self.OUTpar.FlagValidSubFold:
                currpath=myStandardPath(currpath+self.OUTpar.subfold)
                if self.OUTpar.FlagValidSubFold==1: FlagCreateSubFold=True
                elif self.OUTpar.FlagValidSubFold==-1: FlagExistPath=True
        else:
            currpath='./'
        pattern=myStandardRoot(currpath+self.OUTpar.root+'*'+ext)
        if FlagExistPath:
            files=findFiles_sorted(pattern)
            FlagExist=len(files)>0
            if FlagExist:
                FlagExist=False
                for f in files:
                    if pa.match(f):
                        FlagExist=True
                        break
        else:
            FlagExist=False
        if  FlagExist:
            self.ui.label_check_root.setPixmap(self.Lab_warning)
            self.ui.label_check_root.setToolTip("There are files with the same filename root in the selected path! 😰")
            self.OUTpar.FlagValidRoot=-1
        else:
            try:
                FlagCreateSubFold=FlagCreateSubFold and not os.path.exists(currpath)
                if FlagCreateSubFold:
                    currpath=myStandardPath(currpath)
                    os.mkdir(currpath)
                filename=pattern.replace('*','a0')+'.delmeplease'
                open(filename,'w')
            except:
                self.ui.label_check_root.setPixmap(self.mapx)
                self.ui.label_check_root.setToolTip("Filename root not admitted! 😞")
                self.OUTpar.FlagValidRoot=0
            else:
                os.remove(filename)
                self.ui.label_check_root.setPixmap(self.mapv)
                self.ui.label_check_root.setToolTip("Filename root admitted! 😃")
                self.OUTpar.FlagValidRoot=1
            if FlagCreateSubFold:
                os.rmdir(currpath)
            
    def combo_out_type_callback(self):
        FlagAddOUTpar= self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.OUTpar.outType=self.ui.combo_out_type.currentIndex()
        self.checkRoot()
        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
        self.add_OUTpar('outtype')

    def combo_saveall_callback(self):
        FlagAddOUTpar= self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.OUTpar.saveAll=self.ui.combo_saveall.currentIndex()
        self.checkRoot()
        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
        self.add_OUTpar('saveall')
    
#*************************************************** Image sizes
    def spin_x_callback(self):
        if self.ui.spin_x.hasFocus():
            self.OUTpar.x=self.ui.spin_x.value()
            dx=self.OUTpar.W-self.OUTpar.x
            self.ui.spin_w.setMaximum(dx)
            if self.ui.spin_x.Win<dx:
                dx=self.ui.spin_x.Win
            self.OUTpar.w=dx
            self.ui.spin_w.setValue(dx)
            
    def spin_y_callback(self):
        if self.ui.spin_y.hasFocus():
            self.OUTpar.y=self.ui.spin_y.value()
            dy=self.ui.spin_y.Win-self.OUTpar.y
            self.ui.spin_h.setMaximum(dy)
            if self.ui.spin_y.Win<dy:
                dy=self.ui.spin_y.Win
            self.OUTpar.h=dy    
            self.ui.spin_h.setValue(dy)
            
    def spin_w_callback(self):
        if self.ui.spin_w.hasFocus():
            self.OUTpar.w=self.ui.spin_w.value()

    def spin_h_callback(self):
        if self.ui.spin_h.hasFocus():
            self.OUTpar.h=self.ui.spin_h.value()

    def button_resize_callback(self):
        FlagAddOUTpar=self.OUTpar.FlagAddOUTpar
        self.OUTpar.FlagAddOUTpar=False
        self.ui.spin_x.setValue(0)
        self.ui.spin_y.setValue(0)
        self.ui.spin_w.setMaximum(self.OUTpar.W)
        self.ui.spin_w.setValue(self.OUTpar.W)
        self.ui.spin_h.setMaximum(self.OUTpar.H)
        self.ui.spin_h.setValue(self.OUTpar.H)
        self.check_resize()
        self.OUTpar.FlagAddOUTpar=FlagAddOUTpar
        self.add_OUTpar('button_resize')

#*************************************************** Resolution
    def spin_x_res_callback(self):
        if self.ui.spin_x_res.hasFocus():
            self.OUTpar.xres=self.ui.spin_x_res.value()
            self.adjustResLabel()

    def spin_y_res_callback(self):
        if self.ui.spin_y_res.hasFocus():
            self.OUTpar.pixAR=self.ui.spin_y_res.value()
            self.adjustResLabel()

    def spin_dt_callback(self):
        if self.ui.spin_dt.hasFocus():
            self.OUTpar.dt=self.ui.spin_dt.value()
            self.adjustResLabel()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Export_Tab(None)
    object.show()
    sys.exit(app.exec())

