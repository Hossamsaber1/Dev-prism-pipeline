# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SaveComment.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_SaveComment(object):
    def setupUi(self, dlg_SaveComment):
        if not dlg_SaveComment.objectName():
            dlg_SaveComment.setObjectName(u"dlg_SaveComment")
        dlg_SaveComment.resize(599, 611)
        self.verticalLayout = QVBoxLayout(dlg_SaveComment)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.w_details = QWidget(dlg_SaveComment)
        self.w_details.setObjectName(u"w_details")
        self.gridLayout = QGridLayout(self.w_details)
        self.gridLayout.setObjectName(u"gridLayout")
        self.l_preview = QLabel(self.w_details)
        self.l_preview.setObjectName(u"l_preview")
        self.l_preview.setMinimumSize(QSize(500, 281))
        self.l_preview.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.l_preview, 4, 1, 1, 1)

        self.label = QLabel(self.w_details)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.l_comment = QLabel(self.w_details)
        self.l_comment.setObjectName(u"l_comment")

        self.gridLayout.addWidget(self.l_comment, 0, 0, 1, 1)

        self.e_comment = QLineEdit(self.w_details)
        self.e_comment.setObjectName(u"e_comment")

        self.gridLayout.addWidget(self.e_comment, 0, 1, 1, 1)

        self.label_2 = QLabel(self.w_details)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.e_description = QTextEdit(self.w_details)
        self.e_description.setObjectName(u"e_description")

        self.gridLayout.addWidget(self.e_description, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.w_details)

        self.b_changePreview = QPushButton(dlg_SaveComment)
        self.b_changePreview.setObjectName(u"b_changePreview")

        self.verticalLayout.addWidget(self.b_changePreview)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(dlg_SaveComment)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.e_comment, self.e_description)

        self.retranslateUi(dlg_SaveComment)

        QMetaObject.connectSlotsByName(dlg_SaveComment)
    # setupUi

    def retranslateUi(self, dlg_SaveComment):
        dlg_SaveComment.setWindowTitle(QCoreApplication.translate("dlg_SaveComment", u"Save Extended", None))
        self.l_preview.setText(QCoreApplication.translate("dlg_SaveComment", u"Preview", None))
        self.label.setText(QCoreApplication.translate("dlg_SaveComment", u"Preview:", None))
        self.l_comment.setText(QCoreApplication.translate("dlg_SaveComment", u"Comment:", None))
        self.label_2.setText(QCoreApplication.translate("dlg_SaveComment", u"Description:", None))
        self.b_changePreview.setText(QCoreApplication.translate("dlg_SaveComment", u"Change preview", None))
    # retranslateUi

