from .addwidgets_ps import icons_path
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Tree_Tab.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QScrollArea, QSizePolicy, QSpacerItem,
    QToolButton, QTreeWidgetItem, QVBoxLayout, QWidget)

from .addwidgets_ps import myQTreeWidget

class Ui_TreeTab(object):
    def setupUi(self, TreeTab):
        if not TreeTab.objectName():
            TreeTab.setObjectName(u"TreeTab")
        TreeTab.resize(500, 680)
        TreeTab.setMinimumSize(QSize(260, 340))
        TreeTab.setMaximumSize(QSize(1000, 16777215))
        font = QFont()
        font.setPointSize(11)
        TreeTab.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u""+ icons_path +"checklist.png", QSize(), QIcon.Normal, QIcon.Off)
        TreeTab.setWindowIcon(icon1)
        self.verticalLayout_7 = QVBoxLayout(TreeTab)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.w_Mode = QWidget(TreeTab)
        self.w_Mode.setObjectName(u"w_Mode")
        self.w_Mode.setMinimumSize(QSize(0, 40))
        self.w_Mode.setMaximumSize(QSize(16777215, 40))
        self.w_Mode.setFont(font)
        self.horizontalLayout_5 = QHBoxLayout(self.w_Mode)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 10)
        self.icon = QLabel(self.w_Mode)
        self.icon.setObjectName(u"icon")
        self.icon.setMinimumSize(QSize(35, 35))
        self.icon.setMaximumSize(QSize(35, 35))
        self.icon.setPixmap(QPixmap(u""+ icons_path +"checklist.png"))
        self.icon.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.icon)

        self.name_tab = QLabel(self.w_Mode)
        self.name_tab.setObjectName(u"name_tab")
        self.name_tab.setMinimumSize(QSize(200, 35))
        self.name_tab.setMaximumSize(QSize(16777215, 35))
        font1 = QFont()
        font1.setFamilies([u"Gadugi"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.name_tab.setFont(font1)

        self.horizontalLayout_5.addWidget(self.name_tab)

        self.hs1 = QSpacerItem(70, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.hs1)

        self.button_restore = QToolButton(self.w_Mode)
        self.button_restore.setObjectName(u"button_restore")
        self.button_restore.setMinimumSize(QSize(30, 30))
        self.button_restore.setMaximumSize(QSize(30, 30))
        icon2 = QIcon()
        icon2.addFile(u""+ icons_path +"restore.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_restore.setIcon(icon2)
        self.button_restore.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.button_restore)

        self.button_delete = QToolButton(self.w_Mode)
        self.button_delete.setObjectName(u"button_delete")
        self.button_delete.setMinimumSize(QSize(30, 30))
        self.button_delete.setMaximumSize(QSize(30, 30))
        icon3 = QIcon()
        icon3.addFile(u""+ icons_path +"delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_delete.setIcon(icon3)
        self.button_delete.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.button_delete)


        self.verticalLayout_7.addWidget(self.w_Mode)

        self.line = QFrame(TreeTab)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 5))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.scrollArea = QScrollArea(TreeTab)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 480, 607))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setSpacing(10)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 5, 10, 0)
        self.w_Tree_past = QWidget(self.scrollAreaWidgetContents)
        self.w_Tree_past.setObjectName(u"w_Tree_past")
        self.verticalLayout = QVBoxLayout(self.w_Tree_past)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 20)
        self.label_Tree_past = QLabel(self.w_Tree_past)
        self.label_Tree_past.setObjectName(u"label_Tree_past")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_Tree_past.sizePolicy().hasHeightForWidth())
        self.label_Tree_past.setSizePolicy(sizePolicy1)
        self.label_Tree_past.setMinimumSize(QSize(0, 20))
        self.label_Tree_past.setMaximumSize(QSize(16777215, 20))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(True)
        self.label_Tree_past.setFont(font2)
        self.label_Tree_past.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_Tree_past)

        self.tree_past = myQTreeWidget(self.w_Tree_past)
        QTreeWidgetItem(self.tree_past)
        self.tree_past.setObjectName(u"tree_past")
        self.tree_past.setColumnCount(1)
        self.tree_past.header().setVisible(False)
        self.tree_past.header().setCascadingSectionResizes(False)
        self.tree_past.header().setMinimumSectionSize(15)
        self.tree_past.header().setHighlightSections(False)
        self.tree_past.header().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tree_past)


        self.verticalLayout_8.addWidget(self.w_Tree_past)

        self.w_Tree_current = QWidget(self.scrollAreaWidgetContents)
        self.w_Tree_current.setObjectName(u"w_Tree_current")
        self.verticalLayout_2 = QVBoxLayout(self.w_Tree_current)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_Tree_current = QLabel(self.w_Tree_current)
        self.label_Tree_current.setObjectName(u"label_Tree_current")
        sizePolicy1.setHeightForWidth(self.label_Tree_current.sizePolicy().hasHeightForWidth())
        self.label_Tree_current.setSizePolicy(sizePolicy1)
        self.label_Tree_current.setMinimumSize(QSize(0, 20))
        self.label_Tree_current.setMaximumSize(QSize(16777215, 20))
        self.label_Tree_current.setFont(font2)
        self.label_Tree_current.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label_Tree_current)

        self.tree_current = myQTreeWidget(self.w_Tree_current)
        QTreeWidgetItem(self.tree_current)
        self.tree_current.setObjectName(u"tree_current")
        self.tree_current.setMinimumSize(QSize(0, 22))
        self.tree_current.setMaximumSize(QSize(16777215, 22))
        self.tree_current.setColumnCount(1)
        self.tree_current.header().setVisible(False)
        self.tree_current.header().setCascadingSectionResizes(False)
        self.tree_current.header().setMinimumSectionSize(15)
        self.tree_current.header().setHighlightSections(False)
        self.tree_current.header().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.tree_current)


        self.verticalLayout_8.addWidget(self.w_Tree_current)

        self.w_Tree_future = QWidget(self.scrollAreaWidgetContents)
        self.w_Tree_future.setObjectName(u"w_Tree_future")
        self.verticalLayout_3 = QVBoxLayout(self.w_Tree_future)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_Tree_future = QLabel(self.w_Tree_future)
        self.label_Tree_future.setObjectName(u"label_Tree_future")
        sizePolicy1.setHeightForWidth(self.label_Tree_future.sizePolicy().hasHeightForWidth())
        self.label_Tree_future.setSizePolicy(sizePolicy1)
        self.label_Tree_future.setMinimumSize(QSize(0, 20))
        self.label_Tree_future.setMaximumSize(QSize(16777215, 20))
        self.label_Tree_future.setFont(font2)
        self.label_Tree_future.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.label_Tree_future)

        self.tree_future = myQTreeWidget(self.w_Tree_future)
        QTreeWidgetItem(self.tree_future)
        QTreeWidgetItem(self.tree_future)
        self.tree_future.setObjectName(u"tree_future")
        self.tree_future.setColumnCount(1)
        self.tree_future.header().setVisible(False)
        self.tree_future.header().setCascadingSectionResizes(False)
        self.tree_future.header().setMinimumSectionSize(15)
        self.tree_future.header().setHighlightSections(False)
        self.tree_future.header().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.tree_future)


        self.verticalLayout_8.addWidget(self.w_Tree_future)

        self.w_proc_Buttons = QWidget(self.scrollAreaWidgetContents)
        self.w_proc_Buttons.setObjectName(u"w_proc_Buttons")
        self.horizontalLayout = QHBoxLayout(self.w_proc_Buttons)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.button_min = QToolButton(self.w_proc_Buttons)
        self.button_min.setObjectName(u"button_min")
        self.button_min.setMinimumSize(QSize(120, 24))
        self.button_min.setMaximumSize(QSize(120, 24))
        self.button_min.setFont(font)
        self.button_min.setCheckable(False)

        self.horizontalLayout.addWidget(self.button_min)

        self.button_PIV = QToolButton(self.w_proc_Buttons)
        self.button_PIV.setObjectName(u"button_PIV")
        self.button_PIV.setMinimumSize(QSize(120, 24))
        self.button_PIV.setMaximumSize(QSize(120, 24))
        self.button_PIV.setFont(font)
        self.button_PIV.setCheckable(False)

        self.horizontalLayout.addWidget(self.button_PIV)

        self.hs_proc_Buttons = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.hs_proc_Buttons)


        self.verticalLayout_8.addWidget(self.w_proc_Buttons)

        self.verticalSpacer = QSpacerItem(5, 15, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.verticalLayout_8.setStretch(0, 1)
        self.verticalLayout_8.setStretch(2, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_7.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.scrollArea, self.button_restore)
        QWidget.setTabOrder(self.button_restore, self.button_delete)
        QWidget.setTabOrder(self.button_delete, self.tree_past)
        QWidget.setTabOrder(self.tree_past, self.tree_current)
        QWidget.setTabOrder(self.tree_current, self.tree_future)

        self.retranslateUi(TreeTab)

        QMetaObject.connectSlotsByName(TreeTab)
    # setupUi

    def retranslateUi(self, TreeTab):
        TreeTab.setWindowTitle(QCoreApplication.translate("TreeTab", u"Tree", None))
#if QT_CONFIG(accessibility)
        TreeTab.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.icon.setText("")
        self.name_tab.setText(QCoreApplication.translate("TreeTab", u"Queue", None))
#if QT_CONFIG(tooltip)
        self.button_restore.setToolTip(QCoreApplication.translate("TreeTab", u"Restore process", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.button_delete.setToolTip(QCoreApplication.translate("TreeTab", u"Delete process", None))
#endif // QT_CONFIG(tooltip)
        self.label_Tree_past.setText(QCoreApplication.translate("TreeTab", u"Past", None))
        ___qtreewidgetitem = self.tree_past.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("TreeTab", u"Name", None));

        __sortingEnabled = self.tree_past.isSortingEnabled()
        self.tree_past.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.tree_past.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("TreeTab", u"first", None));
        self.tree_past.setSortingEnabled(__sortingEnabled)

        self.label_Tree_current.setText(QCoreApplication.translate("TreeTab", u"Current", None))
        ___qtreewidgetitem2 = self.tree_current.headerItem()
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("TreeTab", u"Name", None));

        __sortingEnabled1 = self.tree_current.isSortingEnabled()
        self.tree_current.setSortingEnabled(False)
        ___qtreewidgetitem3 = self.tree_current.topLevelItem(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("TreeTab", u"current", None));
        self.tree_current.setSortingEnabled(__sortingEnabled1)

        self.label_Tree_future.setText(QCoreApplication.translate("TreeTab", u"Future", None))
        ___qtreewidgetitem4 = self.tree_future.headerItem()
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("TreeTab", u"Name", None));

        __sortingEnabled2 = self.tree_future.isSortingEnabled()
        self.tree_future.setSortingEnabled(False)
        ___qtreewidgetitem5 = self.tree_future.topLevelItem(0)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("TreeTab", u"next #1", None));
        ___qtreewidgetitem6 = self.tree_future.topLevelItem(1)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("TreeTab", u"next #2", None));
        self.tree_future.setSortingEnabled(__sortingEnabled2)

#if QT_CONFIG(tooltip)
        self.button_min.setToolTip(QCoreApplication.translate("TreeTab", u"Add ensemble minimum computation to queue", None))
#endif // QT_CONFIG(tooltip)
        self.button_min.setText(QCoreApplication.translate("TreeTab", u"Calc. Min.", None))
#if QT_CONFIG(tooltip)
        self.button_PIV.setToolTip(QCoreApplication.translate("TreeTab", u"Add PIV process to queue", None))
#endif // QT_CONFIG(tooltip)
        self.button_PIV.setText(QCoreApplication.translate("TreeTab", u"PIV proc.", None))
    # retranslateUi

