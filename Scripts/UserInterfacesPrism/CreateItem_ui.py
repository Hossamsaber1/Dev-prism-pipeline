# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreateItem.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_CreateItem(object):
    def setupUi(self, dlg_CreateItem):
        if not dlg_CreateItem.objectName():
            dlg_CreateItem.setObjectName(u"dlg_CreateItem")
        dlg_CreateItem.resize(317, 182)
        self.verticalLayout = QVBoxLayout(dlg_CreateItem)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.w_type = QWidget(dlg_CreateItem)
        self.w_type.setObjectName(u"w_type")
        self.horizontalLayout_2 = QHBoxLayout(self.w_type)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.w_type)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.rb_asset = QRadioButton(self.w_type)
        self.rb_asset.setObjectName(u"rb_asset")
        self.rb_asset.setChecked(True)

        self.horizontalLayout_2.addWidget(self.rb_asset)

        self.rb_folder = QRadioButton(self.w_type)
        self.rb_folder.setObjectName(u"rb_folder")

        self.horizontalLayout_2.addWidget(self.rb_folder)


        self.verticalLayout.addWidget(self.w_type)

        self.w_item = QWidget(dlg_CreateItem)
        self.w_item.setObjectName(u"w_item")
        self.horizontalLayout = QHBoxLayout(self.w_item)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.l_item = QLabel(self.w_item)
        self.l_item.setObjectName(u"l_item")

        self.horizontalLayout.addWidget(self.l_item)

        self.e_item = QLineEdit(self.w_item)
        self.e_item.setObjectName(u"e_item")

        self.horizontalLayout.addWidget(self.e_item)

        self.b_showTasks = QPushButton(self.w_item)
        self.b_showTasks.setObjectName(u"b_showTasks")
        self.b_showTasks.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout.addWidget(self.b_showTasks)


        self.verticalLayout.addWidget(self.w_item)

        self.w_options = QWidget(dlg_CreateItem)
        self.w_options.setObjectName(u"w_options")
        self.horizontalLayout_3 = QHBoxLayout(self.w_options)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout.addWidget(self.w_options)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.buttonBox = QDialogButtonBox(dlg_CreateItem)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.e_item, self.b_showTasks)
        QWidget.setTabOrder(self.b_showTasks, self.buttonBox)
        QWidget.setTabOrder(self.buttonBox, self.rb_asset)
        QWidget.setTabOrder(self.rb_asset, self.rb_folder)

        self.retranslateUi(dlg_CreateItem)

        QMetaObject.connectSlotsByName(dlg_CreateItem)
    # setupUi

    def retranslateUi(self, dlg_CreateItem):
        dlg_CreateItem.setWindowTitle(QCoreApplication.translate("dlg_CreateItem", u"Create Category", None))
        self.label.setText(QCoreApplication.translate("dlg_CreateItem", u"Type:", None))
        self.rb_asset.setText(QCoreApplication.translate("dlg_CreateItem", u"Asset", None))
        self.rb_folder.setText(QCoreApplication.translate("dlg_CreateItem", u"Folder", None))
        self.l_item.setText(QCoreApplication.translate("dlg_CreateItem", u"Category Name:", None))
#if QT_CONFIG(tooltip)
        self.b_showTasks.setToolTip(QCoreApplication.translate("dlg_CreateItem", u"existing tasks", None))
#endif // QT_CONFIG(tooltip)
        self.b_showTasks.setText(QCoreApplication.translate("dlg_CreateItem", u"\u25bc", None))
    # retranslateUi

