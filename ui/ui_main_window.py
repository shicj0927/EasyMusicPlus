# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollBar, QSizePolicy, QSlider,
    QSpacerItem, QSplitter, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(1148, 701)
        self.qAction_openDB = QAction(mainWindow)
        self.qAction_openDB.setObjectName(u"qAction_openDB")
        self.qAction_newDB = QAction(mainWindow)
        self.qAction_newDB.setObjectName(u"qAction_newDB")
        self.qAction_openSong = QAction(mainWindow)
        self.qAction_openSong.setObjectName(u"qAction_openSong")
        self.qAction_quit = QAction(mainWindow)
        self.qAction_quit.setObjectName(u"qAction_quit")
        self.qAction_setting = QAction(mainWindow)
        self.qAction_setting.setObjectName(u"qAction_setting")
        self.qAction_openList = QAction(mainWindow)
        self.qAction_openList.setObjectName(u"qAction_openList")
        self.qAction_newList = QAction(mainWindow)
        self.qAction_newList.setObjectName(u"qAction_newList")
        self.qAction_about = QAction(mainWindow)
        self.qAction_about.setObjectName(u"qAction_about")
        self.centralWidget = QWidget(mainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.qSplitter_mainSplitter = QSplitter(self.centralWidget)
        self.qSplitter_mainSplitter.setObjectName(u"qSplitter_mainSplitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qSplitter_mainSplitter.sizePolicy().hasHeightForWidth())
        self.qSplitter_mainSplitter.setSizePolicy(sizePolicy)
        self.qSplitter_mainSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.qWidget_listsArea = QWidget(self.qSplitter_mainSplitter)
        self.qWidget_listsArea.setObjectName(u"qWidget_listsArea")
        self.qVBoxLayout_listsArea = QVBoxLayout(self.qWidget_listsArea)
        self.qVBoxLayout_listsArea.setObjectName(u"qVBoxLayout_listsArea")
        self.qVBoxLayout_listsArea.setContentsMargins(0, 0, 0, 0)
        self.qLabel_listsTitle = QLabel(self.qWidget_listsArea)
        self.qLabel_listsTitle.setObjectName(u"qLabel_listsTitle")

        self.qVBoxLayout_listsArea.addWidget(self.qLabel_listsTitle)

        self.qListWidget_listsList = QListWidget(self.qWidget_listsArea)
        self.qListWidget_listsList.setObjectName(u"qListWidget_listsList")

        self.qVBoxLayout_listsArea.addWidget(self.qListWidget_listsList)

        self.qSplitter_mainSplitter.addWidget(self.qWidget_listsArea)
        self.qWidget_songsArea = QWidget(self.qSplitter_mainSplitter)
        self.qWidget_songsArea.setObjectName(u"qWidget_songsArea")
        self.qVBoxLayout_songsArea = QVBoxLayout(self.qWidget_songsArea)
        self.qVBoxLayout_songsArea.setObjectName(u"qVBoxLayout_songsArea")
        self.qVBoxLayout_songsArea.setContentsMargins(0, 0, 0, 0)
        self.qLabel_songsTitle = QLabel(self.qWidget_songsArea)
        self.qLabel_songsTitle.setObjectName(u"qLabel_songsTitle")

        self.qVBoxLayout_songsArea.addWidget(self.qLabel_songsTitle)

        self.qListWidget_songsList = QListWidget(self.qWidget_songsArea)
        self.qListWidget_songsList.setObjectName(u"qListWidget_songsList")

        self.qVBoxLayout_songsArea.addWidget(self.qListWidget_songsList)

        self.qSplitter_mainSplitter.addWidget(self.qWidget_songsArea)
        self.qWidget_infoArea = QWidget(self.qSplitter_mainSplitter)
        self.qWidget_infoArea.setObjectName(u"qWidget_infoArea")
        self.qVBoxLayout_infoArea = QVBoxLayout(self.qWidget_infoArea)
        self.qVBoxLayout_infoArea.setObjectName(u"qVBoxLayout_infoArea")
        self.qVBoxLayout_infoArea.setContentsMargins(0, 0, 0, 0)
        self.qLabel_nowPlayingInfo = QLabel(self.qWidget_infoArea)
        self.qLabel_nowPlayingInfo.setObjectName(u"qLabel_nowPlayingInfo")

        self.qVBoxLayout_infoArea.addWidget(self.qLabel_nowPlayingInfo)

        self.qHBoxLayout_lyricArea = QHBoxLayout()
        self.qHBoxLayout_lyricArea.setObjectName(u"qHBoxLayout_lyricArea")
        self.qListWidget_lyricList = QListWidget(self.qWidget_infoArea)
        QListWidgetItem(self.qListWidget_lyricList)
        self.qListWidget_lyricList.setObjectName(u"qListWidget_lyricList")

        self.qHBoxLayout_lyricArea.addWidget(self.qListWidget_lyricList)

        self.qScrollBar_lyricScrollBar = QScrollBar(self.qWidget_infoArea)
        self.qScrollBar_lyricScrollBar.setObjectName(u"qScrollBar_lyricScrollBar")
        self.qScrollBar_lyricScrollBar.setOrientation(Qt.Orientation.Vertical)

        self.qHBoxLayout_lyricArea.addWidget(self.qScrollBar_lyricScrollBar)


        self.qVBoxLayout_infoArea.addLayout(self.qHBoxLayout_lyricArea)

        self.qSplitter_mainSplitter.addWidget(self.qWidget_infoArea)

        self.verticalLayout_4.addWidget(self.qSplitter_mainSplitter)

        self.qLabel_nowPlaying = QLabel(self.centralWidget)
        self.qLabel_nowPlaying.setObjectName(u"qLabel_nowPlaying")

        self.verticalLayout_4.addWidget(self.qLabel_nowPlaying)

        self.qHBoxLayout_progressArea = QHBoxLayout()
        self.qHBoxLayout_progressArea.setObjectName(u"qHBoxLayout_progressArea")
        self.qLabel_progressLeft = QLabel(self.centralWidget)
        self.qLabel_progressLeft.setObjectName(u"qLabel_progressLeft")

        self.qHBoxLayout_progressArea.addWidget(self.qLabel_progressLeft)

        self.qSlider_progressBar = QSlider(self.centralWidget)
        self.qSlider_progressBar.setObjectName(u"qSlider_progressBar")
        self.qSlider_progressBar.setOrientation(Qt.Orientation.Horizontal)

        self.qHBoxLayout_progressArea.addWidget(self.qSlider_progressBar)

        self.qLabel_progressRight = QLabel(self.centralWidget)
        self.qLabel_progressRight.setObjectName(u"qLabel_progressRight")

        self.qHBoxLayout_progressArea.addWidget(self.qLabel_progressRight)


        self.verticalLayout_4.addLayout(self.qHBoxLayout_progressArea)

        self.qHBoxLayout_controlArea = QHBoxLayout()
        self.qHBoxLayout_controlArea.setObjectName(u"qHBoxLayout_controlArea")
        self.qPushButton_control = QPushButton(self.centralWidget)
        self.qPushButton_control.setObjectName(u"qPushButton_control")

        self.qHBoxLayout_controlArea.addWidget(self.qPushButton_control)

        self.qPushButton_prev = QPushButton(self.centralWidget)
        self.qPushButton_prev.setObjectName(u"qPushButton_prev")

        self.qHBoxLayout_controlArea.addWidget(self.qPushButton_prev)

        self.qPushButton_stop = QPushButton(self.centralWidget)
        self.qPushButton_stop.setObjectName(u"qPushButton_stop")

        self.qHBoxLayout_controlArea.addWidget(self.qPushButton_stop)

        self.qPushButton_next = QPushButton(self.centralWidget)
        self.qPushButton_next.setObjectName(u"qPushButton_next")

        self.qHBoxLayout_controlArea.addWidget(self.qPushButton_next)

        self.qPushButton_mode = QPushButton(self.centralWidget)
        self.qPushButton_mode.setObjectName(u"qPushButton_mode")

        self.qHBoxLayout_controlArea.addWidget(self.qPushButton_mode)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.qHBoxLayout_controlArea.addItem(self.horizontalSpacer)

        self.qLabel_soundIcon = QLabel(self.centralWidget)
        self.qLabel_soundIcon.setObjectName(u"qLabel_soundIcon")

        self.qHBoxLayout_controlArea.addWidget(self.qLabel_soundIcon)

        self.qSlider_soundBar = QSlider(self.centralWidget)
        self.qSlider_soundBar.setObjectName(u"qSlider_soundBar")
        self.qSlider_soundBar.setOrientation(Qt.Orientation.Horizontal)

        self.qHBoxLayout_controlArea.addWidget(self.qSlider_soundBar)


        self.verticalLayout_4.addLayout(self.qHBoxLayout_controlArea)

        mainWindow.setCentralWidget(self.centralWidget)
        self.qMenuBar_menuBar = QMenuBar(mainWindow)
        self.qMenuBar_menuBar.setObjectName(u"qMenuBar_menuBar")
        self.qMenuBar_menuBar.setGeometry(QRect(0, 0, 1148, 23))
        self.qMenu_file = QMenu(self.qMenuBar_menuBar)
        self.qMenu_file.setObjectName(u"qMenu_file")
        self.qMenu_tool = QMenu(self.qMenuBar_menuBar)
        self.qMenu_tool.setObjectName(u"qMenu_tool")
        self.qMenu_about = QMenu(self.qMenuBar_menuBar)
        self.qMenu_about.setObjectName(u"qMenu_about")
        mainWindow.setMenuBar(self.qMenuBar_menuBar)
        self.qStatusBar_statusBar = QStatusBar(mainWindow)
        self.qStatusBar_statusBar.setObjectName(u"qStatusBar_statusBar")
        mainWindow.setStatusBar(self.qStatusBar_statusBar)

        self.qMenuBar_menuBar.addAction(self.qMenu_file.menuAction())
        self.qMenuBar_menuBar.addAction(self.qMenu_tool.menuAction())
        self.qMenuBar_menuBar.addAction(self.qMenu_about.menuAction())
        self.qMenu_file.addAction(self.qAction_openDB)
        self.qMenu_file.addAction(self.qAction_newDB)
        self.qMenu_file.addSeparator()
        self.qMenu_file.addAction(self.qAction_openList)
        self.qMenu_file.addAction(self.qAction_newList)
        self.qMenu_file.addSeparator()
        self.qMenu_file.addAction(self.qAction_openSong)
        self.qMenu_file.addSeparator()
        self.qMenu_file.addAction(self.qAction_quit)
        self.qMenu_tool.addAction(self.qAction_setting)
        self.qMenu_about.addAction(self.qAction_about)

        self.retranslateUi(mainWindow)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Easy Music Plus", None))
        self.qAction_openDB.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6b4c\u66f2\u5e93", None))
        self.qAction_newDB.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u6b4c\u66f2\u5e93", None))
        self.qAction_openSong.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6b4c\u66f2", None))
        self.qAction_quit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.qAction_setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.qAction_openList.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6b4c\u5355", None))
        self.qAction_newList.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u6b4c\u5355", None))
        self.qAction_about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.qLabel_listsTitle.setText(QCoreApplication.translate("MainWindow", u"\u6b4c\u5355\u5217\u8868", None))
        self.qLabel_songsTitle.setText(QCoreApplication.translate("MainWindow", u"\u6b4c\u66f2\u5217\u8868", None))
        self.qLabel_nowPlayingInfo.setText(QCoreApplication.translate("MainWindow", u"\u65e0\u66f2\u76ee", None))

        __sortingEnabled = self.qListWidget_lyricList.isSortingEnabled()
        self.qListWidget_lyricList.setSortingEnabled(False)
        ___qlistwidgetitem = self.qListWidget_lyricList.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u65e0\u6b4c\u8bcd", None))
        self.qListWidget_lyricList.setSortingEnabled(__sortingEnabled)

        self.qLabel_nowPlaying.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u64ad\u653e\uff1a-", None))
        self.qLabel_progressLeft.setText(QCoreApplication.translate("MainWindow", u"--:--/--:--", None))
        self.qLabel_progressRight.setText(QCoreApplication.translate("MainWindow", u"--:--", None))
        self.qPushButton_control.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
        self.qPushButton_prev.setText(QCoreApplication.translate("MainWindow", u"\u23ee", None))
        self.qPushButton_stop.setText(QCoreApplication.translate("MainWindow", u"\u23f9", None))
        self.qPushButton_next.setText(QCoreApplication.translate("MainWindow", u"\u23ed", None))
        self.qPushButton_mode.setText(QCoreApplication.translate("MainWindow", u"->", None))
        self.qLabel_soundIcon.setText(QCoreApplication.translate("MainWindow", u"\U0001f50a", None))
        self.qMenu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.qMenu_tool.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
        self.qMenu_about.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
    # retranslateUi

