from .addwidgets_ps import icons_path
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gPairs.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStatusBar, QToolButton, QVBoxLayout, QWidget)

from .Export_Tab import Export_Tab
from .Import_Tab import Import_Tab
from .Log_Tab import Log_Tab
from .Process_Tab import Process_Tab
from .Tree_Tab import Tree_Tab
from .addwidgets_ps import (MplCanvas, MyTabLabel)

class Ui_gPairs(object):
    def setupUi(self, gPairs):
        if not gPairs.objectName():
            gPairs.setObjectName(u"gPairs")
        gPairs.resize(1200, 800)
        gPairs.setMinimumSize(QSize(900, 0))
        icon1 = QIcon()
        icon1.addFile(u""+ icons_path +"logo_PaIRS.png", QSize(), QIcon.Normal, QIcon.Off)
        gPairs.setWindowIcon(icon1)
        gPairs.setUnifiedTitleAndToolBarOnMac(False)
        self.actionExit = QAction(gPairs)
        self.actionExit.setObjectName(u"actionExit")
        self.aExit = QAction(gPairs)
        self.aExit.setObjectName(u"aExit")
        self.actionSave = QAction(gPairs)
        self.actionSave.setObjectName(u"actionSave")
        self.actionLoad = QAction(gPairs)
        self.actionLoad.setObjectName(u"actionLoad")
        self.actionNew = QAction(gPairs)
        self.actionNew.setObjectName(u"actionNew")
        self.actionAbout = QAction(gPairs)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionGuide = QAction(gPairs)
        self.actionGuide.setObjectName(u"actionGuide")
        self.centralwidget = QWidget(gPairs)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1080, 0))
        self.main_lay = QHBoxLayout(self.centralwidget)
        self.main_lay.setSpacing(20)
        self.main_lay.setObjectName(u"main_lay")
        self.main_lay.setContentsMargins(15, 5, 15, 5)
        self.w_Managing_Tabs = QWidget(self.centralwidget)
        self.w_Managing_Tabs.setObjectName(u"w_Managing_Tabs")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_Managing_Tabs.sizePolicy().hasHeightForWidth())
        self.w_Managing_Tabs.setSizePolicy(sizePolicy)
        self.w_Managing_Tabs.setMinimumSize(QSize(290, 0))
        self.w_Managing_Tabs.setMaximumSize(QSize(810, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.w_Managing_Tabs)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.w_Buttons_Run = QWidget(self.w_Managing_Tabs)
        self.w_Buttons_Run.setObjectName(u"w_Buttons_Run")
        self.w_Buttons_Run.setMinimumSize(QSize(0, 80))
        self.w_Buttons_Run.setMaximumSize(QSize(16777215, 80))
        self.horizontalLayout_9 = QHBoxLayout(self.w_Buttons_Run)
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.logo = QLabel(self.w_Buttons_Run)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(92, 60))
        self.logo.setMaximumSize(QSize(92, 60))
        self.logo.setPixmap(QPixmap(u""+ icons_path +"logo_PaIRS_rect.png"))
        self.logo.setScaledContents(True)

        self.horizontalLayout_9.addWidget(self.logo)

        self.hs_logo = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.hs_logo)

        self.progress_Proc = QProgressBar(self.w_Buttons_Run)
        self.progress_Proc.setObjectName(u"progress_Proc")
        sizePolicy.setHeightForWidth(self.progress_Proc.sizePolicy().hasHeightForWidth())
        self.progress_Proc.setSizePolicy(sizePolicy)
        self.progress_Proc.setMinimumSize(QSize(100, 40))
        self.progress_Proc.setMaximumSize(QSize(100, 40))
        font = QFont()
        font.setKerning(True)
        self.progress_Proc.setFont(font)
        self.progress_Proc.setStyleSheet(u"")
        self.progress_Proc.setValue(24)
        self.progress_Proc.setAlignment(Qt.AlignCenter)
        self.progress_Proc.setInvertedAppearance(False)

        self.horizontalLayout_9.addWidget(self.progress_Proc)

        self.button_pause = QToolButton(self.w_Buttons_Run)
        self.button_pause.setObjectName(u"button_pause")
        sizePolicy.setHeightForWidth(self.button_pause.sizePolicy().hasHeightForWidth())
        self.button_pause.setSizePolicy(sizePolicy)
        self.button_pause.setMinimumSize(QSize(40, 40))
        self.button_pause.setMaximumSize(QSize(40, 40))
        font1 = QFont()
        font1.setPointSize(16)
        self.button_pause.setFont(font1)
        self.button_pause.setToolTipDuration(-1)
        self.button_pause.setLayoutDirection(Qt.LeftToRight)
        icon2 = QIcon()
        icon2.addFile(u""+ icons_path +"pause.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_pause.setIcon(icon2)
        self.button_pause.setIconSize(QSize(28, 28))
        self.button_pause.setPopupMode(QToolButton.DelayedPopup)
        self.button_pause.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_9.addWidget(self.button_pause)

        self.button_delete = QToolButton(self.w_Buttons_Run)
        self.button_delete.setObjectName(u"button_delete")
        sizePolicy.setHeightForWidth(self.button_delete.sizePolicy().hasHeightForWidth())
        self.button_delete.setSizePolicy(sizePolicy)
        self.button_delete.setMinimumSize(QSize(40, 40))
        self.button_delete.setMaximumSize(QSize(40, 40))
        self.button_delete.setFont(font1)
        self.button_delete.setLayoutDirection(Qt.LeftToRight)
        icon3 = QIcon()
        icon3.addFile(u""+ icons_path +"delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_delete.setIcon(icon3)
        self.button_delete.setIconSize(QSize(28, 28))
        self.button_delete.setPopupMode(QToolButton.DelayedPopup)
        self.button_delete.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.horizontalLayout_9.addWidget(self.button_delete)

        self.button_Run = QPushButton(self.w_Buttons_Run)
        self.button_Run.setObjectName(u"button_Run")
        sizePolicy.setHeightForWidth(self.button_Run.sizePolicy().hasHeightForWidth())
        self.button_Run.setSizePolicy(sizePolicy)
        self.button_Run.setMinimumSize(QSize(0, 40))
        self.button_Run.setMaximumSize(QSize(16777215, 40))
        self.button_Run.setFont(font1)

        self.horizontalLayout_9.addWidget(self.button_Run)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.w_Buttons_Run)

        self.f_Tree_Process = QFrame(self.w_Managing_Tabs)
        self.f_Tree_Process.setObjectName(u"f_Tree_Process")
        sizePolicy.setHeightForWidth(self.f_Tree_Process.sizePolicy().hasHeightForWidth())
        self.f_Tree_Process.setSizePolicy(sizePolicy)
        self.f_Tree_Process.setMinimumSize(QSize(280, 0))
        self.f_Tree_Process.setMaximumSize(QSize(800, 16777215))
        self.f_Tree_Process.setStyleSheet(u"QFrame#f_Tree_Process{\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.f_Tree_Process)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.w_Tree = Tree_Tab(self.f_Tree_Process)
        self.w_Tree.setObjectName(u"w_Tree")

        self.verticalLayout_4.addWidget(self.w_Tree)


        self.verticalLayout_3.addWidget(self.f_Tree_Process)


        self.main_lay.addWidget(self.w_Managing_Tabs)

        self.w_Operating_Tabs = QWidget(self.centralwidget)
        self.w_Operating_Tabs.setObjectName(u"w_Operating_Tabs")
        sizePolicy.setHeightForWidth(self.w_Operating_Tabs.sizePolicy().hasHeightForWidth())
        self.w_Operating_Tabs.setSizePolicy(sizePolicy)
        self.w_Operating_Tabs.setMinimumSize(QSize(700, 0))
        self.oplay = QVBoxLayout(self.w_Operating_Tabs)
        self.oplay.setSpacing(5)
        self.oplay.setObjectName(u"oplay")
        self.oplay.setContentsMargins(0, 0, 0, 0)
        self.w_Buttons = QWidget(self.w_Operating_Tabs)
        self.w_Buttons.setObjectName(u"w_Buttons")
        self.w_Buttons.setMinimumSize(QSize(700, 80))
        self.w_Buttons.setMaximumSize(QSize(16777215, 90))
        self.horizontalLayout_3 = QHBoxLayout(self.w_Buttons)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.w_button_Shape = QWidget(self.w_Buttons)
        self.w_button_Shape.setObjectName(u"w_button_Shape")
        self.w_button_Shape.setMinimumSize(QSize(80, 40))
        self.w_button_Shape.setSizeIncrement(QSize(40, 40))
        self.horizontalLayout_4 = QHBoxLayout(self.w_button_Shape)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.button_dock = QToolButton(self.w_button_Shape)
        self.button_dock.setObjectName(u"button_dock")
        self.button_dock.setMinimumSize(QSize(30, 30))
        self.button_dock.setMaximumSize(QSize(30, 30))
        self.button_dock.setFont(font1)
        icon4 = QIcon()
        icon4.addFile(u""+ icons_path +"undock_tabs.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_dock.setIcon(icon4)
        self.button_dock.setIconSize(QSize(20, 20))
        self.button_dock.setCheckable(False)

        self.horizontalLayout_4.addWidget(self.button_dock)

        self.button_Shape = QToolButton(self.w_button_Shape)
        self.button_Shape.setObjectName(u"button_Shape")
        self.button_Shape.setMinimumSize(QSize(30, 30))
        self.button_Shape.setMaximumSize(QSize(30, 30))
        self.button_Shape.setFont(font1)
        icon5 = QIcon()
        icon5.addFile(u""+ icons_path +"menu_docked.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_Shape.setIcon(icon5)
        self.button_Shape.setIconSize(QSize(26, 26))
        self.button_Shape.setCheckable(False)

        self.horizontalLayout_4.addWidget(self.button_Shape)


        self.horizontalLayout_3.addWidget(self.w_button_Shape)

        self.button_Input = QPushButton(self.w_Buttons)
        self.button_Input.setObjectName(u"button_Input")
        sizePolicy.setHeightForWidth(self.button_Input.sizePolicy().hasHeightForWidth())
        self.button_Input.setSizePolicy(sizePolicy)
        self.button_Input.setMinimumSize(QSize(110, 40))
        self.button_Input.setMaximumSize(QSize(16777215, 40))
        self.button_Input.setFont(font1)
        self.button_Input.setStyleSheet(u"QPushButton:checked {\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u""+ icons_path +"import_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_Input.setIcon(icon6)
        self.button_Input.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.button_Input)

        self.button_Output = QPushButton(self.w_Buttons)
        self.button_Output.setObjectName(u"button_Output")
        sizePolicy.setHeightForWidth(self.button_Output.sizePolicy().hasHeightForWidth())
        self.button_Output.setSizePolicy(sizePolicy)
        self.button_Output.setMinimumSize(QSize(110, 40))
        self.button_Output.setMaximumSize(QSize(16777215, 40))
        self.button_Output.setFont(font1)
        self.button_Output.setStyleSheet(u"QPushButton:checked {\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u""+ icons_path +"export_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_Output.setIcon(icon7)
        self.button_Output.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.button_Output)

        self.button_Process = QPushButton(self.w_Buttons)
        self.button_Process.setObjectName(u"button_Process")
        sizePolicy.setHeightForWidth(self.button_Process.sizePolicy().hasHeightForWidth())
        self.button_Process.setSizePolicy(sizePolicy)
        self.button_Process.setMinimumSize(QSize(110, 40))
        self.button_Process.setMaximumSize(QSize(16777215, 40))
        self.button_Process.setFont(font1)
        self.button_Process.setStyleSheet(u"QPushButton:checked {\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u""+ icons_path +"process_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_Process.setIcon(icon8)
        self.button_Process.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.button_Process)

        self.button_Log = QPushButton(self.w_Buttons)
        self.button_Log.setObjectName(u"button_Log")
        sizePolicy.setHeightForWidth(self.button_Log.sizePolicy().hasHeightForWidth())
        self.button_Log.setSizePolicy(sizePolicy)
        self.button_Log.setMinimumSize(QSize(110, 40))
        self.button_Log.setMaximumSize(QSize(16777215, 40))
        self.button_Log.setFont(font1)
        self.button_Log.setStyleSheet(u"QPushButton:checked {\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u""+ icons_path +"terminal.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_Log.setIcon(icon9)
        self.button_Log.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.button_Log)

        self.button_Vis = QPushButton(self.w_Buttons)
        self.button_Vis.setObjectName(u"button_Vis")
        sizePolicy.setHeightForWidth(self.button_Vis.sizePolicy().hasHeightForWidth())
        self.button_Vis.setSizePolicy(sizePolicy)
        self.button_Vis.setMinimumSize(QSize(110, 40))
        self.button_Vis.setMaximumSize(QSize(16777215, 40))
        self.button_Vis.setFont(font1)
        self.button_Vis.setStyleSheet(u"QPushButton:checked {\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u""+ icons_path +"vect_field.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_Vis.setIcon(icon10)
        self.button_Vis.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.button_Vis)

        self.hs_buttons = QSpacerItem(10000, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.hs_buttons)


        self.oplay.addWidget(self.w_Buttons)

        self.scrollArea = QScrollArea(self.w_Operating_Tabs)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setStyleSheet(u" QScrollArea {\n"
"        border: 1pix solid gray;\n"
"    }\n"
"\n"
"QScrollBar:horizontal\n"
"    {\n"
"        height: 15px;\n"
"        margin: 3px 10px 3px 10px;\n"
"        border: 1px transparent #2A2929;\n"
"        border-radius: 4px;\n"
"        background-color:  rgba(200,200,200,50);    /* #2A2929; */\n"
"    }\n"
"\n"
"QScrollBar::handle:horizontal\n"
"    {\n"
"        background-color: rgba(180,180,180,180);      /* #605F5F; */\n"
"        min-width: 5px;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"QScrollBar:vertical\n"
"    {\n"
"        background-color: rgba(200,200,200,50);  ;\n"
"        width: 15px;\n"
"        margin: 10px 3px 10px 3px;\n"
"        border: 1px transparent #2A2929;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"QScrollBar::handle:vertical\n"
"    {\n"
"        background-color: rgba(180,180,180,180);         /* #605F5F; */\n"
"        min-height: 5px;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"QScrollBar::add-line {\n"
"        border: none;\n"
"      "
                        "  background: none;\n"
"    }\n"
"\n"
"QScrollBar::sub-line {\n"
"        border: none;\n"
"        background: none;\n"
"    }\n"
"")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 2655, 646))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(0, 0))
        self.flay = QHBoxLayout(self.scrollAreaWidgetContents)
        self.flay.setSpacing(5)
        self.flay.setObjectName(u"flay")
        self.flay.setContentsMargins(0, 0, 200, 0)
        self.f_ImportTab = QFrame(self.scrollAreaWidgetContents)
        self.f_ImportTab.setObjectName(u"f_ImportTab")
        self.f_ImportTab.setMinimumSize(QSize(480, 0))
        self.f_ImportTab.setMaximumSize(QSize(720, 16777215))
        self.f_ImportTab.setStyleSheet(u"QFrame#f_ImportTab{\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        self.horizontalLayout_5 = QHBoxLayout(self.f_ImportTab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.w_ImportTab = Import_Tab(self.f_ImportTab)
        self.w_ImportTab.setObjectName(u"w_ImportTab")

        self.horizontalLayout_5.addWidget(self.w_ImportTab)


        self.flay.addWidget(self.f_ImportTab)

        self.f_ExportTab = QFrame(self.scrollAreaWidgetContents)
        self.f_ExportTab.setObjectName(u"f_ExportTab")
        self.f_ExportTab.setMinimumSize(QSize(500, 0))
        self.f_ExportTab.setMaximumSize(QSize(750, 16777215))
        self.f_ExportTab.setSizeIncrement(QSize(0, 0))
        self.f_ExportTab.setStyleSheet(u"QFrame#f_ExportTab{\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        self.f_ExportTab.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.f_ExportTab)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.w_ExportTab = Export_Tab(self.f_ExportTab)
        self.w_ExportTab.setObjectName(u"w_ExportTab")
        self.w_ExportTab.setStyleSheet(u"")

        self.horizontalLayout_6.addWidget(self.w_ExportTab)


        self.flay.addWidget(self.f_ExportTab)

        self.f_ProcessTab = QFrame(self.scrollAreaWidgetContents)
        self.f_ProcessTab.setObjectName(u"f_ProcessTab")
        self.f_ProcessTab.setMinimumSize(QSize(480, 0))
        self.f_ProcessTab.setMaximumSize(QSize(720, 16777215))
        self.f_ProcessTab.setStyleSheet(u"QFrame#f_ProcessTab{\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        self.horizontalLayout_7 = QHBoxLayout(self.f_ProcessTab)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.w_ProcessTab = Process_Tab(self.f_ProcessTab)
        self.w_ProcessTab.setObjectName(u"w_ProcessTab")

        self.horizontalLayout_7.addWidget(self.w_ProcessTab)


        self.flay.addWidget(self.f_ProcessTab)

        self.f_LogTab = QFrame(self.scrollAreaWidgetContents)
        self.f_LogTab.setObjectName(u"f_LogTab")
        self.f_LogTab.setMinimumSize(QSize(480, 0))
        self.f_LogTab.setMaximumSize(QSize(720, 16777215))
        self.f_LogTab.setSizeIncrement(QSize(0, 0))
        self.f_LogTab.setStyleSheet(u"QFrame#f_LogTab{\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        self.f_LogTab.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.f_LogTab)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.w_LogTab = Log_Tab(self.f_LogTab)
        self.w_LogTab.setObjectName(u"w_LogTab")
        self.w_LogTab.setStyleSheet(u"")

        self.horizontalLayout_13.addWidget(self.w_LogTab)


        self.flay.addWidget(self.f_LogTab)

        self.f_VisTab = QFrame(self.scrollAreaWidgetContents)
        self.f_VisTab.setObjectName(u"f_VisTab")
        self.f_VisTab.setMinimumSize(QSize(480, 0))
        self.f_VisTab.setMaximumSize(QSize(720, 16777215))
        self.f_VisTab.setStyleSheet(u"QFrame#f_VisTab{\n"
"border: 1px solid gray;\n"
"border-radius: 15px;\n"
"}")
        self.f_VisTab.setFrameShape(QFrame.Box)
        self.lay_Vis = QVBoxLayout(self.f_VisTab)
        self.lay_Vis.setObjectName(u"lay_Vis")
        self.w_Mode = QWidget(self.f_VisTab)
        self.w_Mode.setObjectName(u"w_Mode")
        self.w_Mode.setMinimumSize(QSize(0, 40))
        self.w_Mode.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setPointSize(11)
        self.w_Mode.setFont(font2)
        self.horizontalLayout_8 = QHBoxLayout(self.w_Mode)
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 10)
        self.icon = QLabel(self.w_Mode)
        self.icon.setObjectName(u"icon")
        self.icon.setMinimumSize(QSize(35, 35))
        self.icon.setMaximumSize(QSize(35, 35))
        self.icon.setPixmap(QPixmap(u""+ icons_path +"vect_field.png"))
        self.icon.setScaledContents(True)

        self.horizontalLayout_8.addWidget(self.icon)

        self.name_tab = MyTabLabel(self.w_Mode)
        self.name_tab.setObjectName(u"name_tab")
        self.name_tab.setMinimumSize(QSize(200, 35))
        self.name_tab.setMaximumSize(QSize(16777215, 35))
        font3 = QFont()
        font3.setFamilies([u"Gadugi"])
        font3.setPointSize(20)
        font3.setBold(True)
        self.name_tab.setFont(font3)

        self.horizontalLayout_8.addWidget(self.name_tab)

        self.hs1 = QSpacerItem(70, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.hs1)


        self.lay_Vis.addWidget(self.w_Mode)

        self.line = QFrame(self.f_VisTab)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 5))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.lay_Vis.addWidget(self.line)

        self.w_plot = QWidget(self.f_VisTab)
        self.w_plot.setObjectName(u"w_plot")
        self.lay_w_Plot = QVBoxLayout(self.w_plot)
        self.lay_w_Plot.setSpacing(3)
        self.lay_w_Plot.setObjectName(u"lay_w_Plot")
        self.lay_w_Plot.setContentsMargins(0, 12, 0, 0)
        self.plot = MplCanvas(self.w_plot)
        self.plot.setObjectName(u"plot")

        self.lay_w_Plot.addWidget(self.plot)


        self.lay_Vis.addWidget(self.w_plot)


        self.flay.addWidget(self.f_VisTab)

        self.f_empty = QWidget(self.scrollAreaWidgetContents)
        self.f_empty.setObjectName(u"f_empty")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.f_empty.sizePolicy().hasHeightForWidth())
        self.f_empty.setSizePolicy(sizePolicy1)

        self.flay.addWidget(self.f_empty)

        self.flay.setStretch(0, 1)
        self.flay.setStretch(1, 1)
        self.flay.setStretch(2, 1)
        self.flay.setStretch(3, 1)
        self.flay.setStretch(4, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.oplay.addWidget(self.scrollArea)


        self.main_lay.addWidget(self.w_Operating_Tabs)

        gPairs.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(gPairs)
        self.statusbar.setObjectName(u"statusbar")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        font4.setItalic(True)
        self.statusbar.setFont(font4)
        self.statusbar.setStyleSheet(u"color: rgb(0, 0, 255);")
        gPairs.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(gPairs)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        self.menubar.setNativeMenuBar(False)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        gPairs.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.aExit)
        self.menuHelp.addAction(self.actionGuide)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(gPairs)

        QMetaObject.connectSlotsByName(gPairs)
    # setupUi

    def retranslateUi(self, gPairs):
        gPairs.setWindowTitle(QCoreApplication.translate("gPairs", u"PaIRS", None))
        self.actionExit.setText(QCoreApplication.translate("gPairs", u"Exit", None))
        self.aExit.setText(QCoreApplication.translate("gPairs", u"Exit", None))
        self.actionSave.setText(QCoreApplication.translate("gPairs", u"Save", None))
        self.actionLoad.setText(QCoreApplication.translate("gPairs", u"Load", None))
        self.actionNew.setText(QCoreApplication.translate("gPairs", u"New", None))
        self.actionAbout.setText(QCoreApplication.translate("gPairs", u"About PaIRS", None))
        self.actionGuide.setText(QCoreApplication.translate("gPairs", u"Guide", None))
        self.logo.setText("")
#if QT_CONFIG(tooltip)
        self.button_pause.setToolTip(QCoreApplication.translate("gPairs", u"Pause/restart process queue", None))
#endif // QT_CONFIG(tooltip)
        self.button_pause.setText("")
#if QT_CONFIG(tooltip)
        self.button_delete.setToolTip(QCoreApplication.translate("gPairs", u"Cancel process queue", None))
#endif // QT_CONFIG(tooltip)
        self.button_delete.setText("")
#if QT_CONFIG(tooltip)
        self.button_Run.setToolTip(QCoreApplication.translate("gPairs", u"Run and enjoy!", None))
#endif // QT_CONFIG(tooltip)
        self.button_Run.setText(QCoreApplication.translate("gPairs", u"Run", None))
        self.button_dock.setText("")
        self.button_Shape.setText("")
#if QT_CONFIG(tooltip)
        self.button_Input.setToolTip(QCoreApplication.translate("gPairs", u"Show/hide Input tab", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.button_Input.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.button_Input.setText(QCoreApplication.translate("gPairs", u"Input", None))
#if QT_CONFIG(tooltip)
        self.button_Output.setToolTip(QCoreApplication.translate("gPairs", u"Show/hide Output tab", None))
#endif // QT_CONFIG(tooltip)
        self.button_Output.setText(QCoreApplication.translate("gPairs", u"Output", None))
#if QT_CONFIG(tooltip)
        self.button_Process.setToolTip(QCoreApplication.translate("gPairs", u"Show/hide Process tab", None))
#endif // QT_CONFIG(tooltip)
        self.button_Process.setText(QCoreApplication.translate("gPairs", u"Process", None))
#if QT_CONFIG(tooltip)
        self.button_Log.setToolTip(QCoreApplication.translate("gPairs", u"Show/hide Log Tab", None))
#endif // QT_CONFIG(tooltip)
        self.button_Log.setText(QCoreApplication.translate("gPairs", u"Log", None))
#if QT_CONFIG(tooltip)
        self.button_Vis.setToolTip(QCoreApplication.translate("gPairs", u"Show/hide Visualization Tab", None))
#endif // QT_CONFIG(tooltip)
        self.button_Vis.setText(QCoreApplication.translate("gPairs", u"Vis", None))
        self.icon.setText("")
        self.name_tab.setText(QCoreApplication.translate("gPairs", u"Vis", None))
        self.menuFile.setTitle(QCoreApplication.translate("gPairs", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("gPairs", u"?", None))
    # retranslateUi

