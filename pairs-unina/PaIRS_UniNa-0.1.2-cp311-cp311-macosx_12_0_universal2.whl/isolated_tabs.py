
from .gPaIRS import *
FlagHeight_Isolated=True
import sys
app = QApplication(sys.argv)
app.setStyle('Fusion')
self = gPaIRS()

tab=self.ui.w_ImportTab
#tab=self.ui.w_ExportTab
#tab=self.ui.w_ProcessTab
tab=self.ui.w_ProcessTab.ui.CollapBox_Interp
#tab=self.ui.w_ProcessTab.ui.CollapBox_Validation
#self.ui.w_ProcessTab.ui.w_Nogueira.hide()
#tab=self.ui.w_ProcessTab.ui.CollapBox_Windowing
#tab=self.ui.f_VisTab
#tab=self.ui.w_Tree
#tab=self.ui.w_LogTab

w=FloatingObject(self,tab,True,False,0)

sys.exit(app.exec())
 