# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(989, 836)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.main_dashboard = QWidget()
        self.main_dashboard.setObjectName(u"main_dashboard")
        self.groupBox_7 = QGroupBox(self.main_dashboard)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(20, 460, 921, 251))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.groupBox_7.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.txt_system_log = QTextEdit(self.groupBox_7)
        self.txt_system_log.setObjectName(u"txt_system_log")
        self.txt_system_log.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.txt_system_log)

        self.groupBox_8 = QGroupBox(self.main_dashboard)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(20, 120, 921, 321))
        self.groupBox_8.setFont(font)
        self.graph_temperature = PlotWidget(self.groupBox_8)
        self.graph_temperature.setObjectName(u"graph_temperature")
        self.graph_temperature.setGeometry(QRect(20, 90, 881, 211))
        self.layoutWidget = QWidget(self.groupBox_8)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 41, 881, 30))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_current = QLabel(self.layoutWidget)
        self.lbl_current.setObjectName(u"lbl_current")
        self.lbl_current.setFont(font)

        self.horizontalLayout.addWidget(self.lbl_current)

        self.dash_current = QLabel(self.layoutWidget)
        self.dash_current.setObjectName(u"dash_current")
        self.dash_current.setFont(font)

        self.horizontalLayout.addWidget(self.dash_current)

        self.lbl_high_limit = QLabel(self.layoutWidget)
        self.lbl_high_limit.setObjectName(u"lbl_high_limit")
        self.lbl_high_limit.setFont(font)

        self.horizontalLayout.addWidget(self.lbl_high_limit)

        self.dash_high = QLabel(self.layoutWidget)
        self.dash_high.setObjectName(u"dash_high")
        self.dash_high.setFont(font)

        self.horizontalLayout.addWidget(self.dash_high)

        self.lbl_low_limit = QLabel(self.layoutWidget)
        self.lbl_low_limit.setObjectName(u"lbl_low_limit")
        self.lbl_low_limit.setFont(font)

        self.horizontalLayout.addWidget(self.lbl_low_limit)

        self.dash_low = QLabel(self.layoutWidget)
        self.dash_low.setObjectName(u"dash_low")
        self.dash_low.setFont(font)

        self.horizontalLayout.addWidget(self.dash_low)

        self.groupBox_9 = QGroupBox(self.main_dashboard)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(20, 10, 921, 91))
        self.groupBox_9.setFont(font)
        self.widget = QWidget(self.groupBox_9)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(17, 32, 891, 44))
        self.horizontalLayout_15 = QHBoxLayout(self.widget)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.ip_label = QLabel(self.widget)
        self.ip_label.setObjectName(u"ip_label")

        self.horizontalLayout_12.addWidget(self.ip_label)

        self.search_ip = QLineEdit(self.widget)
        self.search_ip.setObjectName(u"search_ip")

        self.horizontalLayout_12.addWidget(self.search_ip)

        self.port_label_2 = QLabel(self.widget)
        self.port_label_2.setObjectName(u"port_label_2")

        self.horizontalLayout_12.addWidget(self.port_label_2)

        self.search_port = QLineEdit(self.widget)
        self.search_port.setObjectName(u"search_port")

        self.horizontalLayout_12.addWidget(self.search_port)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.connect_pushButton = QPushButton(self.widget)
        self.connect_pushButton.setObjectName(u"connect_pushButton")

        self.horizontalLayout_13.addWidget(self.connect_pushButton)

        self.disconnect_pushButton = QPushButton(self.widget)
        self.disconnect_pushButton.setObjectName(u"disconnect_pushButton")

        self.horizontalLayout_13.addWidget(self.disconnect_pushButton)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_13)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.horizontalLayout_4.addWidget(self.label)

        self.lbl_status = QLabel(self.widget)
        self.lbl_status.setObjectName(u"lbl_status")
        self.lbl_status.setFont(font)

        self.horizontalLayout_4.addWidget(self.lbl_status)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.main_dashboard, "")
        self.data_inquiry = QWidget()
        self.data_inquiry.setObjectName(u"data_inquiry")
        self.groupBox = QGroupBox(self.data_inquiry)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 30, 941, 101))
        self.groupBox.setFont(font)
        self.inquiry_btn_search = QPushButton(self.groupBox)
        self.inquiry_btn_search.setObjectName(u"inquiry_btn_search")
        self.inquiry_btn_search.setGeometry(QRect(800, 47, 101, 26))
        self.layoutWidget1 = QWidget(self.groupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(40, 40, 716, 40))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.dt_start = QDateTimeEdit(self.layoutWidget1)
        self.dt_start.setObjectName(u"dt_start")
        self.dt_start.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.dt_start)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.dt_end = QDateTimeEdit(self.layoutWidget1)
        self.dt_end.setObjectName(u"dt_end")
        self.dt_end.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.dt_end)

        self.groupBox_2 = QGroupBox(self.data_inquiry)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 270, 941, 421))
        self.groupBox_2.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.graph_inquiry = PlotWidget(self.groupBox_2)
        self.graph_inquiry.setObjectName(u"graph_inquiry")

        self.gridLayout_2.addWidget(self.graph_inquiry, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.data_inquiry)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 150, 941, 101))
        self.groupBox_3.setFont(font)
        self.layoutWidget2 = QWidget(self.groupBox_3)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(20, 45, 901, 32))
        self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lbl_current_2 = QLabel(self.layoutWidget2)
        self.lbl_current_2.setObjectName(u"lbl_current_2")

        self.horizontalLayout_3.addWidget(self.lbl_current_2)

        self.inquiry_avg = QLabel(self.layoutWidget2)
        self.inquiry_avg.setObjectName(u"inquiry_avg")

        self.horizontalLayout_3.addWidget(self.inquiry_avg)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lbl_high_limit_2 = QLabel(self.layoutWidget2)
        self.lbl_high_limit_2.setObjectName(u"lbl_high_limit_2")

        self.horizontalLayout_5.addWidget(self.lbl_high_limit_2)

        self.inquiry_high = QLabel(self.layoutWidget2)
        self.inquiry_high.setObjectName(u"inquiry_high")

        self.horizontalLayout_5.addWidget(self.inquiry_high)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lbl_low_limit_2 = QLabel(self.layoutWidget2)
        self.lbl_low_limit_2.setObjectName(u"lbl_low_limit_2")

        self.horizontalLayout_6.addWidget(self.lbl_low_limit_2)

        self.inquiry_low = QLabel(self.layoutWidget2)
        self.inquiry_low.setObjectName(u"inquiry_low")

        self.horizontalLayout_6.addWidget(self.inquiry_low)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)

        self.tabWidget.addTab(self.data_inquiry, "")
        self.settings = QWidget()
        self.settings.setObjectName(u"settings")
        self.groupBox_4 = QGroupBox(self.settings)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 30, 931, 161))
        self.groupBox_4.setFont(font)
        self.set_btn_save = QPushButton(self.groupBox_4)
        self.set_btn_save.setObjectName(u"set_btn_save")
        self.set_btn_save.setGeometry(QRect(800, 73, 81, 31))
        self.layoutWidget3 = QWidget(self.groupBox_4)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(40, 70, 751, 40))
        self.horizontalLayout_8 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.lbl_high_limit_3 = QLabel(self.layoutWidget3)
        self.lbl_high_limit_3.setObjectName(u"lbl_high_limit_3")

        self.horizontalLayout_8.addWidget(self.lbl_high_limit_3)

        self.set_high = QDoubleSpinBox(self.layoutWidget3)
        self.set_high.setObjectName(u"set_high")
        self.set_high.setMaximum(100.000000000000000)
        self.set_high.setSingleStep(0.100000000000000)

        self.horizontalLayout_8.addWidget(self.set_high)

        self.lbl_low_limit_3 = QLabel(self.layoutWidget3)
        self.lbl_low_limit_3.setObjectName(u"lbl_low_limit_3")

        self.horizontalLayout_8.addWidget(self.lbl_low_limit_3)

        self.set_low = QDoubleSpinBox(self.layoutWidget3)
        self.set_low.setObjectName(u"set_low")
        self.set_low.setMaximum(100.000000000000000)
        self.set_low.setSingleStep(0.100000000000000)

        self.horizontalLayout_8.addWidget(self.set_low)

        self.groupBox_5 = QGroupBox(self.settings)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 230, 931, 161))
        self.groupBox_5.setFont(font)
        self.set_btn_save_2 = QPushButton(self.groupBox_5)
        self.set_btn_save_2.setObjectName(u"set_btn_save_2")
        self.set_btn_save_2.setGeometry(QRect(800, 73, 81, 31))
        self.layoutWidget4 = QWidget(self.groupBox_5)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(40, 70, 751, 40))
        self.horizontalLayout_9 = QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.plc_label = QLabel(self.layoutWidget4)
        self.plc_label.setObjectName(u"plc_label")

        self.horizontalLayout_9.addWidget(self.plc_label)

        self.set_plc_ip = QLineEdit(self.layoutWidget4)
        self.set_plc_ip.setObjectName(u"set_plc_ip")

        self.horizontalLayout_9.addWidget(self.set_plc_ip)

        self.port_label = QLabel(self.layoutWidget4)
        self.port_label.setObjectName(u"port_label")

        self.horizontalLayout_9.addWidget(self.port_label)

        self.set_plc_port = QLineEdit(self.layoutWidget4)
        self.set_plc_port.setObjectName(u"set_plc_port")

        self.horizontalLayout_9.addWidget(self.set_plc_port)

        self.groupBox_6 = QGroupBox(self.settings)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(10, 420, 931, 291))
        self.groupBox_6.setFont(font)
        self.set_btn_save_3 = QPushButton(self.groupBox_6)
        self.set_btn_save_3.setObjectName(u"set_btn_save_3")
        self.set_btn_save_3.setGeometry(QRect(800, 220, 81, 38))
        self.layoutWidget5 = QWidget(self.groupBox_6)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(41, 51, 841, 161))
        self.verticalLayout = QVBoxLayout(self.layoutWidget5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.db_path_label = QLabel(self.layoutWidget5)
        self.db_path_label.setObjectName(u"db_path_label")

        self.horizontalLayout_10.addWidget(self.db_path_label)

        self.set_db_path = QLineEdit(self.layoutWidget5)
        self.set_db_path.setObjectName(u"set_db_path")
        self.set_db_path.setReadOnly(True)

        self.horizontalLayout_10.addWidget(self.set_db_path)

        self.set_btn_find = QPushButton(self.layoutWidget5)
        self.set_btn_find.setObjectName(u"set_btn_find")

        self.horizontalLayout_10.addWidget(self.set_btn_find)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.db_table_label = QLabel(self.layoutWidget5)
        self.db_table_label.setObjectName(u"db_table_label")

        self.horizontalLayout_11.addWidget(self.db_table_label)

        self.set_db_table = QLineEdit(self.layoutWidget5)
        self.set_db_table.setObjectName(u"set_db_table")

        self.horizontalLayout_11.addWidget(self.set_db_table)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.tabWidget.addTab(self.settings, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 989, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\uc2dc\uc2a4\ud15c \ub85c\uadf8", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\uc628\ub3c4 \ubaa8\ub2c8\ud130\ub9c1", None))
        self.lbl_current.setText(QCoreApplication.translate("MainWindow", u"\ud604\uc7ac:", None))
        self.dash_current.setText(QCoreApplication.translate("MainWindow", u"--.- \u2103", None))
        self.lbl_high_limit.setText(QCoreApplication.translate("MainWindow", u"\uc0c1\ud55c", None))
        self.dash_high.setText(QCoreApplication.translate("MainWindow", u"--.- \u2103", None))
        self.lbl_low_limit.setText(QCoreApplication.translate("MainWindow", u"\ud558\ud55c", None))
        self.dash_low.setText(QCoreApplication.translate("MainWindow", u"--.- \u2103", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"\ud1b5\uc2e0 \uc0c1\ud0dc", None))
        self.ip_label.setText(QCoreApplication.translate("MainWindow", u"IP:", None))
        self.port_label_2.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.connect_pushButton.setText(QCoreApplication.translate("MainWindow", u"\uc811\uc18d", None))
        self.disconnect_pushButton.setText(QCoreApplication.translate("MainWindow", u"\ud574\uc81c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ud1b5\uc2e0 \uc0c1\ud0dc:", None))
        self.lbl_status.setText(QCoreApplication.translate("MainWindow", u"\u25cf \uc5f0\uacb0 \ub300\uae30 \uc911", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_dashboard), QCoreApplication.translate("MainWindow", u"\uba54\uc778 \ub300\uc2dc\ubcf4\ub4dc", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\uc870\ud68c \uae30\uac04 \uc124\uc815", None))
        self.inquiry_btn_search.setText(QCoreApplication.translate("MainWindow", u"\uc870\ud68c", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791 \uc77c\uc2dc:", None))
        self.dt_start.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"~", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uc885\ub8cc \uc77c\uc2dc:", None))
        self.dt_end.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\uc870\ud68c \uc628\ub3c4 \ubcc0\ud654 \ucd94\uc774 \uadf8\ub798\ud504", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\uc694\uc57d \ud1b5\uacc4 \uc815\ubcf4", None))
        self.lbl_current_2.setText(QCoreApplication.translate("MainWindow", u"\ud3c9\uade0:", None))
        self.inquiry_avg.setText(QCoreApplication.translate("MainWindow", u"--.- \u2103", None))
        self.lbl_high_limit_2.setText(QCoreApplication.translate("MainWindow", u"\uc0c1\ud55c:", None))
        self.inquiry_high.setText(QCoreApplication.translate("MainWindow", u"--.- \u2103", None))
        self.lbl_low_limit_2.setText(QCoreApplication.translate("MainWindow", u"\ud558\ud55c:", None))
        self.inquiry_low.setText(QCoreApplication.translate("MainWindow", u"--.- \u2103", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data_inquiry), QCoreApplication.translate("MainWindow", u"\uc870\ud68c \ud654\uba74", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\uc628\ub3c4 \uc0c1/\ud558\ud55c \uc124\uc815", None))
        self.set_btn_save.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.lbl_high_limit_3.setText(QCoreApplication.translate("MainWindow", u"\uc0c1\ud55c\uce58:", None))
        self.set_high.setSuffix(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.lbl_low_limit_3.setText(QCoreApplication.translate("MainWindow", u"\ud558\ud55c\uce58:", None))
        self.set_low.setSuffix(QCoreApplication.translate("MainWindow", u"\u2103", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"PLC \ud1b5\uc2e0 \uc124\uc815", None))
        self.set_btn_save_2.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.plc_label.setText(QCoreApplication.translate("MainWindow", u"PLC IP:", None))
        self.port_label.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\ub370\uc774\ud130\ubca0\uc774\uc2a4(DB) \uc124\uc815", None))
        self.set_btn_save_3.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.db_path_label.setText(QCoreApplication.translate("MainWindow", u"DB \ud30c\uc77c \uacbd\ub85c:", None))
        self.set_btn_find.setText(QCoreApplication.translate("MainWindow", u"\ucc3e\uae30", None))
        self.db_table_label.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5 \ud14c\uc774\ube14\uba85:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), QCoreApplication.translate("MainWindow", u"\uc124\uc815 \ud654\uba74", None))
    # retranslateUi

