# coding:utf-8
import json
import os
import sys
import subprocess
from typing import Union

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QIcon, QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (QWidget, QApplication, QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy,
                               QFileDialog, QLabel, QButtonGroup)
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, LineEdit, PushSettingCard, PushButton, InfoBar, InfoBarPosition,
                            isDarkTheme, OptionsSettingCard, OptionsConfigItem, OptionsValidator, ExpandSettingCard,
                            FluentIconBase, RadioButton, qconfig)
from qframelesswindow import FramelessWindow
from qfluentwidgets import FluentIcon as FIF
from libs import translate, spawnDict


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow, FramelessWindow):
    OriginDir: str
    TranslatedDir: str
    LangDir: str
    OutputDir: str
    setting: dict

    def __init__(self):
        super().__init__()

        with open(os.path.abspath('setting.json'), 'r', encoding='utf-8') as fp:
            self.setting = json.load(fp)

        # create sub interface
        self.generateInterface = QWidget(self)
        self.generateInterface.setObjectName('Generate Interface')
        self.generateInterface.setMinimumSize(500, 500)
        self.translateInterface = QWidget(self)
        self.translateInterface.setObjectName('Translate Interface')
        self.translateInterface.setMinimumSize(500, 500)

        self.settingInterface = QWidget(self)
        self.settingInterface.setObjectName('Setting Interface')
        self.settingInterface.setMinimumSize(500, 500)

        # Generate Interface
        self.verticalLayout = QVBoxLayout(self.generateInterface)
        self.OriginFolderCard = PushSettingCard("选择文件夹", FIF.FOLDER, "游戏原文件", parent=self.generateInterface)
        self.TranslatedFolderCard = PushSettingCard("选择文件夹", FIF.FOLDER, "游戏翻译文件", parent=self.generateInterface)
        self.verticalLayout.addWidget(self.OriginFolderCard)
        self.verticalLayout.addWidget(self.TranslatedFolderCard)

        self.HorizontalWidget = QWidget(self.generateInterface)
        self.verticalLayout.addWidget(self.HorizontalWidget)
        self.HorizontalLayout = QHBoxLayout(self.HorizontalWidget)
        self.GenerateButton = PushButton(self.HorizontalWidget)
        self.GenerateButton.setText('生成')
        self.GenerateButton.setMinimumSize(40, 20)
        self.HorizontalLayout.addWidget(self.GenerateButton)

        self.HorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.HorizontalLayout.addItem(self.HorizontalSpacer)

        self.DictFolderCard = PushSettingCard("打开文件夹", FIF.FOLDER, "对照字典", parent=self.generateInterface)
        self.verticalLayout.addWidget(self.DictFolderCard)

        self.VerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.verticalLayout.addItem(self.VerticalSpacer)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 5)

        # Translate Interface
        self.verticalLayout1 = QVBoxLayout(self.translateInterface)
        self.langFolderCard = PushSettingCard(self.tr("选择文件夹"), FIF.FOLDER, self.tr("游戏语言文件夹"),
                                              parent=self.translateInterface)
        self.verticalLayout1.addWidget(self.langFolderCard)
        self.outputFolderCard = PushSettingCard(self.tr("选择文件夹"), FIF.FOLDER, self.tr("输出文件夹"),
                                                parent=self.translateInterface)
        self.verticalLayout1.addWidget(self.outputFolderCard)

        self.HorizontalWidget1 = QWidget(self.translateInterface)
        self.verticalLayout1.addWidget(self.HorizontalWidget1)
        self.HorizontalLayout1 = QHBoxLayout(self.HorizontalWidget1)
        self.TranslateButton = PushButton(self.HorizontalWidget1)
        self.TranslateButton.setText(self.tr('生成'))
        self.TranslateButton.setMinimumSize(40, 20)
        self.HorizontalLayout1.addWidget(self.TranslateButton)

        self.HorizontalSpacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.HorizontalLayout1.addItem(self.HorizontalSpacer1)
        self.VerticalSpacer1 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.verticalLayout1.addItem(self.VerticalSpacer1)

        self.verticalLayout1.setStretch(0, 1)
        self.verticalLayout1.setStretch(1, 1)
        self.verticalLayout1.setStretch(2, 1)
        self.verticalLayout1.setStretch(3, 6)

        # setting interface
        # self.verticalLayout2 = QVBoxLayout(self.settingInterface)
        # print(list(self.setting['lang'].keys()))
        # self.langOptionsCard = Sett(
        #     configItem=cfg.languageOption,
        #     texts=list([value['Text'] for value in self.setting['lang'].values()]),
        #     icon=FIF.LANGUAGE,
        #     title=self.tr('语言'),
        #     parent=self.settingInterface
        # )
        # self.verticalLayout2.addWidget(self.langOptionsCard)
        # # themeMode = OptionsConfigItem("Window", "ThemeMode", "Light", OptionsValidator(["Light", "Dark", "Auto"]),
        # #                               restart=True)
        # # self.themeOptionsCard = OptionsSettingCard(
        # #     themeMode,
        # #     FIF.BRUSH,
        # #     self.tr("主题"),
        # #     self.setting['theme'],
        # #     parent=self.settingInterface
        # # )
        # # self.verticalLayout2.addWidget(self.themeOptionsCard)
        # self.VerticalSpacer2 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.verticalLayout2.addItem(self.VerticalSpacer2)
        #
        # self.verticalLayout2.setStretch(0, 1)
        # self.verticalLayout2.setStretch(1, 1)
        # self.verticalLayout2.setStretch(2, 5)

        self.initNavigation()
        self.initWindow()
        self.initButton()

    def initNavigation(self):
        self.addSubInterface(self.generateInterface, FIF.DOCUMENT, self.tr('生成'))
        self.addSubInterface(self.translateInterface, FIF.SYNC, self.tr('翻译'))
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)

        self.navigationInterface.addSeparator()

    def initWindow(self):
        self.resize(800, 200)
        # self.setWindowIcon(QIcon(':logo.png'))
        self.setWindowTitle('LocalizationUpdateTool for Umamusume')

        rect = QGuiApplication.primaryScreen().geometry()
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def initButton(self):
        self.OriginFolderCard.clicked.connect(self.setOriginFolder)
        self.TranslatedFolderCard.clicked.connect(self.setTranslatedFolder)
        self.DictFolderCard.clicked.connect(self.openDictFolder)
        self.GenerateButton.clicked.connect(self.generateDict)
        self.langFolderCard.clicked.connect(self.setLangFolder)
        self.outputFolderCard.clicked.connect(self.setOutputFolder)
        self.TranslateButton.clicked.connect(self.Translate)

    def setOriginFolder(self):
        self.OriginDir = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"), "./")
        self.OriginFolderCard.setContent(self.OriginDir)

    def setTranslatedFolder(self):
        self.TranslatedDir = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"), "./")
        self.TranslatedFolderCard.setContent(self.TranslatedDir)

    @staticmethod
    def openDictFolder():
        os.startfile(os.path.abspath('source_file/dict'))

    def generateDict(self):
        if hasattr(self, 'OriginDir') and hasattr(self, 'TranslatedDir'):
            spawnDict(self.OriginDir, self.TranslatedDir)
        else:
            self.createErrorBar(self.tr('参数错误'), self.tr('请检查游戏原文件与游戏翻译文本的路径'))

    def setLangFolder(self):
        self.LangDir = QFileDialog.getExistingDirectory(self, self.tr("选择文件夹"), "./")
        self.langFolderCard.setContent(self.LangDir)

    def setOutputFolder(self):
        self.OutputDir = QFileDialog.getExistingDirectory(self, self.tr("选择文件夹"), "./")
        self.outputFolderCard.setContent(self.OutputDir)

    def Translate(self):
        if hasattr(self, 'LangDir'):
            if hasattr(self, 'OutputDir'):
                translate(self.LangDir, self.OutputDir)
            else:
                translate(self.LangDir, os.path.abspath('source_file/output'))
        else:
            self.createErrorBar(self.tr('参数错误'), self.tr('请检查游戏文件路径'))

    def createErrorBar(self, title: str, content: str):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=False,
            duration=2000,
            position=InfoBarPosition.BOTTOM_RIGHT,
            parent=self
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/theme/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
