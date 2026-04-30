# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EditShot.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_EditShot(object):
    def setupUi(self, dlg_EditShot):
        if not dlg_EditShot.objectName():
            dlg_EditShot.setObjectName(u"dlg_EditShot")
        dlg_EditShot.resize(436, 417)
        self.verticalLayout = QVBoxLayout(dlg_EditShot)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.w_shotName = QWidget(dlg_EditShot)
        self.w_shotName.setObjectName(u"w_shotName")
        self.gridLayout = QGridLayout(self.w_shotName)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 10, -1, -1)
        self.l_shotIcon = QLabel(self.w_shotName)
        self.l_shotIcon.setObjectName(u"l_shotIcon")

        self.gridLayout.addWidget(self.l_shotIcon, 2, 0, 1, 1)

        self.l_shot = QLabel(self.w_shotName)
        self.l_shot.setObjectName(u"l_shot")

        self.gridLayout.addWidget(self.l_shot, 2, 1, 1, 1)

        self.e_episode = QLineEdit(self.w_shotName)
        self.e_episode.setObjectName(u"e_episode")

        self.gridLayout.addWidget(self.e_episode, 0, 2, 1, 1)

        self.l_seqIcon = QLabel(self.w_shotName)
        self.l_seqIcon.setObjectName(u"l_seqIcon")

        self.gridLayout.addWidget(self.l_seqIcon, 1, 0, 1, 1)

        self.l_seq = QLabel(self.w_shotName)
        self.l_seq.setObjectName(u"l_seq")

        self.gridLayout.addWidget(self.l_seq, 1, 1, 1, 1)

        self.l_episodeIcon = QLabel(self.w_shotName)
        self.l_episodeIcon.setObjectName(u"l_episodeIcon")

        self.gridLayout.addWidget(self.l_episodeIcon, 0, 0, 1, 1)

        self.b_showSeq = QToolButton(self.w_shotName)
        self.b_showSeq.setObjectName(u"b_showSeq")
        self.b_showSeq.setMaximumSize(QSize(25, 16777215))
        self.b_showSeq.setFocusPolicy(Qt.NoFocus)
        self.b_showSeq.setArrowType(Qt.DownArrow)

        self.gridLayout.addWidget(self.b_showSeq, 1, 3, 1, 1)

        self.l_episode = QLabel(self.w_shotName)
        self.l_episode.setObjectName(u"l_episode")

        self.gridLayout.addWidget(self.l_episode, 0, 1, 1, 1)

        self.b_showEpisodes = QToolButton(self.w_shotName)
        self.b_showEpisodes.setObjectName(u"b_showEpisodes")
        self.b_showEpisodes.setMaximumSize(QSize(25, 16777215))
        self.b_showEpisodes.setFocusPolicy(Qt.NoFocus)
        self.b_showEpisodes.setArrowType(Qt.DownArrow)

        self.gridLayout.addWidget(self.b_showEpisodes, 0, 3, 1, 1)

        self.e_shotName = QLineEdit(self.w_shotName)
        self.e_shotName.setObjectName(u"e_shotName")

        self.gridLayout.addWidget(self.e_shotName, 2, 2, 1, 1)

        self.e_sequence = QLineEdit(self.w_shotName)
        self.e_sequence.setObjectName(u"e_sequence")

        self.gridLayout.addWidget(self.e_sequence, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.w_shotName)

        self.w_range = QWidget(dlg_EditShot)
        self.w_range.setObjectName(u"w_range")
        self.horizontalLayout = QHBoxLayout(self.w_range)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 1, -1, -1)
        self.label_2 = QLabel(self.w_range)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(self.w_range)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.sp_startFrame = QSpinBox(self.w_range)
        self.sp_startFrame.setObjectName(u"sp_startFrame")
        self.sp_startFrame.setMinimumSize(QSize(60, 0))
        self.sp_startFrame.setMaximum(99999)
        self.sp_startFrame.setValue(1001)

        self.horizontalLayout.addWidget(self.sp_startFrame)

        self.label_3 = QLabel(self.w_range)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_3)

        self.sp_endFrame = QSpinBox(self.w_range)
        self.sp_endFrame.setObjectName(u"sp_endFrame")
        self.sp_endFrame.setMinimumSize(QSize(60, 0))
        self.sp_endFrame.setMaximum(99999)
        self.sp_endFrame.setValue(1100)

        self.horizontalLayout.addWidget(self.sp_endFrame)


        self.verticalLayout.addWidget(self.w_range)

        self.w_preview = QWidget(dlg_EditShot)
        self.w_preview.setObjectName(u"w_preview")
        self.horizontalLayout_2 = QHBoxLayout(self.w_preview)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 1, -1, -1)
        self.label_5 = QLabel(self.w_preview)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.l_shotPreview = QLabel(self.w_preview)
        self.l_shotPreview.setObjectName(u"l_shotPreview")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_shotPreview.sizePolicy().hasHeightForWidth())
        self.l_shotPreview.setSizePolicy(sizePolicy)
        self.l_shotPreview.setMinimumSize(QSize(300, 169))
        self.l_shotPreview.setContextMenuPolicy(Qt.CustomContextMenu)

        self.horizontalLayout_2.addWidget(self.l_shotPreview)


        self.verticalLayout.addWidget(self.w_preview)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.w_buttons = QWidget(dlg_EditShot)
        self.w_buttons.setObjectName(u"w_buttons")
        self.horizontalLayout_4 = QHBoxLayout(self.w_buttons)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.b_deleteShot = QPushButton(self.w_buttons)
        self.b_deleteShot.setObjectName(u"b_deleteShot")
        self.b_deleteShot.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_4.addWidget(self.b_deleteShot)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.buttonBox = QDialogButtonBox(self.w_buttons)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.NoButton)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout.addWidget(self.w_buttons)

        QWidget.setTabOrder(self.e_episode, self.e_sequence)
        QWidget.setTabOrder(self.e_sequence, self.e_shotName)
        QWidget.setTabOrder(self.e_shotName, self.sp_startFrame)
        QWidget.setTabOrder(self.sp_startFrame, self.sp_endFrame)

        self.retranslateUi(dlg_EditShot)

        QMetaObject.connectSlotsByName(dlg_EditShot)
    # setupUi

    def retranslateUi(self, dlg_EditShot):
        dlg_EditShot.setWindowTitle(QCoreApplication.translate("dlg_EditShot", u"Edit shot", None))
        self.l_shotIcon.setText("")
        self.l_shot.setText(QCoreApplication.translate("dlg_EditShot", u"Shot:", None))
        self.e_episode.setPlaceholderText(QCoreApplication.translate("dlg_EditShot", u"ep01", None))
        self.l_seqIcon.setText("")
        self.l_seq.setText(QCoreApplication.translate("dlg_EditShot", u"Sequence:", None))
        self.l_episodeIcon.setText("")
#if QT_CONFIG(tooltip)
        self.b_showSeq.setToolTip(QCoreApplication.translate("dlg_EditShot", u"Existing sequence names", None))
#endif // QT_CONFIG(tooltip)
        self.b_showSeq.setText("")
        self.l_episode.setText(QCoreApplication.translate("dlg_EditShot", u"Episode:", None))
#if QT_CONFIG(tooltip)
        self.b_showEpisodes.setToolTip(QCoreApplication.translate("dlg_EditShot", u"Existing episode names", None))
#endif // QT_CONFIG(tooltip)
        self.b_showEpisodes.setText("")
        self.e_shotName.setPlaceholderText(QCoreApplication.translate("dlg_EditShot", u"sh010", None))
        self.e_sequence.setPlaceholderText(QCoreApplication.translate("dlg_EditShot", u"sq010", None))
        self.label_2.setText(QCoreApplication.translate("dlg_EditShot", u"Framerange:", None))
        self.label.setText(QCoreApplication.translate("dlg_EditShot", u"start:", None))
        self.label_3.setText(QCoreApplication.translate("dlg_EditShot", u"end:", None))
        self.label_5.setText(QCoreApplication.translate("dlg_EditShot", u"Thumbnail:", None))
        self.l_shotPreview.setText(QCoreApplication.translate("dlg_EditShot", u"Preview image", None))
        self.b_deleteShot.setText(QCoreApplication.translate("dlg_EditShot", u"Delete shot", None))
    # retranslateUi

