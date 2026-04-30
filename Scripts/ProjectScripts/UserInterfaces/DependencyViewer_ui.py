# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DependencyViewer.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_DependencyViewer(object):
    def setupUi(self, dlg_DependencyViewer):
        if not dlg_DependencyViewer.objectName():
            dlg_DependencyViewer.setObjectName(u"dlg_DependencyViewer")
        dlg_DependencyViewer.resize(1555, 412)
        self.verticalLayout = QVBoxLayout(dlg_DependencyViewer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(dlg_DependencyViewer)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)


        self.horizontalLayout_2.addWidget(self.widget_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.e_search = QLineEdit(self.widget)
        self.e_search.setObjectName(u"e_search")

        self.horizontalLayout.addWidget(self.e_search)


        self.horizontalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.widget_2)

        self.l_root = QLabel(dlg_DependencyViewer)
        self.l_root.setObjectName(u"l_root")
        font = QFont()
        font.setBold(True)
        self.l_root.setFont(font)

        self.verticalLayout.addWidget(self.l_root)

        self.tw_dependencies = QTreeWidget(dlg_DependencyViewer)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_dependencies.setHeaderItem(__qtreewidgetitem)
        self.tw_dependencies.setObjectName(u"tw_dependencies")
        self.tw_dependencies.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_dependencies.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_dependencies.header().setVisible(True)

        self.verticalLayout.addWidget(self.tw_dependencies)


        self.retranslateUi(dlg_DependencyViewer)

        QMetaObject.connectSlotsByName(dlg_DependencyViewer)
    # setupUi

    def retranslateUi(self, dlg_DependencyViewer):
        dlg_DependencyViewer.setWindowTitle(QCoreApplication.translate("dlg_DependencyViewer", u"Dependency Viewer", None))
        self.label.setText(QCoreApplication.translate("dlg_DependencyViewer", u"The asets in the list were used to create:", None))
        self.label_2.setText(QCoreApplication.translate("dlg_DependencyViewer", u"Search:", None))
        self.l_root.setText("")
    # retranslateUi

