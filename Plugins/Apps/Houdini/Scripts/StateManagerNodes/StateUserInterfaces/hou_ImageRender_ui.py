# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hou_ImageRender.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_ImageRender(object):
    def setupUi(self, wg_ImageRender):
        if not wg_ImageRender.objectName():
            wg_ImageRender.setObjectName(u"wg_ImageRender")
        wg_ImageRender.resize(389, 1521)
        self.verticalLayout = QVBoxLayout(wg_ImageRender)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(wg_ImageRender)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, 18, 0)
        self.l_name = QLabel(self.widget_4)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout_4.addWidget(self.l_name)

        self.e_name = QLineEdit(self.widget_4)
        self.e_name.setObjectName(u"e_name")

        self.horizontalLayout_4.addWidget(self.e_name)

        self.l_class = QLabel(self.widget_4)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        self.l_class.setFont(font)

        self.horizontalLayout_4.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.widget_4)

        self.gb_imageRender = QGroupBox(wg_ImageRender)
        self.gb_imageRender.setObjectName(u"gb_imageRender")
        self.verticalLayout_2 = QVBoxLayout(self.gb_imageRender)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.w_comment = QWidget(self.gb_imageRender)
        self.w_comment.setObjectName(u"w_comment")
        self.horizontalLayout_40 = QHBoxLayout(self.w_comment)
        self.horizontalLayout_40.setSpacing(0)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalLayout_40.setContentsMargins(9, 0, 9, 0)
        self.l_comment = QLabel(self.w_comment)
        self.l_comment.setObjectName(u"l_comment")
        self.l_comment.setMinimumSize(QSize(40, 0))
        self.l_comment.setMaximumSize(QSize(95, 16777215))

        self.horizontalLayout_40.addWidget(self.l_comment)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_40.addItem(self.horizontalSpacer_10)

        self.e_comment = QLineEdit(self.w_comment)
        self.e_comment.setObjectName(u"e_comment")

        self.horizontalLayout_40.addWidget(self.e_comment)


        self.verticalLayout_2.addWidget(self.w_comment)

        self.w_context = QWidget(self.gb_imageRender)
        self.w_context.setObjectName(u"w_context")
        self.horizontalLayout_19 = QHBoxLayout(self.w_context)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(9, 0, 9, 0)
        self.label_9 = QLabel(self.w_context)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_19.addWidget(self.label_9)

        self.horizontalSpacer_5 = QSpacerItem(37, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_5)

        self.l_context = QLabel(self.w_context)
        self.l_context.setObjectName(u"l_context")

        self.horizontalLayout_19.addWidget(self.l_context)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_8)

        self.b_context = QPushButton(self.w_context)
        self.b_context.setObjectName(u"b_context")

        self.horizontalLayout_19.addWidget(self.b_context)

        self.cb_context = QComboBox(self.w_context)
        self.cb_context.setObjectName(u"cb_context")

        self.horizontalLayout_19.addWidget(self.cb_context)


        self.verticalLayout_2.addWidget(self.w_context)

        self.widget_10 = QWidget(self.gb_imageRender)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, 0)
        self.label_2 = QLabel(self.widget_10)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_10.addWidget(self.label_2)

        self.l_taskName = QLabel(self.widget_10)
        self.l_taskName.setObjectName(u"l_taskName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_taskName.sizePolicy().hasHeightForWidth())
        self.l_taskName.setSizePolicy(sizePolicy)
        self.l_taskName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.l_taskName)

        self.b_changeTask = QPushButton(self.widget_10)
        self.b_changeTask.setObjectName(u"b_changeTask")
        self.b_changeTask.setEnabled(True)
        self.b_changeTask.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_10.addWidget(self.b_changeTask)


        self.verticalLayout_2.addWidget(self.widget_10)

        self.widget_2 = QWidget(self.gb_imageRender)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.cb_rangeType = QComboBox(self.widget_2)
        self.cb_rangeType.setObjectName(u"cb_rangeType")
        self.cb_rangeType.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.cb_rangeType)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.w_frameRangeValues = QWidget(self.gb_imageRender)
        self.w_frameRangeValues.setObjectName(u"w_frameRangeValues")
        self.gridLayout = QGridLayout(self.w_frameRangeValues)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, 0)
        self.l_rangeEnd = QLabel(self.w_frameRangeValues)
        self.l_rangeEnd.setObjectName(u"l_rangeEnd")
        self.l_rangeEnd.setMinimumSize(QSize(30, 0))
        self.l_rangeEnd.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.l_rangeEnd, 1, 5, 1, 1)

        self.sp_rangeEnd = QSpinBox(self.w_frameRangeValues)
        self.sp_rangeEnd.setObjectName(u"sp_rangeEnd")
        self.sp_rangeEnd.setMaximum(99999)
        self.sp_rangeEnd.setValue(1100)

        self.gridLayout.addWidget(self.sp_rangeEnd, 1, 6, 1, 1)

        self.sp_rangeStart = QSpinBox(self.w_frameRangeValues)
        self.sp_rangeStart.setObjectName(u"sp_rangeStart")
        self.sp_rangeStart.setMaximum(99999)
        self.sp_rangeStart.setValue(1001)

        self.gridLayout.addWidget(self.sp_rangeStart, 0, 6, 1, 1)

        self.l_rangeStart = QLabel(self.w_frameRangeValues)
        self.l_rangeStart.setObjectName(u"l_rangeStart")
        self.l_rangeStart.setMinimumSize(QSize(30, 0))
        self.l_rangeStart.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.l_rangeStart, 0, 5, 1, 1)

        self.l_rangeStartInfo = QLabel(self.w_frameRangeValues)
        self.l_rangeStartInfo.setObjectName(u"l_rangeStartInfo")

        self.gridLayout.addWidget(self.l_rangeStartInfo, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 0, 4, 1, 1)

        self.l_rangeEndInfo = QLabel(self.w_frameRangeValues)
        self.l_rangeEndInfo.setObjectName(u"l_rangeEndInfo")

        self.gridLayout.addWidget(self.l_rangeEndInfo, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.w_frameRangeValues)

        self.w_frameExpression = QWidget(self.gb_imageRender)
        self.w_frameExpression.setObjectName(u"w_frameExpression")
        self.horizontalLayout_17 = QHBoxLayout(self.w_frameExpression)
        self.horizontalLayout_17.setSpacing(6)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(9, 0, 9, 0)
        self.l_frameExpression = QLabel(self.w_frameExpression)
        self.l_frameExpression.setObjectName(u"l_frameExpression")

        self.horizontalLayout_17.addWidget(self.l_frameExpression)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_23)

        self.le_frameExpression = QLineEdit(self.w_frameExpression)
        self.le_frameExpression.setObjectName(u"le_frameExpression")
        self.le_frameExpression.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_17.addWidget(self.le_frameExpression)


        self.verticalLayout_2.addWidget(self.w_frameExpression)

        self.w_camera = QWidget(self.gb_imageRender)
        self.w_camera.setObjectName(u"w_camera")
        self.horizontalLayout_2 = QHBoxLayout(self.w_camera)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.label = QLabel(self.w_camera)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.chb_camOverride = QCheckBox(self.w_camera)
        self.chb_camOverride.setObjectName(u"chb_camOverride")

        self.horizontalLayout_2.addWidget(self.chb_camOverride)

        self.cb_cams = QComboBox(self.w_camera)
        self.cb_cams.setObjectName(u"cb_cams")
        self.cb_cams.setEnabled(False)
        self.cb_cams.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.cb_cams)


        self.verticalLayout_2.addWidget(self.w_camera)

        self.w_resolution = QWidget(self.gb_imageRender)
        self.w_resolution.setObjectName(u"w_resolution")
        self.horizontalLayout_9 = QHBoxLayout(self.w_resolution)
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(9, 0, 9, 0)
        self.label_6 = QLabel(self.w_resolution)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_9.addWidget(self.label_6)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_13)

        self.chb_resOverride = QCheckBox(self.w_resolution)
        self.chb_resOverride.setObjectName(u"chb_resOverride")

        self.horizontalLayout_9.addWidget(self.chb_resOverride)

        self.sp_resWidth = QSpinBox(self.w_resolution)
        self.sp_resWidth.setObjectName(u"sp_resWidth")
        self.sp_resWidth.setEnabled(False)
        self.sp_resWidth.setMinimum(1)
        self.sp_resWidth.setMaximum(99999)
        self.sp_resWidth.setValue(1280)

        self.horizontalLayout_9.addWidget(self.sp_resWidth)

        self.sp_resHeight = QSpinBox(self.w_resolution)
        self.sp_resHeight.setObjectName(u"sp_resHeight")
        self.sp_resHeight.setEnabled(False)
        self.sp_resHeight.setMinimum(1)
        self.sp_resHeight.setMaximum(99999)
        self.sp_resHeight.setValue(720)

        self.horizontalLayout_9.addWidget(self.sp_resHeight)

        self.b_resPresets = QPushButton(self.w_resolution)
        self.b_resPresets.setObjectName(u"b_resPresets")
        self.b_resPresets.setEnabled(False)
        self.b_resPresets.setMinimumSize(QSize(23, 23))
        self.b_resPresets.setMaximumSize(QSize(23, 23))

        self.horizontalLayout_9.addWidget(self.b_resPresets)


        self.verticalLayout_2.addWidget(self.w_resolution)

        self.widget_7 = QWidget(self.gb_imageRender)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, 0)
        self.label_7 = QLabel(self.widget_7)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_11.addWidget(self.label_7)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)

        self.chb_useTake = QCheckBox(self.widget_7)
        self.chb_useTake.setObjectName(u"chb_useTake")

        self.horizontalLayout_11.addWidget(self.chb_useTake)

        self.cb_take = QComboBox(self.widget_7)
        self.cb_take.setObjectName(u"cb_take")
        self.cb_take.setEnabled(False)
        self.cb_take.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_11.addWidget(self.cb_take)


        self.verticalLayout_2.addWidget(self.widget_7)

        self.w_renderPreset = QWidget(self.gb_imageRender)
        self.w_renderPreset.setObjectName(u"w_renderPreset")
        self.horizontalLayout_12 = QHBoxLayout(self.w_renderPreset)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, 0)
        self.l_renderPreset = QLabel(self.w_renderPreset)
        self.l_renderPreset.setObjectName(u"l_renderPreset")

        self.horizontalLayout_12.addWidget(self.l_renderPreset)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_6)

        self.chb_renderPreset = QCheckBox(self.w_renderPreset)
        self.chb_renderPreset.setObjectName(u"chb_renderPreset")

        self.horizontalLayout_12.addWidget(self.chb_renderPreset)

        self.cb_renderPreset = QComboBox(self.w_renderPreset)
        self.cb_renderPreset.setObjectName(u"cb_renderPreset")
        self.cb_renderPreset.setEnabled(False)
        self.cb_renderPreset.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_12.addWidget(self.cb_renderPreset)


        self.verticalLayout_2.addWidget(self.w_renderPreset)

        self.w_master = QWidget(self.gb_imageRender)
        self.w_master.setObjectName(u"w_master")
        self.horizontalLayout_20 = QHBoxLayout(self.w_master)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(9, 0, 9, 0)
        self.l_master = QLabel(self.w_master)
        self.l_master.setObjectName(u"l_master")

        self.horizontalLayout_20.addWidget(self.l_master)

        self.horizontalSpacer_29 = QSpacerItem(113, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_29)

        self.cb_master = QComboBox(self.w_master)
        self.cb_master.setObjectName(u"cb_master")
        self.cb_master.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_20.addWidget(self.cb_master)


        self.verticalLayout_2.addWidget(self.w_master)

        self.w_outPath = QWidget(self.gb_imageRender)
        self.w_outPath.setObjectName(u"w_outPath")
        self.horizontalLayout_18 = QHBoxLayout(self.w_outPath)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(9, 0, 9, 0)
        self.l_outPath = QLabel(self.w_outPath)
        self.l_outPath.setObjectName(u"l_outPath")

        self.horizontalLayout_18.addWidget(self.l_outPath)

        self.horizontalSpacer_9 = QSpacerItem(113, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_9)

        self.cb_outPath = QComboBox(self.w_outPath)
        self.cb_outPath.setObjectName(u"cb_outPath")
        self.cb_outPath.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_18.addWidget(self.cb_outPath)


        self.verticalLayout_2.addWidget(self.w_outPath)

        self.w_format = QWidget(self.gb_imageRender)
        self.w_format.setObjectName(u"w_format")
        self.horizontalLayout_13 = QHBoxLayout(self.w_format)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(9, 0, 9, 0)
        self.label_8 = QLabel(self.w_format)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_13.addWidget(self.label_8)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_14)

        self.chb_format = QCheckBox(self.w_format)
        self.chb_format.setObjectName(u"chb_format")

        self.horizontalLayout_13.addWidget(self.chb_format)

        self.cb_format = QComboBox(self.w_format)
        self.cb_format.setObjectName(u"cb_format")
        self.cb_format.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_13.addWidget(self.cb_format)


        self.verticalLayout_2.addWidget(self.w_format)

        self.f_renderer = QWidget(self.gb_imageRender)
        self.f_renderer.setObjectName(u"f_renderer")
        self.horizontalLayout_3 = QHBoxLayout(self.f_renderer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, 0, 9, 0)
        self.label_4 = QLabel(self.f_renderer)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.cb_renderer = QComboBox(self.f_renderer)
        self.cb_renderer.setObjectName(u"cb_renderer")
        self.cb_renderer.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.cb_renderer)


        self.verticalLayout_2.addWidget(self.f_renderer)

        self.f_status = QWidget(self.gb_imageRender)
        self.f_status.setObjectName(u"f_status")
        self.horizontalLayout_5 = QHBoxLayout(self.f_status)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.label_5 = QLabel(self.f_status)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(40, 0))
        self.label_5.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.l_status = QLabel(self.f_status)
        self.l_status.setObjectName(u"l_status")
        self.l_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.l_status)

        self.b_goTo = QPushButton(self.f_status)
        self.b_goTo.setObjectName(u"b_goTo")
        self.b_goTo.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_5.addWidget(self.b_goTo)


        self.verticalLayout_2.addWidget(self.f_status)

        self.f_connect = QWidget(self.gb_imageRender)
        self.f_connect.setObjectName(u"f_connect")
        self.horizontalLayout_6 = QHBoxLayout(self.f_connect)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.b_connect = QPushButton(self.f_connect)
        self.b_connect.setObjectName(u"b_connect")
        self.b_connect.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_6.addWidget(self.b_connect)


        self.verticalLayout_2.addWidget(self.f_connect)


        self.verticalLayout.addWidget(self.gb_imageRender)

        self.gb_submit = QGroupBox(wg_ImageRender)
        self.gb_submit.setObjectName(u"gb_submit")
        self.gb_submit.setCheckable(True)
        self.gb_submit.setChecked(True)
        self.verticalLayout_7 = QVBoxLayout(self.gb_submit)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 15, -1, -1)
        self.f_manager = QWidget(self.gb_submit)
        self.f_manager.setObjectName(u"f_manager")
        self.horizontalLayout_8 = QHBoxLayout(self.f_manager)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.l_manager = QLabel(self.f_manager)
        self.l_manager.setObjectName(u"l_manager")

        self.horizontalLayout_8.addWidget(self.l_manager)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_19)

        self.cb_manager = QComboBox(self.f_manager)
        self.cb_manager.setObjectName(u"cb_manager")
        self.cb_manager.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_8.addWidget(self.cb_manager)


        self.verticalLayout_7.addWidget(self.f_manager)

        self.f_rjPrio = QWidget(self.gb_submit)
        self.f_rjPrio.setObjectName(u"f_rjPrio")
        self.horizontalLayout_21 = QHBoxLayout(self.f_rjPrio)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, 0, -1, 0)
        self.l_rjPrio = QLabel(self.f_rjPrio)
        self.l_rjPrio.setObjectName(u"l_rjPrio")

        self.horizontalLayout_21.addWidget(self.l_rjPrio)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_15)

        self.sp_rjPrio = QSpinBox(self.f_rjPrio)
        self.sp_rjPrio.setObjectName(u"sp_rjPrio")
        self.sp_rjPrio.setMaximum(100)
        self.sp_rjPrio.setValue(50)

        self.horizontalLayout_21.addWidget(self.sp_rjPrio)


        self.verticalLayout_7.addWidget(self.f_rjPrio)

        self.f_rjWidgetsPerTask = QWidget(self.gb_submit)
        self.f_rjWidgetsPerTask.setObjectName(u"f_rjWidgetsPerTask")
        self.horizontalLayout_22 = QHBoxLayout(self.f_rjWidgetsPerTask)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 0, -1, 0)
        self.label_15 = QLabel(self.f_rjWidgetsPerTask)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_22.addWidget(self.label_15)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_16)

        self.sp_rjFramesPerTask = QSpinBox(self.f_rjWidgetsPerTask)
        self.sp_rjFramesPerTask.setObjectName(u"sp_rjFramesPerTask")
        self.sp_rjFramesPerTask.setMinimum(1)
        self.sp_rjFramesPerTask.setMaximum(9999)
        self.sp_rjFramesPerTask.setValue(5)

        self.horizontalLayout_22.addWidget(self.sp_rjFramesPerTask)


        self.verticalLayout_7.addWidget(self.f_rjWidgetsPerTask)

        self.f_rjTimeout = QWidget(self.gb_submit)
        self.f_rjTimeout.setObjectName(u"f_rjTimeout")
        self.horizontalLayout_28 = QHBoxLayout(self.f_rjTimeout)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(-1, 0, -1, 0)
        self.l_rjTimeout = QLabel(self.f_rjTimeout)
        self.l_rjTimeout.setObjectName(u"l_rjTimeout")

        self.horizontalLayout_28.addWidget(self.l_rjTimeout)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_22)

        self.sp_rjTimeout = QSpinBox(self.f_rjTimeout)
        self.sp_rjTimeout.setObjectName(u"sp_rjTimeout")
        self.sp_rjTimeout.setMinimum(1)
        self.sp_rjTimeout.setMaximum(9999)
        self.sp_rjTimeout.setValue(180)

        self.horizontalLayout_28.addWidget(self.sp_rjTimeout)


        self.verticalLayout_7.addWidget(self.f_rjTimeout)

        self.f_rjSuspended = QWidget(self.gb_submit)
        self.f_rjSuspended.setObjectName(u"f_rjSuspended")
        self.horizontalLayout_26 = QHBoxLayout(self.f_rjSuspended)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, 0, -1, 0)
        self.label_18 = QLabel(self.f_rjSuspended)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_26.addWidget(self.label_18)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_20)

        self.chb_rjSuspended = QCheckBox(self.f_rjSuspended)
        self.chb_rjSuspended.setObjectName(u"chb_rjSuspended")
        self.chb_rjSuspended.setChecked(False)

        self.horizontalLayout_26.addWidget(self.chb_rjSuspended)


        self.verticalLayout_7.addWidget(self.f_rjSuspended)

        self.w_renderIFDs = QWidget(self.gb_submit)
        self.w_renderIFDs.setObjectName(u"w_renderIFDs")
        self.horizontalLayout_35 = QHBoxLayout(self.w_renderIFDs)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(-1, 0, -1, 0)
        self.label_22 = QLabel(self.w_renderIFDs)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_35.addWidget(self.label_22)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_30)

        self.chb_rjIFDs = QCheckBox(self.w_renderIFDs)
        self.chb_rjIFDs.setObjectName(u"chb_rjIFDs")
        self.chb_rjIFDs.setChecked(True)

        self.horizontalLayout_35.addWidget(self.chb_rjIFDs)


        self.verticalLayout_7.addWidget(self.w_renderIFDs)

        self.w_renderNSIs = QWidget(self.gb_submit)
        self.w_renderNSIs.setObjectName(u"w_renderNSIs")
        self.horizontalLayout_32 = QHBoxLayout(self.w_renderNSIs)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(-1, 0, -1, 0)
        self.label_20 = QLabel(self.w_renderNSIs)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_32.addWidget(self.label_20)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_27)

        self.chb_rjNSIs = QCheckBox(self.w_renderNSIs)
        self.chb_rjNSIs.setObjectName(u"chb_rjNSIs")
        self.chb_rjNSIs.setChecked(True)

        self.horizontalLayout_32.addWidget(self.chb_rjNSIs)


        self.verticalLayout_7.addWidget(self.w_renderNSIs)

        self.w_renderRS = QWidget(self.gb_submit)
        self.w_renderRS.setObjectName(u"w_renderRS")
        self.horizontalLayout_33 = QHBoxLayout(self.w_renderRS)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(-1, 0, -1, 0)
        self.label_21 = QLabel(self.w_renderRS)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_33.addWidget(self.label_21)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_28)

        self.chb_rjRS = QCheckBox(self.w_renderRS)
        self.chb_rjRS.setObjectName(u"chb_rjRS")
        self.chb_rjRS.setChecked(True)

        self.horizontalLayout_33.addWidget(self.chb_rjRS)


        self.verticalLayout_7.addWidget(self.w_renderRS)

        self.w_renderASSs = QWidget(self.gb_submit)
        self.w_renderASSs.setObjectName(u"w_renderASSs")
        self.horizontalLayout_36 = QHBoxLayout(self.w_renderASSs)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(-1, 0, -1, 0)
        self.label_23 = QLabel(self.w_renderASSs)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_36.addWidget(self.label_23)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer_31)

        self.chb_rjASSs = QCheckBox(self.w_renderASSs)
        self.chb_rjASSs.setObjectName(u"chb_rjASSs")
        self.chb_rjASSs.setChecked(True)

        self.horizontalLayout_36.addWidget(self.chb_rjASSs)


        self.verticalLayout_7.addWidget(self.w_renderASSs)

        self.w_renderVrscenes = QWidget(self.gb_submit)
        self.w_renderVrscenes.setObjectName(u"w_renderVrscenes")
        self.horizontalLayout_38 = QHBoxLayout(self.w_renderVrscenes)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(-1, 0, -1, 0)
        self.label_24 = QLabel(self.w_renderVrscenes)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_38.addWidget(self.label_24)

        self.horizontalSpacer_33 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_33)

        self.chb_rjVrscenes = QCheckBox(self.w_renderVrscenes)
        self.chb_rjVrscenes.setObjectName(u"chb_rjVrscenes")
        self.chb_rjVrscenes.setChecked(True)

        self.horizontalLayout_38.addWidget(self.chb_rjVrscenes)


        self.verticalLayout_7.addWidget(self.w_renderVrscenes)

        self.w_exportScenesLocally = QWidget(self.gb_submit)
        self.w_exportScenesLocally.setObjectName(u"w_exportScenesLocally")
        self.horizontalLayout_39 = QHBoxLayout(self.w_exportScenesLocally)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(-1, 0, -1, 0)
        self.label_25 = QLabel(self.w_exportScenesLocally)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_39.addWidget(self.label_25)

        self.horizontalSpacer_34 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_39.addItem(self.horizontalSpacer_34)

        self.chb_exportScenesLocally = QCheckBox(self.w_exportScenesLocally)
        self.chb_exportScenesLocally.setObjectName(u"chb_exportScenesLocally")

        self.horizontalLayout_39.addWidget(self.chb_exportScenesLocally)


        self.verticalLayout_7.addWidget(self.w_exportScenesLocally)

        self.f_osDependencies = QWidget(self.gb_submit)
        self.f_osDependencies.setObjectName(u"f_osDependencies")
        self.horizontalLayout_27 = QHBoxLayout(self.f_osDependencies)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, -1, 0)
        self.label_19 = QLabel(self.f_osDependencies)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_27.addWidget(self.label_19)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_21)

        self.chb_osDependencies = QCheckBox(self.f_osDependencies)
        self.chb_osDependencies.setObjectName(u"chb_osDependencies")
        self.chb_osDependencies.setChecked(True)

        self.horizontalLayout_27.addWidget(self.chb_osDependencies)


        self.verticalLayout_7.addWidget(self.f_osDependencies)

        self.f_osUpload = QWidget(self.gb_submit)
        self.f_osUpload.setObjectName(u"f_osUpload")
        self.horizontalLayout_23 = QHBoxLayout(self.f_osUpload)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, 0, -1, 0)
        self.label_16 = QLabel(self.f_osUpload)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_23.addWidget(self.label_16)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_17)

        self.chb_osUpload = QCheckBox(self.f_osUpload)
        self.chb_osUpload.setObjectName(u"chb_osUpload")
        self.chb_osUpload.setChecked(True)

        self.horizontalLayout_23.addWidget(self.chb_osUpload)


        self.verticalLayout_7.addWidget(self.f_osUpload)

        self.f_osPAssets = QWidget(self.gb_submit)
        self.f_osPAssets.setObjectName(u"f_osPAssets")
        self.horizontalLayout_24 = QHBoxLayout(self.f_osPAssets)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 0, -1, 0)
        self.label_17 = QLabel(self.f_osPAssets)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_24.addWidget(self.label_17)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_18)

        self.chb_osPAssets = QCheckBox(self.f_osPAssets)
        self.chb_osPAssets.setObjectName(u"chb_osPAssets")
        self.chb_osPAssets.setChecked(True)

        self.horizontalLayout_24.addWidget(self.chb_osPAssets)


        self.verticalLayout_7.addWidget(self.f_osPAssets)

        self.gb_osSlaves = QGroupBox(self.gb_submit)
        self.gb_osSlaves.setObjectName(u"gb_osSlaves")
        self.horizontalLayout_25 = QHBoxLayout(self.gb_osSlaves)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(9, 3, 9, 3)
        self.e_osSlaves = QLineEdit(self.gb_osSlaves)
        self.e_osSlaves.setObjectName(u"e_osSlaves")

        self.horizontalLayout_25.addWidget(self.e_osSlaves)

        self.b_osSlaves = QPushButton(self.gb_osSlaves)
        self.b_osSlaves.setObjectName(u"b_osSlaves")
        self.b_osSlaves.setMaximumSize(QSize(25, 16777215))
        self.b_osSlaves.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_25.addWidget(self.b_osSlaves)


        self.verticalLayout_7.addWidget(self.gb_osSlaves)

        self.w_dlConcurrentTasks = QWidget(self.gb_submit)
        self.w_dlConcurrentTasks.setObjectName(u"w_dlConcurrentTasks")
        self.horizontalLayout_29 = QHBoxLayout(self.w_dlConcurrentTasks)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(-1, 0, -1, 0)
        self.l_dlConcurrentTasks = QLabel(self.w_dlConcurrentTasks)
        self.l_dlConcurrentTasks.setObjectName(u"l_dlConcurrentTasks")

        self.horizontalLayout_29.addWidget(self.l_dlConcurrentTasks)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_24)

        self.sp_dlConcurrentTasks = QSpinBox(self.w_dlConcurrentTasks)
        self.sp_dlConcurrentTasks.setObjectName(u"sp_dlConcurrentTasks")
        self.sp_dlConcurrentTasks.setMinimum(1)
        self.sp_dlConcurrentTasks.setMaximum(99)
        self.sp_dlConcurrentTasks.setValue(1)

        self.horizontalLayout_29.addWidget(self.sp_dlConcurrentTasks)


        self.verticalLayout_7.addWidget(self.w_dlConcurrentTasks)

        self.w_dlGPUpt = QWidget(self.gb_submit)
        self.w_dlGPUpt.setObjectName(u"w_dlGPUpt")
        self.horizontalLayout_30 = QHBoxLayout(self.w_dlGPUpt)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(-1, 0, -1, 0)
        self.l_dlGPUpt = QLabel(self.w_dlGPUpt)
        self.l_dlGPUpt.setObjectName(u"l_dlGPUpt")

        self.horizontalLayout_30.addWidget(self.l_dlGPUpt)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_25)

        self.sp_dlGPUpt = QSpinBox(self.w_dlGPUpt)
        self.sp_dlGPUpt.setObjectName(u"sp_dlGPUpt")
        self.sp_dlGPUpt.setMinimum(0)
        self.sp_dlGPUpt.setMaximum(99)
        self.sp_dlGPUpt.setValue(0)

        self.horizontalLayout_30.addWidget(self.sp_dlGPUpt)


        self.verticalLayout_7.addWidget(self.w_dlGPUpt)

        self.w_dlGPUdevices = QWidget(self.gb_submit)
        self.w_dlGPUdevices.setObjectName(u"w_dlGPUdevices")
        self.horizontalLayout_31 = QHBoxLayout(self.w_dlGPUdevices)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(-1, 0, -1, 0)
        self.l_dlGPUdevices = QLabel(self.w_dlGPUdevices)
        self.l_dlGPUdevices.setObjectName(u"l_dlGPUdevices")

        self.horizontalLayout_31.addWidget(self.l_dlGPUdevices)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_26)

        self.le_dlGPUdevices = QLineEdit(self.w_dlGPUdevices)
        self.le_dlGPUdevices.setObjectName(u"le_dlGPUdevices")
        self.le_dlGPUdevices.setMinimumSize(QSize(170, 0))

        self.horizontalLayout_31.addWidget(self.le_dlGPUdevices)


        self.verticalLayout_7.addWidget(self.w_dlGPUdevices)


        self.verticalLayout.addWidget(self.gb_submit)

        self.gb_passes = QGroupBox(wg_ImageRender)
        self.gb_passes.setObjectName(u"gb_passes")
        self.verticalLayout_5 = QVBoxLayout(self.gb_passes)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.w_separateAovs = QWidget(self.gb_passes)
        self.w_separateAovs.setObjectName(u"w_separateAovs")
        self.horizontalLayout_37 = QHBoxLayout(self.w_separateAovs)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(-1, 0, -1, 0)
        self.l_separateAovs = QLabel(self.w_separateAovs)
        self.l_separateAovs.setObjectName(u"l_separateAovs")

        self.horizontalLayout_37.addWidget(self.l_separateAovs)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_32)

        self.chb_separateAovs = QCheckBox(self.w_separateAovs)
        self.chb_separateAovs.setObjectName(u"chb_separateAovs")

        self.horizontalLayout_37.addWidget(self.chb_separateAovs)


        self.verticalLayout_5.addWidget(self.w_separateAovs)

        self.widget_14 = QWidget(self.gb_passes)
        self.widget_14.setObjectName(u"widget_14")
        self.horizontalLayout_14 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 9, -1, 0)
        self.tw_passes = QTableWidget(self.widget_14)
        if (self.tw_passes.columnCount() < 2):
            self.tw_passes.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tw_passes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tw_passes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tw_passes.setObjectName(u"tw_passes")
        self.tw_passes.setMinimumSize(QSize(0, 200))
        self.tw_passes.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tw_passes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tw_passes.horizontalHeader().setVisible(True)
        self.tw_passes.horizontalHeader().setHighlightSections(False)
        self.tw_passes.horizontalHeader().setStretchLastSection(True)
        self.tw_passes.verticalHeader().setVisible(False)

        self.horizontalLayout_14.addWidget(self.tw_passes)


        self.verticalLayout_5.addWidget(self.widget_14)

        self.widget_15 = QWidget(self.gb_passes)
        self.widget_15.setObjectName(u"widget_15")
        self.horizontalLayout_15 = QHBoxLayout(self.widget_15)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.b_addPasses = QPushButton(self.widget_15)
        self.b_addPasses.setObjectName(u"b_addPasses")
        self.b_addPasses.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_15.addWidget(self.b_addPasses)


        self.verticalLayout_5.addWidget(self.widget_15)


        self.verticalLayout.addWidget(self.gb_passes)

        self.groupBox_3 = QGroupBox(wg_ImageRender)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setChecked(False)
        self.horizontalLayout_34 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.scrollArea = QScrollArea(self.groupBox_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 338, 54))
        self.horizontalLayout_16 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.l_pathLast = QLabel(self.scrollAreaWidgetContents)
        self.l_pathLast.setObjectName(u"l_pathLast")

        self.horizontalLayout_16.addWidget(self.l_pathLast)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_34.addWidget(self.scrollArea)

        self.b_pathLast = QToolButton(self.groupBox_3)
        self.b_pathLast.setObjectName(u"b_pathLast")
        self.b_pathLast.setEnabled(True)
        self.b_pathLast.setArrowType(Qt.ArrowType.DownArrow)

        self.horizontalLayout_34.addWidget(self.b_pathLast)


        self.verticalLayout.addWidget(self.groupBox_3)

        QWidget.setTabOrder(self.e_name, self.cb_rangeType)
        QWidget.setTabOrder(self.cb_rangeType, self.sp_rangeStart)
        QWidget.setTabOrder(self.sp_rangeStart, self.sp_rangeEnd)
        QWidget.setTabOrder(self.sp_rangeEnd, self.le_frameExpression)
        QWidget.setTabOrder(self.le_frameExpression, self.chb_camOverride)
        QWidget.setTabOrder(self.chb_camOverride, self.cb_cams)
        QWidget.setTabOrder(self.cb_cams, self.chb_resOverride)
        QWidget.setTabOrder(self.chb_resOverride, self.sp_resWidth)
        QWidget.setTabOrder(self.sp_resWidth, self.sp_resHeight)
        QWidget.setTabOrder(self.sp_resHeight, self.b_resPresets)
        QWidget.setTabOrder(self.b_resPresets, self.chb_useTake)
        QWidget.setTabOrder(self.chb_useTake, self.cb_take)
        QWidget.setTabOrder(self.cb_take, self.chb_renderPreset)
        QWidget.setTabOrder(self.chb_renderPreset, self.cb_renderPreset)
        QWidget.setTabOrder(self.cb_renderPreset, self.cb_master)
        QWidget.setTabOrder(self.cb_master, self.cb_outPath)
        QWidget.setTabOrder(self.cb_outPath, self.cb_format)
        QWidget.setTabOrder(self.cb_format, self.cb_renderer)
        QWidget.setTabOrder(self.cb_renderer, self.gb_submit)
        QWidget.setTabOrder(self.gb_submit, self.cb_manager)
        QWidget.setTabOrder(self.cb_manager, self.sp_rjPrio)
        QWidget.setTabOrder(self.sp_rjPrio, self.sp_rjFramesPerTask)
        QWidget.setTabOrder(self.sp_rjFramesPerTask, self.sp_rjTimeout)
        QWidget.setTabOrder(self.sp_rjTimeout, self.chb_rjSuspended)
        QWidget.setTabOrder(self.chb_rjSuspended, self.chb_rjNSIs)
        QWidget.setTabOrder(self.chb_rjNSIs, self.chb_rjRS)
        QWidget.setTabOrder(self.chb_rjRS, self.chb_osDependencies)
        QWidget.setTabOrder(self.chb_osDependencies, self.chb_osUpload)
        QWidget.setTabOrder(self.chb_osUpload, self.chb_osPAssets)
        QWidget.setTabOrder(self.chb_osPAssets, self.e_osSlaves)
        QWidget.setTabOrder(self.e_osSlaves, self.sp_dlConcurrentTasks)
        QWidget.setTabOrder(self.sp_dlConcurrentTasks, self.sp_dlGPUpt)
        QWidget.setTabOrder(self.sp_dlGPUpt, self.le_dlGPUdevices)
        QWidget.setTabOrder(self.le_dlGPUdevices, self.tw_passes)
        QWidget.setTabOrder(self.tw_passes, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.b_pathLast)

        self.retranslateUi(wg_ImageRender)

        QMetaObject.connectSlotsByName(wg_ImageRender)
    # setupUi

    def retranslateUi(self, wg_ImageRender):
        wg_ImageRender.setWindowTitle(QCoreApplication.translate("wg_ImageRender", u"Image Render", None))
        self.l_name.setText(QCoreApplication.translate("wg_ImageRender", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_ImageRender", u"ImageRender", None))
        self.gb_imageRender.setTitle(QCoreApplication.translate("wg_ImageRender", u"General", None))
        self.l_comment.setText(QCoreApplication.translate("wg_ImageRender", u"Comment:", None))
        self.label_9.setText(QCoreApplication.translate("wg_ImageRender", u"Context:", None))
        self.l_context.setText("")
        self.b_context.setText(QCoreApplication.translate("wg_ImageRender", u"Select", None))
        self.label_2.setText(QCoreApplication.translate("wg_ImageRender", u"Identifier:", None))
        self.l_taskName.setText("")
        self.b_changeTask.setText(QCoreApplication.translate("wg_ImageRender", u"change", None))
        self.label_3.setText(QCoreApplication.translate("wg_ImageRender", u"Framerange:", None))
        self.l_rangeEnd.setText(QCoreApplication.translate("wg_ImageRender", u"1100", None))
        self.l_rangeStart.setText(QCoreApplication.translate("wg_ImageRender", u"1001", None))
        self.l_rangeStartInfo.setText(QCoreApplication.translate("wg_ImageRender", u"Start:", None))
        self.l_rangeEndInfo.setText(QCoreApplication.translate("wg_ImageRender", u"End:", None))
        self.l_frameExpression.setText(QCoreApplication.translate("wg_ImageRender", u"Frame expression:", None))
        self.label.setText(QCoreApplication.translate("wg_ImageRender", u"Camera override:", None))
        self.chb_camOverride.setText("")
        self.label_6.setText(QCoreApplication.translate("wg_ImageRender", u"Resolution override:", None))
        self.chb_resOverride.setText("")
        self.b_resPresets.setText(QCoreApplication.translate("wg_ImageRender", u"\u25bc", None))
        self.label_7.setText(QCoreApplication.translate("wg_ImageRender", u"Override take:", None))
        self.chb_useTake.setText("")
        self.l_renderPreset.setText(QCoreApplication.translate("wg_ImageRender", u"Rendersettings preset:", None))
        self.chb_renderPreset.setText("")
        self.l_master.setText(QCoreApplication.translate("wg_ImageRender", u"Master Version:", None))
        self.l_outPath.setText(QCoreApplication.translate("wg_ImageRender", u"Location:", None))
        self.label_8.setText(QCoreApplication.translate("wg_ImageRender", u"Format:", None))
        self.chb_format.setText("")
        self.label_4.setText(QCoreApplication.translate("wg_ImageRender", u"Renderer:", None))
        self.label_5.setText(QCoreApplication.translate("wg_ImageRender", u"Status:", None))
        self.l_status.setText(QCoreApplication.translate("wg_ImageRender", u"Not connected", None))
        self.b_goTo.setText(QCoreApplication.translate("wg_ImageRender", u"Go to Node", None))
        self.b_connect.setText(QCoreApplication.translate("wg_ImageRender", u"Connect to selected ROP", None))
        self.gb_submit.setTitle(QCoreApplication.translate("wg_ImageRender", u"Submit Render Job", None))
        self.l_manager.setText(QCoreApplication.translate("wg_ImageRender", u"Manager:", None))
        self.l_rjPrio.setText(QCoreApplication.translate("wg_ImageRender", u"Priority:", None))
        self.label_15.setText(QCoreApplication.translate("wg_ImageRender", u"Frames per Task:", None))
        self.l_rjTimeout.setText(QCoreApplication.translate("wg_ImageRender", u"Task Timeout (min)", None))
        self.label_18.setText(QCoreApplication.translate("wg_ImageRender", u"Submit suspended:", None))
        self.chb_rjSuspended.setText("")
        self.label_22.setText(QCoreApplication.translate("wg_ImageRender", u"Render .ifd files:", None))
        self.chb_rjIFDs.setText("")
        self.label_20.setText(QCoreApplication.translate("wg_ImageRender", u"Render NSIs:", None))
        self.chb_rjNSIs.setText("")
        self.label_21.setText(QCoreApplication.translate("wg_ImageRender", u"Render .rs files:", None))
        self.chb_rjRS.setText("")
        self.label_23.setText(QCoreApplication.translate("wg_ImageRender", u"Render .ass files:", None))
        self.chb_rjASSs.setText("")
        self.label_24.setText(QCoreApplication.translate("wg_ImageRender", u"Render .vrscene files:", None))
        self.chb_rjVrscenes.setText("")
        self.label_25.setText(QCoreApplication.translate("wg_ImageRender", u"Export scene description locally:", None))
        self.chb_exportScenesLocally.setText("")
        self.label_19.setText(QCoreApplication.translate("wg_ImageRender", u"Submit dependent files:", None))
        self.chb_osDependencies.setText("")
        self.label_16.setText(QCoreApplication.translate("wg_ImageRender", u"Upload output:", None))
        self.chb_osUpload.setText("")
        self.label_17.setText(QCoreApplication.translate("wg_ImageRender", u"Use Project Assets", None))
        self.chb_osPAssets.setText("")
        self.gb_osSlaves.setTitle(QCoreApplication.translate("wg_ImageRender", u"Assign to slaves:", None))
        self.b_osSlaves.setText(QCoreApplication.translate("wg_ImageRender", u"...", None))
        self.l_dlConcurrentTasks.setText(QCoreApplication.translate("wg_ImageRender", u"Concurrent Tasks:", None))
        self.l_dlGPUpt.setText(QCoreApplication.translate("wg_ImageRender", u"GPUs Per Task:", None))
        self.l_dlGPUdevices.setText(QCoreApplication.translate("wg_ImageRender", u"Select GPU Devices:", None))
        self.le_dlGPUdevices.setPlaceholderText(QCoreApplication.translate("wg_ImageRender", u"Enter Valid GPU Device Id(s)", None))
        self.gb_passes.setTitle(QCoreApplication.translate("wg_ImageRender", u"Render Passes", None))
        self.l_separateAovs.setText(QCoreApplication.translate("wg_ImageRender", u"Save as separate files:", None))
        self.chb_separateAovs.setText("")
        ___qtablewidgetitem = self.tw_passes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("wg_ImageRender", u"Name", None));
        ___qtablewidgetitem1 = self.tw_passes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("wg_ImageRender", u"VEX Variable", None));
        self.b_addPasses.setText(QCoreApplication.translate("wg_ImageRender", u"Add Passes", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("wg_ImageRender", u"Last render", None))
        self.l_pathLast.setText(QCoreApplication.translate("wg_ImageRender", u"None", None))
        self.b_pathLast.setText(QCoreApplication.translate("wg_ImageRender", u"...", None))
    # retranslateUi

