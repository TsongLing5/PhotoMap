import exifread
import re
import json
import requests
from PyQt5.uic.properties import QtWidgets
from coord_convert.transform import wgs2gcj, wgs2bd, gcj2wgs, gcj2bd, bd2wgs, bd2gcj
from PyQt5.QtWidgets import QPushButton,QTextEdit,QApplication,QWidget,QLineEdit,QLabel,QFileDialog,QRadioButton,QButtonGroup
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
from scr import html, sss
# import html.py


'''code is not good and not '''

global folderpath,phoFormat
global mapLayer

baseSet=20
opAPP = QApplication(sys.argv)
opwindows=QWidget()

pathLab=QLabel(opwindows)
path=QLineEdit(opwindows)
choiceButton=QPushButton(opwindows)

path.setEnabled(True)
formatLabel=QLabel(opwindows)
formatLE=QLineEdit(opwindows)


startButton=QPushButton(opwindows)
fileDialog=QFileDialog(opwindows)

standerLayer=QRadioButton('标准图',opwindows)
satelliteLayer = QRadioButton('卫星图',opwindows)

bg=QButtonGroup(opwindows)

mapWindows = QWidget()
web = QWebEngineView(mapWindows)
web.setHtml(html.mapsFrame)


# print(phoFormat)
def ppprint():
    global folderpath
    directory = fileDialog.getExistingDirectory(None, "getExistingDirectory", "./")
    folderpath=directory
    path.setText(directory)




def showMap():
    global folderpath,phoFormat,mapLayer
    # opwindows.close()
    # sys.exit(opAPP.exec_())
    # mapAPP= QApplication(sys.argv)
    print(folderpath)
    mapLayer = 'stander'
    if(bg.checkedId()==0):
        mapLayer='stander'
    else:
        mapLayer = 'satellite'
    print(mapLayer)
    phoFormat = formatLE.text()
    phoFormat = '.'+phoFormat
    print(phoFormat)
    pef = sss.getPic(folderpath,phoFormat)
    # print(pef)
    gps = sss.getGPSInfo(folderpath,pef)
    print(bg.checkedId())
    # print(gps)
    if(gps):
        arr = sss.buildGPSArry(gps)
        # print(arr)
        h = html.mapsFrame
        h = h.replace("var markerArr = [];", arr)
        # print(arr)
        baseloction="var lon={0},lat={1}; ".format(gps[0][1],gps[0][0])
        print(baseloction)
        h=h.replace("var lon=113,lat=22;",baseloction)
        if(mapLayer=='satellite'):
            h=h.replace("layers: [new AMap.TileLayer()],","layers: [new AMap.TileLayer.Satellite()],")
        else:
            pass

        web.setHtml(h)
        mapWindows.show()
        mapWindows.setWindowTitle("PhotoMap")
        mapWindows.showMaximized()
        web.setGeometry(0,0,mapWindows.geometry().width() ,mapWindows.geometry().height() )
        mapWindows.setFixedSize(mapWindows.geometry().width(), mapWindows.geometry().height())  # fix windows max
    # sys.exit(mapAPP.exec_())
    # mywindows.showMaximized()
    # web.setGeometry(0, 0, mywindows.geometry().width(), mywindows.geometry().height())





pathLab.move(10,60+baseSet)
opwindows.resize(600,180)
path.setMaxLength(300)
path.resize(400,20)
path.move(50,60+baseSet)

formatLabel.move(10,30+baseSet)
formatLE.move(50,30+baseSet)
formatLE.resize(60,20)

choiceButton.move(470,52+baseSet)

startButton.move(250,100+baseSet)

satelliteLayer.move(90,0+baseSet)
standerLayer.move(20,0+baseSet)


bg.addButton(standerLayer,0)
bg.addButton(satelliteLayer,1)

standerLayer.setChecked(True)

pathLab.setText("路径：")
formatLabel.setText('格式：')
startButton.setText("显示地图")
opwindows.setWindowTitle("Maps")
choiceButton.setText("选择")
formatLE.setText("jpg")
choiceButton.clicked.connect(ppprint)
startButton.clicked.connect(showMap)

opwindows.show()
opwindows.setWindowTitle("Options")
sys.exit(opAPP.exec_())
