from .ui_Process_Tab import *
from .PaIRS_pypacks import *
from .addwidgets_ps import*

mode_items= ('simple', #0
             'advanced', #1
             'expert') #2

top_items=( 'custom',  #0
            'preview', #1
            'fast',    #2
            'standard',#3
            'advanced',#4
            'high resolution', #5
            'adaptative resolution') #6

mode_init=mode_items[0]
top_init=top_items[3]

ImInt_items=( #************ do not change the order of items here!
            'none',                             # none
            'moving window',                    # moving window
            'linear revitalized',               # linear revitalized
            'bilinear/biquadratic/bicubic',     # bilinear/biquadratic/bicubic
            'simplex',                          # simplex
            'shift theorem',                    # shift theorem
            'sinc (Whittaker-Shannon)',         # sinc (Whittaker-Shannon)
            'B-spline'                          # B-spline
            )
ImInt_order=[i for i in range(8)] #************ change here, please!

VelInt_items=( #************ do not change the order of items here!
            'bilinear',                         # bilinear
            'linear revitalized',               # linear revitalized
            'simplex',                          # simplex
            'shift theorem',                    # shift theorem
            'shift theorem (extrapolation)',    # shift theorem (extrapolation)
            'B-spline'                          # B-spline
            )
VelInt_order=[i for i in range(7)] #************ change here, please!


Wind_items=( #************ do not change the order of items here!
            'top-hat',                          # top-hat
            'Nogueira',                         # Nogueira
            'Blackmann',                        # Blackmann
            'Blackmann-Harris',                 # Blackmann-Harris
            'triangular',                       # Triangular
            'Hann',                             # Hann
            'Gaussian',                         # Gaussian
            )
Wind_order=[i for i in range(8)] #************ change here, please!

def cont_fields(diz):
    cont=0
    for f,v in diz:
        if not 'fields' in f and f[0]!='_':
            cont+=1
    return cont
    
class PROpar:
    def __init__(self,mode,top):
        
        cont=[0]
        name_fields=['']
        #************* DEFAULT VALUES
        #******************************* base_fields
        self.name= ''

        self.FlagCustom=False
        self.prev_top=-1
        self.FlagFinIt_reset=False
        self.FlagInt_reset=False
        self.FlagValidation_reset=False
        self.FlagWind_reset=False

        if not mode in mode_items:
            self.mode=mode_items[0]
        else:
            self.mode=mode
        self.top=top

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('base')

        #******************************* IW_fields
        WSize_init=[128, 96, 64]
        WSpac_init=[ 64, 48, 32]
        self.Nit=len(WSize_init)
        Vect=[np.array(WSize_init,np.intc), np.array(WSpac_init,np.intc),\
            np.array(WSize_init,np.intc), np.array(WSpac_init,np.intc)]
        self.Vect=Vect
        self.flag_rect_wind=False
        self.FlagBordo=1

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('IW')

        #******************************* Int_fields
        self.IntIniz=1
        self.IntFin=1
        self.FlagInt=0
        self.IntCorr=0
        self.IntVel=1

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('Int')

        #******************************* FinalIt_fields
        self.FlagDirectCorr=1
        self.NIterazioni=0

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('FinalIt')

        #******************************* Validation_fields
        self.FlagMedTest=1
        self.TypeMed=1
        self.KernMed=1
        self.SogliaMed=2.0
        self.ErroreMed=0.5

        self.FlagSNTest=0
        self.SogliaSN=1.5

        self.FlagCPTest=0
        self.SogliaCP=0.2

        self.FlagNogTest=0
        self.SogliaMedia=0.25
        self.SogliaNumVet=0.10

        self.SogliaNoise=2.00
        self.SogliaStd=3.00
        self.FlagCorrezioneVel=1
        self.FlagSecMax=1
        self.FlagCorrHart=0

        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('Validation')

        #******************************* Windowing_fields
        self.FlagCalcVel=0
        self.FlagWindowing=0
        self.SemiDimCalcVel=0

        self.FlagAdaptative=0
        self.MinC=0.1
        self.MaxC=0.4
        self.LarMin=1
        self.LarMax=16
        self.FlagSommaProd=1
        
        cont.append(cont_fields(self.__dict__.items()))
        name_fields.append('Wind')

        
        if self.top==top_items[0] or self.top==top_items[1] : #preview/custom
            self.IntIniz=3
            self.IntFin=3
            self.IntVel=1
            self.NIterazioni=0
        elif self.top==top_items[2]: #fast
            self.IntIniz=1
            self.IntFin=1
            self.IntVel=1
            self.NIterazioni=1
        elif self.top==top_items[3]: #standard
            self.IntIniz=53
            self.IntFin=53
            self.IntVel=52
            self.NIterazioni=2
        elif self.top==top_items[4]: #advanced
            self.IntIniz=57
            self.IntFin=57
            self.IntVel=53
            self.NIterazioni=2

            self.FlagCalcVel=2
            self.FlagWindowing=2
        elif self.top==top_items[5]: #high resolution
            self.IntIniz=57
            self.IntFin=57
            self.IntVel=53
            self.NIterazioni=20

            self.FlagCalcVel=2
            self.FlagWindowing=2
            self.SemiDimCalcVel=3
        elif self.top==top_items[6]: #adaptative
            self.IntIniz=57
            self.IntFin=57
            self.IntVel=53
            self.NIterazioni=20

            self.FlagCalcVel=2
            self.FlagWindowing=2
            self.SemiDimCalcVel=5
            self.FlagAdaptative=1

        #******************************* ALL fields
        self.fields={}
        for f,v in self.__dict__.items():
            if not 'fields' in f and f[0]!='_':
                self.fields[f]=v

        for j in range(1,len(cont)):
            setattr(self,name_fields[j]+"_fields",[])
            d=getattr(self,name_fields[j]+"_fields")
            k=-1
            for f in self.fields:
                k+=1
                if k in range(cont[j-1],cont[j]):
                    d.append(f)

    def printPar(self):
        myprint(self.fields)

    def duplicate(self):
        newist=PROpar(self.mode,self.top)
        for f in self.fields:
            a=getattr(self,f)
            setattr(newist,f,copy.deepcopy(a))
        newist.setFields()
        return newist

    def copyfrom(self,newist):
        for f in self.fields:
            a=getattr(newist,f)
            setattr(self,f,copy.deepcopy(a))
        self.setFields()

    def copyfromdiz(self,newist,diz):
        for f in diz:
            a=getattr(newist,f)
            setattr(self,f,copy.deepcopy(a))
        self.setFields()

    def setFields(self):
        for f in self.fields:
            self.fields[f]=getattr(self,f)

    def change_top(self,top_new):
        newist=PROpar(self.mode,top_new)
        for diz in (self.Int_fields,self.FinalIt_fields,self.Wind_fields):
            for f in diz:
                setattr(self,f,getattr(newist,f))       

    def isFieldEqual(self,newist,diz):
        Flag=True
        for f in diz:
            if self.fields[f]!=newist.fields[f]:
                Flag=False
                break
        return Flag


class uiPROpar(PROpar):
    class _ReactingProp:
        def __init__(self, name_value):
            self.name=name_value[0]
            self.value=name_value[1]
        def __get__(self, instance, owner=None):
            return self.value
        def __set__(self, instance, value):
            if type(value) is list:
                if type(value[0]) is np.ndarray:
                    check=False
                    for i in range(4):
                        if np.size(value[i])!=np.size(self.value[i]):
                            check=True
                            break
                        else:
                            check=any(value[i]!=self.value[i])
                            if check: break
            else:
                check=value != self.value
            if check:
                self.value = value
                instance.fields[self.name]=self.value
                if instance.FlagAddFunc:
                    for f in instance.addfunc:
                        if f=='addPROpar' and instance.FlagAddPROpar:
                            instance.addfunc[f](self.name)
                
    @classmethod
    def __init__(self,mode,top):
        super().__init__(self,mode,top)
        self.FlagAddFunc=True
        self.FlagAddPROpar=True
        self.addfunc={}
        for name_diz in ('IW_fields','Int_fields','FinalIt_fields','Validation_fields','Wind_fields'):
            diz=getattr(self,name_diz)
            for field in diz:
                if not field in ('Nit'):
                    value=getattr(self,field)
                    setattr(self, field, self._ReactingProp([field, value]))
 
class Process_Tab(QWidget):
    
    class Process_Tab_Signals(QObject):
        add_par=Signal()

    def __init__(self,parent):
        super().__init__(parent)

        self.signals=self.Process_Tab_Signals()

        ui=Ui_ProcessTab()
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


        self.Vect_widgets=(ui.line_edit_size,\
            ui.line_edit_spacing,\
                ui.line_edit_size_2,\
                    ui.line_edit_spacing_2)

        ui.CollapBoxes=self.findChildren(CollapsibleBox)
        height_min=2^64
        for cb in ui.CollapBoxes:
            cb.setup()
            cb.initFlag=True
            if cb.heightOpened<height_min:
                height_min=cb.heightOpened

        for cb in ui.CollapBoxes:
            indx=ui.scrollAreaWidgetContents_PT.layout().indexOf(cb)
            cb.setup(indx,cb.heightOpened//height_min+1)

        #ui.CollapBox_IntWind.setup(1,6)
        #ui.CollapBox_top.setup(2,3)
        #ui.CollapBox_FinIt.setup(3,3)
        #ui.CollapBox_Interp.setup(4,10)
        #ui.CollapBox_Validation.setup(5,13)
        #ui.CollapBox_Windowing.setup(6,12)

        ui.line_edit_size.addlab=ui.check_edit_size
        ui.line_edit_size.addwid=[w for w in self.Vect_widgets]
        ui.line_edit_size.addwid.append(ui.spin_final_iter)
        ui.line_edit_spacing.addlab=ui.check_edit_spacing
        ui.line_edit_spacing.addwid=ui.line_edit_size.addwid
        ui.line_edit_size_2.addlab=ui.check_edit_size_2
        ui.line_edit_size_2.addwid=ui.line_edit_size.addwid
        ui.line_edit_spacing_2.addlab=ui.check_edit_spacing_2
        ui.line_edit_spacing_2.addwid=ui.line_edit_size.addwid

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

        #necessary to change the name and the order of the items
        ui.combo_mode.clear()
        for item in mode_items:
            ui.combo_mode.addItem(item)
        ui.combo_top.clear()
        for item in top_items:
            ui.combo_top.addItem(item)

        ui.combo_ImInt.clear()
        for i in range(len(ImInt_items)):
            ui.combo_ImInt.addItem(ImInt_items[ImInt_order[i]])
        ui.combo_ImInt_2.clear()
        for i in range(len(ImInt_items)):
            ui.combo_ImInt_2.addItem(ImInt_items[ImInt_order[i]])
        ui.combo_int_vel.clear()
        for i in range(len(VelInt_items)):
            ui.combo_int_vel.addItem(VelInt_items[VelInt_order[i]])
        ui.combo_Wind_Vel_type.clear()
        for i in range(len(Wind_items)):
            ui.combo_Wind_Vel_type.addItem(Wind_items[Wind_order[i]])
        ui.combo_Wind_Corr_type.clear()
        for i in range(len(Wind_items)):
            ui.combo_Wind_Corr_type.addItem(Wind_items[Wind_order[i]])

        self.icon_plus = QIcon()
        self.icon_plus.addFile(u""+ icons_path +"plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_minus = QIcon()
        self.icon_minus.addFile(u""+ icons_path +"minus.png", QSize(), QIcon.Normal, QIcon.Off)

        self.Lab_greenv=QPixmap(u""+ icons_path +"greenv.png")
        self.Lab_redx=QPixmap(u""+ icons_path +"redx.png")
        self.Lab_warning=QPixmap(u""+ icons_path +"warning.png")

        self.ui.button_more_size.setIconSize(self.ui.button_more_size.size()-QSize(6,6))
        self.ui.button_more_iter.setIconSize(self.ui.button_more_iter.size()-QSize(6,6))

        #mode
        ui.combo_mode.activated.connect(self.combo_mode_callback)

        #CollapBox: Interrogation Window        
        ui.button_more_size.clicked.connect(self.button_more_size_callback)

        ui.check_edit_size.setPixmap(QPixmap())
        ui.line_edit_size.textChanged.connect(\
            lambda: self.edit_Wind_vectors(ui.line_edit_size,ui.check_edit_size))
        ui.line_edit_size.returnPressed.connect(\
            lambda: self.set_Wind_vectors(ui.line_edit_size,ui.check_edit_size,0))
        ui.line_edit_size.editingFinished.connect(self.setVect)
        
        ui.check_edit_spacing.setPixmap(QPixmap())
        ui.line_edit_spacing.textChanged.connect(\
            lambda: self.edit_Wind_vectors(ui.line_edit_spacing,ui.check_edit_spacing))
        ui.line_edit_spacing.returnPressed.connect(\
            lambda: self.set_Wind_vectors(ui.line_edit_spacing,ui.check_edit_spacing,1))
        ui.line_edit_spacing.editingFinished.connect(self.setVect)
        
        ui.check_edit_size_2.setPixmap(QPixmap())
        ui.line_edit_size_2.textChanged.connect(\
            lambda: self.edit_Wind_vectors(ui.line_edit_size_2,ui.check_edit_size_2))
        ui.line_edit_size_2.returnPressed.connect(\
            lambda: self.set_Wind_vectors(ui.line_edit_size_2,ui.check_edit_size_2,2))
        ui.line_edit_size_2.editingFinished.connect(self.setVect)

        ui.check_edit_spacing_2.setPixmap(QPixmap())
        ui.line_edit_spacing_2.textChanged.connect(\
            lambda: self.edit_Wind_vectors(ui.line_edit_spacing_2,ui.check_edit_spacing_2))
        ui.line_edit_spacing_2.returnPressed.connect(\
            lambda: self.set_Wind_vectors(ui.line_edit_spacing_2,ui.check_edit_spacing_2,3))
        ui.line_edit_spacing_2.editingFinished.connect(self.setVect)
        
        ui.flag_boundary.stateChanged.connect(self.flag_boundary_callback)

        #CollapBox: Final iterations
        ui.spin_final_iter.valueChanged.connect(self.spin_final_iter_callback)
        ui.check_DC.stateChanged.connect(self.check_DC_callback)

        #CollapBox: Type of Process
        ui.combo_top.activated.connect(self.combo_top_callback)

        #CollapBox: Interpolation
        self.Flag_setImIntIndex=True
        ui.combo_ImInt.activated.connect(lambda: self.combo_ImInt_callback(ui.combo_ImInt,ui.w_ImInt_par))
        ui.combo_par_pol.activated.connect(lambda: self.setImIntIndex(ui.combo_ImInt,ui.w_ImInt_par))
        ui.combo_par_imshift.activated.connect(lambda: self.setImIntIndex(ui.combo_ImInt,ui.w_ImInt_par))
        ui.spin_order.valueChanged.connect(lambda: self.setImIntIndex(ui.combo_ImInt,ui.w_ImInt_par))

        ui.combo_ImInt_2.currentIndexChanged.connect(lambda: self.combo_ImInt_callback(ui.combo_ImInt_2,ui.w_ImInt_par_2))
        ui.combo_par_pol_2.currentIndexChanged.connect(lambda: self.setImIntIndex(ui.combo_ImInt_2,ui.w_ImInt_par_2))
        ui.combo_par_imshift_2.currentIndexChanged.connect(lambda: self.setImIntIndex(ui.combo_ImInt_2,ui.w_ImInt_par_2))
        ui.spin_order_2.valueChanged.connect(lambda: self.setImIntIndex(ui.combo_ImInt_2,ui.w_ImInt_par_2))

        ui.button_more_iter.clicked.connect(self.button_more_iter_callback)
        ui.spin_final_it.valueChanged.connect(self.spin_final_it_callback)
        ui.spin_final_it.addfuncout['check_more_iter']=self.check_more_iter
        ui.spin_final_it.addfuncreturn['check_more_iter']=self.check_more_iter

        ui.combo_correlation.activated.connect(self.combo_correlation_callback)

        ui.combo_int_vel.activated.connect(lambda: self.combo_VelInt_callback(ui.combo_int_vel,ui.w_VelInt_par))
        ui.spin_VelInt_order.valueChanged.connect(lambda: self.setVelIntIndex(ui.combo_int_vel,ui.w_VelInt_par))

        #CollapBox: Validation   
        ui.radio_MedTest.toggled.connect(self.radio_MedTest_callback)
        ui.combo_MedTest_type.activated.connect(self.combo_MedTest_type_callback)
        ui.spin_MedTest_ker.valueChanged.connect(self.spin_MedTest_ker_callback)
        ui.spin_MedTest_alfa.valueChanged.connect(self.spin_MedTest_alfa_callback)
        ui.spin_MedTest_eps.valueChanged.connect(self.spin_MedTest_eps_callback)

        ui.radio_SNTest.toggled.connect(self.radio_SNTest_callback)
        ui.spin_SNTest_thres.valueChanged.connect(self.spin_SNTest_thres_callback)
        ui.radio_CPTest.toggled.connect(self.radio_CPTest_callback)
        ui.spin_CPTest_thres.valueChanged.connect(self.spin_CPTest_thres_callback)

        ui.radio_Nogueira.toggled.connect(self.radio_Nogueira_callback)
        ui.spin_Nog_tol.valueChanged.connect(self.spin_Nog_tol_callback)
        ui.spin_Nog_numvec.valueChanged.connect(self.spin_Nog_numvec_callback)
        
        ui.spin_MinVal.valueChanged.connect(self.spin_MinVal_callback)
        ui.spin_MinStD.valueChanged.connect(self.spin_MinStD_callback)
        ui.combo_Correction_type.activated.connect(self.combo_Correction_type_callback)
        ui.check_second_peak.stateChanged.connect(self.check_second_peak_callback)
        ui.check_Hart.stateChanged.connect(self.check_Hart_callback)

        #CollapBox: Windowing
        self.Flag_setWindIndex=True
        ui.combo_Wind_Vel_type.activated.connect(lambda: self.combo_Wind_callback(ui.combo_Wind_Vel_type,ui.w_Wind_par))
        ui.combo_par_tophat.activated.connect(lambda: self.setWindIndex(ui.combo_Wind_Vel_type,ui.w_Wind_par))
        ui.combo_par_Nog.activated.connect(lambda: self.setWindIndex(ui.combo_Wind_Vel_type,ui.w_Wind_par))
        ui.combo_par_Bla.activated.connect(lambda: self.setWindIndex(ui.combo_Wind_Vel_type,ui.w_Wind_par))
        ui.combo_par_Har.activated.connect(lambda: self.setWindIndex(ui.combo_Wind_Vel_type,ui.w_Wind_par))
        ui.spin_par_Gauss.valueChanged.connect(lambda: self.setWindIndex(ui.combo_Wind_Vel_type,ui.w_Wind_par))

        ui.spin_Wind_halfwidth.valueChanged.connect(self.spin_Wind_halfwidth_callback)

        ui.combo_Wind_Corr_type.currentIndexChanged.connect(lambda: self.WindCombo_Selection(ui.combo_Wind_Corr_type,ui.w_Wind_par_2))
        ui.combo_par_tophat_2.currentIndexChanged.connect(lambda: self.setWindIndex(ui.combo_Wind_Corr_type,ui.w_Wind_par_2))
        ui.combo_par_Nog_2.currentIndexChanged.connect(lambda: self.setWindIndex(ui.combo_Wind_Corr_type,ui.w_Wind_par_2))
        ui.combo_par_Bla_2.currentIndexChanged.connect(lambda: self.setWindIndex(ui.combo_Wind_Corr_type,ui.w_Wind_par_2))
        ui.combo_par_Har_2.currentIndexChanged.connect(lambda: self.setWindIndex(ui.combo_Wind_Corr_type,ui.w_Wind_par_2))
        ui.spin_par_Gauss_2.valueChanged.connect(lambda: self.setWindIndex(ui.combo_Wind_Corr_type,ui.w_Wind_par_2))

        ui.radio_Adaptative.toggled.connect(self.radio_Adaptative_callback)
        ui.spin_min_Corr.valueChanged.connect(self.spin_min_Corr_callback)
        ui.spin_max_Corr.valueChanged.connect(self.spin_max_Corr_callback)
        ui.combo_type_of_DCs.activated.connect(self.combo_type_of_DCs_callback)
        
        #Controls
        ui.button_back.clicked.connect(self.button_back_callback)
        ui.button_forward.clicked.connect(self.button_forward_callback)

        self.PROpar_prev=[]
        self.PROpar_ind=0
        self.PROpar=uiPROpar(mode_init,top_init)
        
        self.add_PROpar('initial')
        self.setPROpar()
        self.PROpar.addfunc['addPROpar']= lambda name: self.add_PROpar(name)
        self.PROpar.addfunc["check_reset"]=lambda name=None: self.check_reset(name)
        ui.push_CollapBox_FinIt.clicked.connect(lambda: self.reset_field(self.PROpar.FinalIt_fields,ui.push_CollapBox_FinIt))
        ui.push_CollapBox_Interp.clicked.connect(lambda: self.reset_field(self.PROpar.Int_fields,ui.push_CollapBox_Interp))
        ui.push_CollapBox_Validation.clicked.connect(lambda: self.reset_field(self.PROpar.Validation_fields,ui.push_CollapBox_Validation))
        ui.push_CollapBox_Windowing.clicked.connect(lambda: self.reset_field(self.PROpar.Wind_fields,ui.push_CollapBox_Windowing))
        ui.push_CollapBox_top.clicked.connect(self.combo_top_action)

        for s in ui.spins+ui.dspins:
            s.addfuncin['spin_funcin']=lambda sp=s: self.spin_funcin(sp)
            s.addfuncout['spin_funcout']=lambda sp=s: self.spin_funcout(sp)

        self.PROpar_custom=PROpar(self.PROpar.mode,self.PROpar.top)
        self.PROpar_custom.copyfrom(self.PROpar)
        self.PROpar_custom.top='custom'
        self.PROpar.prev_top=self.ui.combo_top.currentIndex()
        ui.button_save_custom.clicked.connect(self.button_save_custom_callback)

        self.ui.button_forward.hide()
        self.ui.button_back.hide()
        
   
 #*************************************************** PROpars and controls
    def setPROpar_prev(self):
        self.PROpar.FlagAddPROpar=False
        self.setPROpar_item(self.PROpar_prev[self.PROpar_ind])
        self.PROpar.FlagAddPROpar=True
        self.display_controls()

    def setPROpar_item(self,PROpar_item):
        mode=self.PROpar.mode[:]
        self.PROpar.copyfrom(PROpar_item)
        self.PROpar.mode=mode
        self.setPROpar()
        
    def display_controls(self):
        if len(self.PROpar_prev)>1:
            self.ui.button_forward.show()
            self.ui.button_back.show()
        else:
            self.ui.button_forward.hide()
            self.ui.button_back.hide()
        if self.PROpar_ind==0:
            self.ui.button_forward.setEnabled(False)
        else:
            self.ui.button_forward.setEnabled(True)
        if self.PROpar_ind==len(self.PROpar_prev)-1:
            self.ui.button_back.setEnabled(False)
        else:
            self.ui.button_back.setEnabled(True)
        if self.PROpar_ind==0:
            self.ui.label_number.setText('')
        else:
            self.ui.label_number.setText("(-"+str(self.PROpar_ind)+")")

    def add_PROpar(self,name):
        if self.PROpar.FlagAddPROpar:
            myprint(name)
            PROpar_new=PROpar(self.PROpar.mode,self.PROpar.top)
            PROpar_new.copyfrom(self.PROpar)
            self.PROpar_prev.insert(0,PROpar_new)
            self.PROpar_ind=0
            self.signals.add_par.emit()
            self.display_controls()

    def button_back_callback(self):
        self.PROpar_ind+=1
        self.setPROpar_prev()

    def button_forward_callback(self):
        self.PROpar_ind-=1
        self.setPROpar_prev()

    def check_reset(self,name=None):
        #top=self.ui.combo_top.itemText(self.PROpar.prev_top)
        #PROpar_old=PROpar(self.PROpar.mode,top)
        PROpar_old=PROpar(self.PROpar.mode,self.PROpar.top)
        self.PROpar.FlagCustom=False
        if not self.PROpar.isFieldEqual(PROpar_old,self.PROpar.FinalIt_fields):
            self.PROpar.FlagFinIt_reset=True
            self.PROpar.FlagCustom=True
        else:
            self.PROpar.FlagFinIt_reset=False
        if not self.PROpar.isFieldEqual(PROpar_old,self.PROpar.Int_fields):
            self.PROpar.FlagInt_reset=True
            self.PROpar.FlagCustom=True
        else:
            self.PROpar.FlagInt_reset=False
        if not self.PROpar.isFieldEqual(PROpar_old,self.PROpar.Validation_fields):
            self.PROpar.FlagValidation_reset=True
            self.PROpar.FlagCustom=True
        else:
            self.PROpar.FlagValidation_reset=False
        if not self.PROpar.isFieldEqual(PROpar_old,self.PROpar.Wind_fields):
            self.PROpar.FlagWind_reset=True
            self.PROpar.FlagCustom=True
        else:
            self.PROpar.FlagWind_reset=False
        
        self.PROpar.FlagAddPROpar=False
        self.setPROpar()
        self.PROpar.FlagAddPROpar=True

    def spin_funcin(self,spin):
        self.PROpar.FlagAddPROpar=False
        self.spin_value=spin.value()
    
    def spin_funcout(self,spin):
        self.PROpar.FlagAddPROpar=True
        if self.spin_value!=spin.value():
            self.check_reset()
            self.add_PROpar(spin.objectName())
            #self.setPROpar()

    def reset_field(self,diz,push):
        top=self.ui.combo_top.itemText(self.PROpar.prev_top)
        PROpar_old=PROpar(self.PROpar.mode,top)
        self.PROpar.FlagAddPROpar=False
        self.PROpar.copyfromdiz(PROpar_old,diz)
        self.PROpar.FlagAddPROpar=True
        self.add_PROpar(push.objectName())
        self.check_reset()

    def button_save_custom_callback(self):
        self.FlagAddFunc=False
        self.PROpar.top='custom'
        self.PROpar.FlagCustom=False
        self.setPROpar_ToP()
        self.PROpar_custom.copyfrom(self.PROpar)
        self.FlagAddFunc=True


#*************************************************** From Parameters to UI
    def setPROpar(self):
        FlagAddFunc=self.PROpar.FlagAddPROpar
        self.PROpar.FlagAddPROpar=False
        self.setPROpar_IW()
        self.setPROpar_FinIt()
        self.setPROpar_ToP()
        self.setPROpar_Int()
        self.setPROpar_Valid()
        self.setPROpar_Wind()
        self.PROpar.FlagAddPROpar=FlagAddFunc
    
    def setPROpar_IW(self):
        #Interrogation Windows
        self.ui.combo_mode.setCurrentIndex(self.ui.combo_mode.findText(self.PROpar.mode))
        self.combo_mode_callback()
        self.ui.button_more_size.setChecked(self.PROpar.flag_rect_wind)
        self.button_more_size_check()
        self.setVect()
        self.ui.flag_boundary.setChecked(not self.PROpar.FlagBordo==0)
    
    def setPROpar_FinIt(self):
        #Final iterations
        self.ui.spin_final_iter.setValue(self.PROpar.NIterazioni)
        self.ui.check_DC.setChecked(not self.PROpar.FlagDirectCorr==0)
        if self.PROpar.FlagFinIt_reset:
            self.ui.push_CollapBox_FinIt.show() 
            self.ui.CollapBox_FinIt.FlagPush=True
        else:
            self.ui.push_CollapBox_FinIt.hide()
            self.ui.CollapBox_FinIt.FlagPush=False

    def setPROpar_ToP(self):
        #Type of process
        self.ui.combo_top.setCurrentIndex(self.ui.combo_top.findText(self.PROpar.top))
        if self.PROpar.FlagCustom:
            self.ui.button_save_custom.show()
            #self.ui.label_top.show()
            #top=self.ui.combo_top.itemText(self.PROpar.prev_top)
            self.ui.label_top.setText("Modified from ")

            self.ui.push_CollapBox_top.show() 
            self.ui.CollapBox_top.FlagPush=True
        else:
            self.ui.button_save_custom.hide()
            #self.ui.label_top.hide()
            self.ui.label_top.setText("Current")

            self.ui.push_CollapBox_top.hide() 
            self.ui.CollapBox_top.FlagPush=False

    def setPROpar_Int(self):
        #Interpolation
        self.ImIntIndex2UiOptions(self.PROpar.IntIniz,self.ui.combo_ImInt,self.ui.w_ImInt_par)
        self.ImIntIndex2UiOptions(self.PROpar.IntFin,self.ui.combo_ImInt_2,self.ui.w_ImInt_par_2)
        self.ui.button_more_iter.setChecked(int(self.PROpar.FlagInt))
        self.button_more_iter_check()
        self.ui.combo_correlation.setCurrentIndex(self.PROpar.IntCorr)
        self.VelIntIndex2UiOptions(self.PROpar.IntVel,self.ui.combo_int_vel,self.ui.w_VelInt_par)
        if self.PROpar.FlagInt_reset:
            self.ui.push_CollapBox_Interp.show()
            self.ui.CollapBox_Interp.FlagPush=True
        else:
            self.ui.push_CollapBox_Interp.hide()
            self.ui.CollapBox_Interp.FlagPush=False

    def setPROpar_Valid(self):
        #Validation
        self.setValidationType()
        self.ui.spin_MinVal.setValue(self.PROpar.SogliaNoise)
        self.ui.spin_MinStD.setValue(self.PROpar.SogliaStd)
        self.ui.combo_Correction_type.setCurrentIndex(self.PROpar.FlagCorrezioneVel)
        self.ui.check_second_peak.setChecked(int(self.PROpar.FlagSecMax))
        self.ui.check_Hart.setChecked(int(self.PROpar.FlagCorrHart))
        if self.PROpar.FlagValidation_reset:
            self.ui.push_CollapBox_Validation.show() 
            self.ui.CollapBox_Validation.FlagPush=True
        else:
            self.ui.push_CollapBox_Validation.hide()
            self.ui.CollapBox_Validation.FlagPush=False

    def setPROpar_Wind(self):
        #Windowing
        self.VelWindIndex2UiOptions(self.PROpar.FlagCalcVel,self.ui.combo_Wind_Vel_type,self.ui.w_Wind_par)
        self.VelWindIndex2UiOptions(self.PROpar.FlagWindowing,self.ui.combo_Wind_Corr_type,self.ui.w_Wind_par_2)
        self.ui.spin_Wind_halfwidth.setValue(self.PROpar.SemiDimCalcVel)
        self.ui.radio_Adaptative.setChecked(not self.PROpar.FlagAdaptative==0)
        self.radio_Adaptative_callback()
        self.ui.spin_min_Corr.setValue(self.PROpar.MinC)
        self.spin_min_Corr_callback()
        self.ui.spin_max_Corr.setValue(self.PROpar.MaxC)
        self.spin_max_Corr_callback()
        self.ui.spin_min_Lar.setValue(self.PROpar.LarMin)
        self.spin_min_Lar_callback()
        self.ui.spin_max_Lar.setValue(self.PROpar.LarMax)
        self.spin_max_Lar_callback()
        self.ui.combo_type_of_DCs.setCurrentIndex(self.PROpar.FlagSommaProd)
        if self.PROpar.FlagWind_reset:
            self.ui.push_CollapBox_Windowing.show() 
            self.ui.CollapBox_Windowing.FlagPush=True
        else:
            self.ui.push_CollapBox_Windowing.hide()
            self.ui.CollapBox_Windowing.FlagPush=False

#*************************************************** TYPE OF PROCESS
    def combo_top_callback(self):
        self.PROpar.top=self.ui.combo_top.currentText()
        self.combo_top_action()
            
    def combo_top_action(self):
        self.PROpar.prev_top=self.ui.combo_top.currentIndex()
        self.PROpar.FlagCustom=False
        self.PROpar.FlagFinIt_reset=False
        self.PROpar.FlagInt_reset=False
        self.PROpar.FlagValidation_reset=False
        self.PROpar.FlagWind_reset=False
        self.PROpar.FlagAddPROpar=False
        if self.PROpar.top=='custom':
            self.PROpar.copyfrom(self.PROpar_custom)
        else:
            self.PROpar.change_top(self.PROpar.top)
        self.PROpar.FlagAddPROpar=True
        self.add_PROpar('top')
        self.setPROpar()

#*************************************************** MODE   
    def combo_mode_callback(self):
        index=self.ui.combo_mode.currentIndex()
        self.PROpar.mode=mode_items[index]
        if index==0:
            self.ui.CollapBox_Interp.hide()
            self.ui.CollapBox_Validation.hide()
            self.ui.CollapBox_Windowing.hide()
        elif index==1:
            self.ui.CollapBox_Interp.show()
            self.ui.CollapBox_Validation.hide()
            self.ui.CollapBox_Windowing.hide()
        elif index==2:
            self.ui.CollapBox_Interp.show()
            self.ui.CollapBox_Validation.show()
            self.ui.CollapBox_Windowing.show()

#*************************************************** INTERROGATION WINDOWS
    def setVect(self):
        for w, v in zip(self.Vect_widgets,self.PROpar.Vect):
            text="".join([str(t)+", " for t in v[:-1]]) + str(v[-1])
            w.setText(text)
        self.check_more_iter()
   
    def button_more_size_callback(self):
        self.PROpar.flag_rect_wind=not self.PROpar.flag_rect_wind
        self.button_more_size_check()

    def button_more_size_check(self):
        if self.PROpar.flag_rect_wind:
            self.ui.button_more_size.setIcon(self.icon_minus)
            self.ui.w_IW_size_2.show()
            self.ui.label_size.setText("Width")
            self.ui.label_spacing.setText("Horizontal")
        else:
            self.ui.button_more_size.setIcon(self.icon_plus)
            self.ui.w_IW_size_2.hide()
            self.ui.label_size.setText("Size")
            self.ui.label_spacing.setText("Spacing")

    def edit_Wind_vectors(self,wedit,wlab):
        text=wedit.text()
        split_text=re.split('(\d+)', text)[1:-1:2]
        vect=np.array([int(i) for i in split_text],dtype=np.intc)
        tip=QToolTip(wedit)
        flag=not np.all(vect[:-1] >= vect[1:])
        if flag:
            wlab.setPixmap(self.Lab_warning)
            tip.showText(QCursor.pos(),"Items must be inserted in decreasing order!")
        else: 
            wlab.setPixmap(QPixmap())
            tip.hideText()
        return split_text, vect, tip, flag

    def set_Wind_vectors(self,wedit,wlab,i):
        split_text, vect, tip, flag=self.edit_Wind_vectors(wedit,wlab)
        tip.hideText()
        """
        if flag and len(vect)>1:
            j=0
            while j<len(vect)-1:
                if vect[j]<vect[j+1]:
                    break          
                j+=1          
        else:
            j=len(vect)-1
        if i==0 or i==1: #wedit.objectName()=="edit_size":
            self.PROpar.Vect[i]=vect[:j+1]
            if not self.PROpar.flag_rect_wind:
                self.PROpar.Vect[i+2]=vect
        """
        if flag: 
            self.setVect()
            wlab.setPixmap(self.Lab_redx)
        else:
            Nit_i=len(vect) 
            if Nit_i>self.PROpar.Nit:
                self.PROpar.Nit=Nit_i
            else:
                if np.all(vect[:Nit_i]==self.PROpar.Vect[i][:Nit_i]):
                    self.PROpar.Nit=Nit_i    
            Vect2=[]
            for j in range(4):
                if self.PROpar.flag_rect_wind:
                    k=j
                else: 
                    k=j%2
                if k==i:
                    Vect2.append(vect)
                else:
                    Vect2.append(self.PROpar.Vect[k])      
            self.PROpar.Vect=self.adjustVect(Vect2)
            wlab.setPixmap(self.Lab_greenv)

    def adjustVect(self,Vect):
        for (i,v) in zip(range(4),Vect):
            if self.PROpar.Nit<len(v):
                Vect[i]=v[:self.PROpar.Nit]
            elif self.PROpar.Nit>len(v):
                Vect[i]=np.append(v,np.repeat(v[-1],self.PROpar.Nit-len(v)))
        rep=np.array([0,0,0,0])
        for (i,v) in zip(range(4),Vect):
            if len(v)>1:
                while v[-1-rep[i]]==v[-2-rep[i]] and rep[i]<len(v):
                    rep[i]+=1
        #si potrebbe programmare meglio...
        dit=np.min(rep)
        if dit:
            self.PROpar.Nit-=dit
            for i in range(4):
                Vect[i]=Vect[i][:self.PROpar.Nit]
            self.ui.spin_final_iter.setValue(self.ui.spin_final_iter.value()+dit)
        self.setVect()
        return Vect

    def flag_boundary_callback(self):
        if self.ui.flag_boundary.isChecked():
            self.PROpar.FlagBordo=1
        else:
            self.PROpar.FlagBordo=0   

#*************************************************** FINAL ITERATIONS
    def spin_final_iter_callback(self):
        self.PROpar.FlagAddPROpar=False
        self.PROpar.NIterazioni=self.ui.spin_final_iter.value()
        self.check_more_iter()

    def check_DC_callback(self):
        if self.ui.check_DC.isChecked():
            self.PROpar.FlagDirectCorr=1
        else:
            self.PROpar.FlagDirectCorr=0
    
#*************************************************** INTERPOLATION
    def ImIntIndex2UiOptions(self,ind,w,p):
        self.Flag_setImIntIndex=False
        w.setCurrentIndex(-1) # necessary because the call to w.setCurrentIndex() evocates the callback function only if the index is changed!
        if ind==0:
            w.setCurrentIndex(w.findText(ImInt_items[0])) #none #così se scelgo un nome diverso è automatico
            self.combo_ImInt_callback(w,p)
        elif ind==1: #Quad4Simplex
            w.setCurrentIndex(w.findText(ImInt_items[4]))
            self.combo_ImInt_callback(w,p)
        elif ind in (3,4): #Moving S, aS
            w.setCurrentIndex(w.findText(ImInt_items[1]))
            self.combo_ImInt_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            qcombo.setCurrentIndex(ind-3)
        elif ind in (5,2,6,7): #BiLinear, BiQuad, BiCubic, BiCubic Matlab
            w.setCurrentIndex(w.findText(ImInt_items[3]))
            self.combo_ImInt_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(-1,-1,  1  ,-1,-1,  0,3,2)
            qcombo.setCurrentIndex(indeff[ind])
        elif ind==10: #Linear revitalized
            w.setCurrentIndex(w.findText(ImInt_items[2])) 
            self.combo_ImInt_callback(w,p)
        elif ind>=23 and ind<=40: #Shift
            w.setCurrentIndex(w.findText(ImInt_items[5]))
            self.combo_ImInt_callback(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-20)
        elif ind>=41 and ind<=50: #Sinc
            w.setCurrentIndex(w.findText(ImInt_items[6]))
            self.combo_ImInt_callback(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-40)
        elif ind>=52 and ind<=70: #BSpline
            w.setCurrentIndex(w.findText(ImInt_items[7]))
            self.combo_ImInt_callback(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-49)
        self.Flag_setImIntIndex=True
                  
    def ImIntUiOptions2Index(self,w,p):
        if w.currentText()==ImInt_items[0]: #none
            ind=0
        elif w.currentText()==ImInt_items[4]: #Quad4Simplex
            ind=1
        elif w.currentText()==ImInt_items[1]: #Moving S, aS
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            ind=qcombo.currentIndex()+3
        elif w.currentText()==ImInt_items[3]: #BiLinear, BiQuad, BiCubic, BiCubic Matlab
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(5,2,6,7)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==ImInt_items[2]: #Linear revitalized
            ind=10
        elif w.currentText()==ImInt_items[5]: #Shift
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+20
        elif w.currentText()==ImInt_items[6]: #Sinc 
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+40
        elif w.currentText()==ImInt_items[7]: #BSpline
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+49
        return ind

    def ImIntComboBox_selection(self,w,p):
        if w.currentText() in (ImInt_items[j] for j in(0,2,4)):
            p.setCurrentIndex(0)
        elif w.currentText()==ImInt_items[1]:
            p.setCurrentIndex(1)
        elif w.currentText()==ImInt_items[3]:
            p.setCurrentIndex(2)
        elif w.currentText() in ImInt_items[5]:
            p.setCurrentIndex(3)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Kernel width')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(3)
            qspin.setMaximum(20)
            qspin.setValue(3)
        elif w.currentText() in ImInt_items[6]:
            p.setCurrentIndex(3)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Kernel half-width')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(1)
            qspin.setMaximum(10)
            qspin.setValue(3)
        elif w.currentText() in ImInt_items[7]:
            p.setCurrentIndex(3)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Order (=Kernel width-1)')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(2)
            qspin.setMaximum(20) 
            qspin.setValue(3)
        
    def combo_ImInt_callback(self,w,p):
        self.ImIntComboBox_selection(w,p)
        self.setImIntIndex(w,p)
    
    def setImIntIndex(self,w,p):
        if self.Flag_setImIntIndex:
            ind=self.ImIntUiOptions2Index(w,p)
            if w.objectName()=='combo_ImInt':
                self.PROpar.IntIniz=ind
            else:
                self.PROpar.IntFin=ind
            #self.PROpar.printPar()
        
    def VelIntIndex2UiOptions(self,ind,w,p):
        if ind>=1 and ind<=5:
            indeff=(-1,  0,2,3,4,1)
            w.setCurrentIndex(w.findText(VelInt_items[indeff[ind]])) #così se scelgo un nome diverso è automatico
            self.combo_VelInt_callback(w,p)
        elif ind>=52 and ind<=70: #BSpline
            w.setCurrentIndex(w.findText(VelInt_items[5]))
            self.combo_VelInt_callback(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            qspin.setValue(ind-49)

    def VelIntUiOptions2Index(self,w,p):
        for j in range(5):    
            if w.currentText()==VelInt_items[j]: #none
                ind=j
                break
        if w.currentText()==VelInt_items[5]: #BSpline
            q=p.widget(p.currentIndex())
            qspin=q.findChild(QSpinBox)
            ind=qspin.value()+49
        return ind

    def VelIntComboBox_selection(self,w,p):
        if w.currentText() in (VelInt_items[j] for j in range(5)):
            p.setCurrentIndex(0)
        elif w.currentText()==VelInt_items[5]:
            p.setCurrentIndex(1)
            q=p.widget(p.currentIndex())
            qlabel=q.findChild(QLabel)
            qlabel.setText('Order (=Kernel width-1)')
            qspin=q.findChild(MyQSpin)
            qspin.setMinimum(2)
            qspin.setMaximum(20)      
            qspin.setValue(3)  
        
    def combo_VelInt_callback(self,w,p):
        self.VelIntComboBox_selection(w,p)
        self.setVelIntIndex(w,p)
    
    def setVelIntIndex(self,w,p):
        self.PROpar.IntVel=self.VelIntUiOptions2Index(w,p)
        #self.PROpar.printPar()

    def button_more_iter_callback(self):
        if self.PROpar.FlagInt==0:
            self.PROpar.FlagInt=1
        else:
            self.PROpar.FlagInt=0
        self.button_more_iter_check()

    def button_more_iter_check(self):
        if self.PROpar.FlagInt==0:
            self.ui.spin_final_it.setValue(self.PROpar.FlagInt)
            self.ui.button_more_iter.setIcon(self.icon_plus)
            self.ui.w_ImInt_2.hide()
            self.ui.w_ImInt_par_2.hide()
        else:
            self.ui.spin_final_it.setValue(self.PROpar.FlagInt)
            self.ui.button_more_iter.setIcon(self.icon_minus)
            self.ui.w_ImInt_2.show()
            self.ui.w_ImInt_par_2.show()

    def check_more_iter(self):
        max_it=len(self.PROpar.Vect[0])+self.PROpar.NIterazioni
        if max_it==1:
            self.PROpar.FlagInt=0
            #self.ui.button_more_iter.setEnabled(False)
            self.ui.button_more_iter.hide()
        else:
            self.ui.label_max_it.setText("of " +str(max_it))
            self.ui.spin_final_it.setMaximum(max_it-1)
            #self.ui.button_more_iter.setEnabled(True)
            self.ui.button_more_iter.show()
        if self.PROpar.FlagInt:
            self.ui.button_more_iter.setIcon(self.icon_minus)
            self.ui.w_ImInt_2.show()
            self.ui.w_ImInt_par_2.show()
        else:
            self.ui.button_more_iter.setIcon(self.icon_plus)
            self.ui.w_ImInt_2.hide()
            self.ui.w_ImInt_par_2.hide()

    def spin_final_it_callback(self):
        self.PROpar.FlagInt=self.ui.spin_final_it.value()
        #self.check_more_iter()
    
    def combo_correlation_callback(self):
        self.PROpar.IntCorr=self.ui.combo_correlation.currentIndex()
        #self.PROpar.printPar()
    
#*************************************************** VALIDATION
    def radio_MedTest_callback(self):
        if self.ui.radio_MedTest.isChecked():
            self.PROpar.FlagAddPROpar=False
            self.PROpar.FlagNogTest=0
            self.PROpar.FlagAddPROpar=True
            self.ui.radio_Nogueira.setChecked(False)
            self.PROpar.FlagMedTest=1
        else:
            self.PROpar.FlagMedTest=0
        self.showValTestBoxed()
    
    def radio_SNTest_callback(self):
        if self.ui.radio_SNTest.isChecked():
            self.PROpar.FlagAddPROpar=False
            self.PROpar.FlagNogTest=0
            self.PROpar.FlagAddPROpar=True
            self.ui.radio_Nogueira.setChecked(False)
            self.PROpar.FlagSNTest=1
        else:
            self.PROpar.FlagSNTest=0
        self.showValTestBoxed()
    
    def radio_CPTest_callback(self):
        if self.ui.radio_CPTest.isChecked():
            self.PROpar.FlagAddPROpar=False
            self.PROpar.FlagNogTest=0
            self.PROpar.FlagAddPROpar=True
            self.ui.radio_Nogueira.setChecked(False)
            self.PROpar.FlagCPTest=1
        else:
            self.PROpar.FlagCPTest=0
        self.showValTestBoxed()

    def radio_Nogueira_callback(self):
            if self.ui.radio_Nogueira.isChecked():
                self.PROpar.FlagAddPROpar=False
                self.PROpar.FlagMedTest=0
                self.ui.radio_MedTest.setChecked(False)
                self.PROpar.FlagSNTest=0
                self.ui.radio_SNTest.setChecked(False)
                self.PROpar.FlagCPTest=0
                self.ui.radio_CPTest.setChecked(False)
                self.PROpar.FlagAddPROpar=True
                self.PROpar.FlagNogTest=1
            else:
                self.PROpar.FlagNogTest=0
            self.showValTestBoxed()

    def setValidationType(self):
        self.checkValidationType()
        self.showValTestBoxed()
        self.ui.combo_MedTest_type.setCurrentIndex(self.PROpar.TypeMed)
        self.ui.spin_MedTest_ker.setValue(self.PROpar.KernMed)
        self.ui.spin_MedTest_alfa.setValue(self.PROpar.SogliaMed)
        self.ui.spin_MedTest_eps.setValue(self.PROpar.ErroreMed)
        self.ui.spin_SNTest_thres.setValue(self.PROpar.SogliaSN)
        self.ui.spin_CPTest_thres.setValue(self.PROpar.SogliaCP)
        self.ui.spin_Nog_tol.setValue(self.PROpar.SogliaMedia)
        self.ui.spin_Nog_numvec.setValue(self.PROpar.SogliaNumVet)
        
    def checkValidationType(self):
        self.ui.radio_MedTest.setChecked(self.PROpar.FlagMedTest)
        self.ui.radio_SNTest.setChecked(self.PROpar.FlagSNTest)
        self.ui.radio_CPTest.setChecked(self.PROpar.FlagCPTest)
        self.ui.radio_Nogueira.setChecked(self.PROpar.FlagNogTest)

    def showValTestBoxed(self):
        self.showMedTestwid()
        self.showSNTestwid()
        self.showCPTestwid()
        self.showNogTestwid()

    def showMedTestwid(self):
        if self.PROpar.FlagMedTest:
            self.ui.label_MedTest_box.show()
            self.ui.w_MedTest_type.show()
            self.ui.w_MedTest_ker.show()
            self.ui.w_MedTest_alfa.show()
            if self.PROpar.TypeMed==1:
                self.ui.w_MedTest_eps.show()
        else:
            self.ui.label_MedTest_box.hide()
            self.ui.w_MedTest_type.hide()
            self.ui.w_MedTest_ker.hide()
            self.ui.w_MedTest_alfa.hide()
            self.ui.w_MedTest_eps.hide()

    def showSNTestwid(self):
        if self.PROpar.FlagSNTest:
            self.ui.label_SNTest.show()
            self.ui.w_SNTest_thres.show()
        else:
            self.ui.label_SNTest.hide()
            self.ui.w_SNTest_thres.hide()

    def showCPTestwid(self):
        if self.PROpar.FlagCPTest:
            self.ui.label_CPTest.show()
            self.ui.w_CPTest_thres.show()
        else:
            self.ui.label_CPTest.hide()
            self.ui.w_CPTest_thres.hide()

    def showNogTestwid(self):
        if self.PROpar.FlagNogTest:
            self.ui.label_Nogueira.show()
            self.ui.w_Nog_tol.show()
            self.ui.w_Nog_numvec.show()
        else:
            self.ui.label_Nogueira.hide()
            self.ui.w_Nog_tol.hide()
            self.ui.w_Nog_numvec.hide()
        
    def combo_MedTest_type_callback(self):
        self.PROpar.TypeMed=self.ui.combo_MedTest_type.currentIndex()
        if self.PROpar.TypeMed==1:
            self.ui.w_MedTest_eps.show()
        else:
            self.ui.w_MedTest_eps.hide()
    
    def spin_MedTest_ker_callback(self):
        self.PROpar.KernMed=self.ui.spin_MedTest_ker.value()

    def spin_MedTest_alfa_callback(self):
        self.PROpar.SogliaMed=self.ui.spin_MedTest_alfa.value()
    
    def spin_MedTest_eps_callback(self):
        self.PROpar.ErroreMed=self.ui.spin_MedTest_eps.value()

    def spin_SNTest_thres_callback(self):
        self.PROpar.SogliaSN=self.ui.spin_SNTest_thres.value()
    
    def spin_CPTest_thres_callback(self):
        self.PROpar.SogliaCP=self.ui.spin_CPTest_thres.value()

    def spin_Nog_tol_callback(self):
        self.PROpar.SogliaMedia=self.ui.spin_Nog_tol.value()

    def spin_Nog_numvec_callback(self):
        self.PROpar.SogliaNumVet=self.ui.spin_Nog_numvec.value()

    def spin_MinVal_callback(self):
        self.PROpar.SogliaNoise=self.ui.spin_MinVal.value()
    
    def spin_MinStD_callback(self):
        self.PROpar.SogliaStd=self.ui.spin_MinStD.value()
    
    def combo_Correction_type_callback(self):
        self.PROpar.FlagCorrezioneVel=self.ui.combo_Correction_type.currentIndex()

    def check_second_peak_callback(self):
        if self.ui.check_second_peak.isChecked():
            self.PROpar.FlagSecMax=1
        else:
            self.PROpar.FlagSecMax=0
    
    def check_Hart_callback(self):
        if self.ui.check_Hart.isChecked():
            self.PROpar.FlagCorrHart=1
        else:
            self.PROpar.FlagCorrHart=0

#*************************************************** WINDOWING
    def VelWindIndex2UiOptions(self,ind,w,p):
        self.Flag_setWindIndex=False
        w.setCurrentIndex(-1)  # necessary because the call to w.setCurrentIndex() evocates the callback function only if the index is changed!
        if ind in (0,3,4):          # top-hat
            w.setCurrentIndex(w.findText(Wind_items[0]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(0, -1,-1, 1, 2)
            qcombo.setCurrentIndex(indeff[ind])
        elif ind in (1,21):         # Nogueira
            w.setCurrentIndex(w.findText(Wind_items[1]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            if ind==1:
                qcombo.setCurrentIndex(0)
            else:
                qcombo.setCurrentIndex(1)
        elif ind in (5,2,6):        # Blackmann
            w.setCurrentIndex(w.findText(Wind_items[2]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(-1,-1, 1, -1,-1, 0,2)
            qcombo.setCurrentIndex(indeff[ind])
        elif ind in (7,8,9,10):     # Blackmann-Harris
            w.setCurrentIndex(w.findText(Wind_items[3]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            qcombo.setCurrentIndex(ind-7)
        elif ind==22:               # Triangular
            w.setCurrentIndex(w.findText(Wind_items[4]))
            self.combo_Wind_callback(w,p)
        elif ind==23:               # Hann
            w.setCurrentIndex(w.findText(Wind_items[5]))
            self.combo_Wind_callback(w,p)
        elif ind>=100 and ind<=200: #Gaussian
            w.setCurrentIndex(w.findText(Wind_items[6]))
            self.combo_Wind_callback(w,p)
            q=p.widget(p.currentIndex())
            qspin=q.findChild(MyQDoubleSpin)
            qspin.setValue(float(ind-100)/10)
        self.Flag_setWindIndex=True

    def WindUiOptions2Index(self,w,p):
        if w.currentText()==Wind_items[0]:     # top-hat/rectangular
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(0,3,4)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==Wind_items[1]:   # Nogueira
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(1,21)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==Wind_items[2]:   # Blackmann
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(5,2,6)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==Wind_items[3]:   # Blackmann-Harris
            q=p.widget(p.currentIndex())
            qcombo=q.findChild(QComboBox)
            indeff=(7,8,9,10)
            ind=indeff[qcombo.currentIndex()]
        elif w.currentText()==Wind_items[4]:   # Triangular
            ind=22
        elif w.currentText()==Wind_items[5]:   # Hann
            ind=23
        elif w.currentText()==Wind_items[6]:   # Gaussian
            q=p.widget(p.currentIndex())
            qspin=q.findChild(MyQDoubleSpin)
            ind=int(qspin.value()*10+100)
        return ind
        
    def WindCombo_Selection(self,w,p):
        if w.currentText()==Wind_items[0]: self.ui.w_type_of_DCs.hide()
        else: self.ui.w_type_of_DCs.show()
        for i in range(4):
            if w.currentText()==Wind_items[i]:
                p.show()
                p.setCurrentIndex(i+1)
                break
        if w.currentText() in (Wind_items[j] for j in(4,5)): #triang./Hann no parameters needed
            p.hide()
        if w.currentText()==Wind_items[6]:
            p.show()
            p.setCurrentIndex(5)
        
    def combo_Wind_callback(self,w,p):
        self.WindCombo_Selection(w,p)
        self.setWindIndex(w,p)
            
    def setWindIndex(self,w,p):
        if self.Flag_setWindIndex:
            ind=self.WindUiOptions2Index(w,p)
            if w.objectName()=='combo_Wind_Vel_type':
                self.PROpar.FlagCalcVel=ind
            else:
                self.PROpar.FlagWindowing=ind
            #self.PROpar.printPar()

    def spin_Wind_halfwidth_callback(self):
        self.PROpar.SemiDimCalcVel=self.ui.spin_Wind_halfwidth.value()

    def radio_Adaptative_callback(self):
        if self.ui.radio_Adaptative.isChecked():
            self.PROpar.FlagAdaptative=1
            self.ui.w_Adaptative.show() 
        else:
            self.PROpar.FlagAdaptative=0
            self.ui.w_Adaptative.hide()

    def spin_min_Corr_callback(self):
        self.PROpar.MinC=self.ui.spin_min_Corr.value()
        self.ui.spin_max_Corr.setMinimum(self.PROpar.MinC+0.01)
        
    def spin_max_Corr_callback(self):
        self.PROpar.MaxC=self.ui.spin_max_Corr.value()
        self.ui.spin_min_Corr.setMaximum(self.PROpar.MaxC-0.01)
    
    def spin_min_Lar_callback(self):
        self.PROpar.LarMin=self.ui.spin_min_Lar.value()
        self.ui.spin_max_Lar.setMinimum(self.PROpar.LarMin+1)
        
    def spin_max_Lar_callback(self):
        self.PROpar.LarMax=self.ui.spin_max_Lar.value()
        self.ui.spin_min_Lar.setMaximum(self.PROpar.LarMax-1)
    
    def combo_type_of_DCs_callback(self):
        self.PROpar.FlagSommaProd=self.ui.combo_type_of_DCs.currentIndex()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Process_Tab(None)
    object.show()
    sys.exit(app.exec())
