from .ui_Tree_Tab import*
from .PaIRS_pypacks import*
from .addwidgets_ps import*


class TREpar:
    def __init__(self):
        self.name = ''
        self.indTree = -2
        self.past = []
        self.current = []
        self.future = []
        self.flagRun=0

        self.none_Icon = QIcon()

        self.done_Icon = QIcon()
        self.done_Icon.addFile(""+ icons_path +"done.png", QSize(), QIcon.Normal, QIcon.Off)
    
        self.cancelled_Icon = QIcon()
        self.cancelled_Icon.addFile(""+ icons_path +"cancelled.png", QSize(), QIcon.Normal, QIcon.Off)

        self.running_Icon = QIcon()
        self.running_Icon.addFile(""+ icons_path +"running.png", QSize(), QIcon.Normal, QIcon.Off)

        self.waiting_Icon = QIcon()
        self.waiting_Icon.addFile(""+ icons_path +"waiting_c.png", QSize(), QIcon.Normal, QIcon.Off)

        self.fields={}
        for f,v in self.__dict__.items():
            if f!='fields':
                self.fields[f]=v

    def setExample(self):
        name="first #1"+"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.addItem2Tree(-1,name,1,self.done_Icon)
        self.addItem2Tree(-1,"second",'a',self.cancelled_Icon)
        self.addItem2Tree(-1,"thrid",{'ciao': 2},self.done_Icon)

        self.addItem2Tree(0,"current","I am the current guy!",QIcon())

        name="Minimum #1"+"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.addItem2Tree(1,name,np.array([1,2,3]),self.running_Icon)
        self.addItem2Tree(1,"PIV process #1",np.array([1,2,3,4,5,6]), self.waiting_Icon)
        self.addItem2Tree(1,"PIV process #2",0,self.waiting_Icon)
        self.flagRun=-1

    def addItem2Tree(self,ind,name,data,icon):
        list_ipar=self.pickTree(ind)
        currentItem=QTreeWidgetItem()
        currentItem.setText(0,name)
        currentItem.setData(0,Qt.UserRole,data)
        currentItem.setIcon(0,icon)
        list_ipar.append(currentItem)

    def pickTree(self,ind):
        if ind==0:
            list_ipar=self.current
        elif ind==-1:
            list_ipar=self.past
        elif ind==1:
            list_ipar=self.future
        else:
            list_ipar=[]
        return list_ipar
        
    def printPar(self):
        myprint(self.__dict__)

    def duplicate(self):
        newist=TREpar()
        for a in TREpar().fields:
            v=copy.deepcopy(getattr(self,a))
            setattr(newist,a,v)
        self.setFields()
        return newist

    def copyfrom(self,newist):
        for a in TREpar().fields:
            v=copy.deepcopy(getattr(newist,a))
            setattr(self,a,v)
        self.setFields()

    def copyfromdiz(self,newist,diz):
        for a in diz:
            v=copy.deepcopy(getattr(newist,a))
            setattr(self,a,v)
        self.setFields()
  
    def setFields(self):
        for f in TREpar().fields:
            self.fields[f]=getattr(self,f)

class uiTREpar(TREpar):

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
        self.FlagAddFunc=False
        self.FlagAddTREEpar=True
        self.addfunc={}
        for field, value in self.fields.items():
            setattr(self, field, self._ReactingProp([field, value]))
            #setattr(self, field, value)
  
class Tree_Tab(QWidget):

    class Tree_Tab_Signals(QObject):
        selection=Signal(int,int,QTreeWidgetItem,int)

    def __init__(self,parent):
        super().__init__(parent)

        self.signals=self.Tree_Tab_Signals()

        ui=Ui_TreeTab()
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

        #c=self.findChildren(myQTreeWidget)
        #for w in c:
        #    w.addfuncout["check_Buttons"]=lambda: self.hideButtons()

        self.ui=ui
        self.itemSize=self.ui.tree_current.size()
                
        ui.tree_past.clear()
        ui.tree_current.clear()
        ui.tree_future.clear()

        self.TREpar=uiTREpar()
        self.clearTree()
        self.TREpar.setExample()
        
        ui.tree_past.itemClicked.connect(lambda i,c: self.selectItem(ui.tree_past,i,c))
        ui.tree_current.itemClicked.connect(lambda i,c: self.selectItem(ui.tree_current,i,c))
        ui.tree_future.itemClicked.connect(lambda i,c: self.selectItem(ui.tree_future,i,c))
        ui.button_delete.clicked.connect(self.removeFromTree)
        ui.button_restore.clicked.connect(self.restoreItemFromTree)

        self.setTREpar()
        self.FlagPause=True
        #self.ui.tree_future.setColumnCount(2)
        #self.ui.tree_future.setHeaderHidden(False)
        #self.ui.tree_future.setHeaderLabels(['Process','Status'])

    def setTREpar(self):
        for ind in range(-1,2):
            tree,list_ipar=self.pickTree(ind)
            for k in range(len(list_ipar)):
                currentItem=QTreeWidgetItem(tree)
                i=list_ipar[k]
                currentItem.setText(0,i.text(0))
                currentItem.setData(0,Qt.UserRole,i.data(0,Qt.UserRole))
                currentItem.setSizeHint(0,self.itemSize)
                currentItem.setIcon(0,i.icon(0))
                tree.addTopLevelItem(currentItem)
                tree.setCurrentItem(currentItem)
                list_ipar[k]=currentItem
                del i
        self.TREpar.indTree=0
        self.TREpar.current[0].setSelected(True)   
        self.ui.tree_current.setFocus()
        self.ui.tree_current.setCurrentItem(self.TREpar.current[0])
        self.checkButtons()

    def pickTree(self,ind):
        if ind==0:
            tree=self.ui.tree_current
            list_ipar=self.TREpar.current
        elif ind==-1:
            tree=self.ui.tree_past
            list_ipar=self.TREpar.past
        elif ind==1:
            tree=self.ui.tree_future
            list_ipar=self.TREpar.future
        else:
            tree=None
            list_ipar=[]
        return tree, list_ipar

    def selectTree(self,tree):
        selected_tree_name=tree.objectName()
        for i,name in enumerate(('past','current','future')):
            tree_name='tree_'+name
            t=getattr(self.ui,tree_name)
            if selected_tree_name!=tree_name:
                t.setCurrentItem(QTreeWidgetItem())  
            else:
                t.setFocus()
                ind=i-1
        return ind

    def addItem(self,ind,name,data,icon,*args):
        if not len(args):
            flagSelection=True
        else:
            flagSelection=args[0]
        self.TREpar.indTree=ind
        tree,list_ipar=self.pickTree(ind)
        currentItem=QTreeWidgetItem(tree)
        currentItem.setText(0,name)
        currentItem.setData(0,Qt.UserRole,data)
        currentItem.setSizeHint(0,self.itemSize)
        currentItem.setIcon(0,icon)
        tree.addTopLevelItem(currentItem)
        tree.setCurrentItem(currentItem)
        tree.setFocus()
        list_ipar.append(currentItem)
        if flagSelection:
            self.selectItem(tree,currentItem,0)
        #self.TREpar.indTree=self.deselectTree(tree)
        #self.checkButtons()

    def selectCurrent(self):
        self.selectItem(self.ui.tree_current,\
            self.ui.tree_current.currentItem(),0)

    def selectItem(self,tree,item,column):
        indTree_prev=self.TREpar.indTree
        self.TREpar.indTree=self.selectTree(tree)
        tree,list_ipar=self.pickTree(self.TREpar.indTree)
        tree.setCurrentItem(item)
        tree.setFocus()
        ind=tree.indexOfTopLevelItem(item)
        self.checkButtons()
        self.signals.selection.emit(indTree_prev,self.TREpar.indTree,item,column)
        #myprint(str(item.data(column,Qt.UserRole))+" = "+str(list_ipar[ind]))

    def removeFromTree(self):
        indTree=self.TREpar.indTree
        tree,list_ipar=self.pickTree(indTree)
        if tree==None: return
        i=tree.currentItem()
        if tree.objectName()=='tree_past':
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            Message="Are you sure you want to permanently delete this item?\n"+\
            "(Once delete from the past queue, you will not be able to recover the related process)"
            dlg.setText(str(Message))

            dlg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            dlg.setDefaultButton(QMessageBox.Yes)
            dlg.setIcon(QMessageBox.Warning)
            dlg.setFont(self.font())
            button = dlg.exec()
        else:
            button = QMessageBox.Yes
        if tree.objectName()=='tree_future':
            if self.TREpar.flagRun==-1:
                self.addItem(-1,i.text(0),i.data(0,Qt.UserRole),self.TREpar.cancelled_Icon,False)
            elif self.TREpar.flagRun==1:
                self.addItem(-1,i.text(0),i.data(0,Qt.UserRole),self.TREpar.done_Icon,False)
            else:
                self.addItem(-1,i.text(0),i.data(0,Qt.UserRole),QIcon(),False)
        if button == QMessageBox.Yes:
            self.removeItem(i,tree,list_ipar)

    def removeItem(self,i,tree,list_ipar,*args):
        if len(args): flag=args[0]
        else: flag=True
        self.TREpar.indTree=self.selectTree(tree)
        tree.removeItemWidget(i, 0)
        ind=tree.indexOfTopLevelItem(i)
        tree.takeTopLevelItem(ind)
        del list_ipar[ind]
        if flag:
            if len(list_ipar): 
                if ind:
                    self.selectItem(tree,list_ipar[ind-1],0)
                else:
                    self.selectItem(tree,list_ipar[ind],0)
                tree.setFocus()
            else:
                self.checkButtons()

    def restoreItemFromTree(self):
        tree,list_ipar=self.pickTree(self.TREpar.indTree)
        if tree==None: return
        i=tree.currentItem()
        self.removeItem(i,tree,list_ipar,False)
        if len(self.TREpar.future):
            self.addItem(+1,i.text(0),i.data(0,Qt.UserRole),self.TREpar.waiting_Icon)
        else:
            self.addItem(+1,i.text(0),i.data(0,Qt.UserRole),self.TREpar.running_Icon)

    def hideButtons(self):
        self.TREpar.indTree=-2
        self.checkButtons()

    def checkButtons(self):
        tree,list_ipar=self.pickTree(self.TREpar.indTree)
        flagShow=True
        if tree==None: flagShow=False
        else:
            if tree.currentItem()==None: flagShow=False
        if flagShow: 
            if self.TREpar.indTree==-1 and self.TREpar.flagRun<1 and self.FlagPause:
                self.ui.button_restore.show()
            else:
                self.ui.button_restore.hide()
            if self.TREpar.indTree in (-1,1) and self.FlagPause:
                self.ui.button_delete.show()
            else:
                self.ui.button_delete.hide()
        else:
            self.TREpar.current[0].setSelected(True)   
            self.ui.tree_current.setFocus()
            self.ui.tree_current.setCurrentItem(self.TREpar.current[0])
            self.selectItem(self.ui.tree_current,self.TREpar.current[0],0)

    def clearTree(self):
        for name in ('past','future'):
            t=getattr(self.TREpar,name)
            for i in t: 
                tree=getattr(self.ui,"tree_"+name)
                tree.removeItemWidget(i, 0)
                ind=tree.indexOfTopLevelItem(i)
                tree.takeTopLevelItem(ind)
            setattr(self.TREpar,name,[])
        self.TREpar.flagRun=0

    def clearAllTree(self):
        for name in ('past','current','future'):
            t=getattr(self.TREpar,name)
            for i in t: 
                tree=getattr(self.ui,"tree_"+name)
                tree.removeItemWidget(i, 0)
                ind=tree.indexOfTopLevelItem(i)
                tree.takeTopLevelItem(ind)
            setattr(self.TREpar,name,[])
        self.TREpar.flagRun=0


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Tree_Tab(None)
    object.show()
    sys.exit(app.exec())
