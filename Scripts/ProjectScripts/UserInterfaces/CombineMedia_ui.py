# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CombineMedia.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_CombineMedia(object):
    def setupUi(self, dlg_CombineMedia):
        if not dlg_CombineMedia.objectName():
            dlg_CombineMedia.setObjectName(u"dlg_CombineMedia")
        dlg_CombineMedia.resize(653, 117)
        self.verticalLayout = QVBoxLayout(dlg_CombineMedia)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(dlg_CombineMedia)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.b_tasks = QPushButton(self.widget)
        self.b_tasks.setObjectName(u"b_tasks")

        self.gridLayout.addWidget(self.b_tasks, 1, 3, 1, 1)

        self.e_output = QLineEdit(self.widget)
        self.e_output.setObjectName(u"e_output")

        self.gridLayout.addWidget(self.e_output, 0, 2, 1, 1)

        self.b_browse = QPushButton(self.widget)
        self.b_browse.setObjectName(u"b_browse")

        self.gridLayout.addWidget(self.b_browse, 0, 3, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.e_task = QLineEdit(self.widget)
        self.e_task.setObjectName(u"e_task")

        self.gridLayout.addWidget(self.e_task, 1, 2, 1, 1)

        self.l_task = QLabel(self.widget)
        self.l_task.setObjectName(u"l_task")

        self.gridLayout.addWidget(self.l_task, 1, 0, 1, 1)

        self.chb_task = QCheckBox(self.widget)
        self.chb_task.setObjectName(u"chb_task")
        self.chb_task.setChecked(True)

        self.gridLayout.addWidget(self.chb_task, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.bb_combine = QDialogButtonBox(dlg_CombineMedia)
        self.bb_combine.setObjectName(u"bb_combine")
        self.bb_combine.setOrientation(Qt.Horizontal)
        self.bb_combine.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.bb_combine)


        self.retranslateUi(dlg_CombineMedia)
        self.bb_combine.accepted.connect(dlg_CombineMedia.accept)
        self.bb_combine.rejected.connect(dlg_CombineMedia.reject)

        QMetaObject.connectSlotsByName(dlg_CombineMedia)
    # setupUi

    def retranslateUi(self, dlg_CombineMedia):
        dlg_CombineMedia.setWindowTitle(QCoreApplication.translate("dlg_CombineMedia", u"Combine media", None))
        self.b_tasks.setText(QCoreApplication.translate("dlg_CombineMedia", u"\u25bc", None))
        self.b_browse.setText(QCoreApplication.translate("dlg_CombineMedia", u"...", None))
        self.label.setText(QCoreApplication.translate("dlg_CombineMedia", u"Outputfile:", None))
        self.l_task.setText(QCoreApplication.translate("dlg_CombineMedia", u"Create external task:", None))
        self.chb_task.setText("")
    # retranslateUi

