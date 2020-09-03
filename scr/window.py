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
import hhtml
import sss
from PYQTObject import MyObjectCls
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
# from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebChannel import QWebChannel
from MySharedObject import  MySharedObject
import os
from PIL import Image
import subprocess
import sip
import ctypes




'''code is not good and not '''

class CallHandler(QObject):
    @pyqtSlot(result=str)
    def myHello(self):
        web.page().runJavaScript('uptext("hello, Python");')
        print('加载完成')
        return 'hello, Python'

    @pyqtSlot(str, result=str)
    def sendData2Web(self,str):
        web.page().runJavaScript('uptext(str);')
        # print('加载完成')
        return 'hello, Python'

    @pyqtSlot(str, result=str)
    def myTest(self,test):
        OS=sys.platform
        # print(test)
        # picPath='/Users/aria/Documents/PENTAX'+'/'+test.replace("相片：","")
        # print(picPath)
        # im=Image.open(picPath)
        # im.show()
        print(test.split('/')[-1])
        if(OS=="darwin"):
            subprocess.call(["open", test])
        elif(OS=="win32"):
            # self.sendData2Web('unsupported Now')
            
            print("open "+test)
            img=Image.open(test[:1]+":"+test[2:])
            img.show()
        # os.system(picPath.replace('/','//'))
        return test




folderpath=''
phoFormat=''
global mapLayer

folder = os.path.exists("Thumbnail")
if(not folder):
    os.makedirs("Thumbnail")
    print("创建Thumbnail成功")
baseSet=20
opAPP = QApplication(sys.argv)
opwindows=QWidget()

pathLab=QLabel(opwindows)
path=QLineEdit(opwindows)
if (sys.platform == "darwin"):
    path.setText('/Users/aria/Documents/PENTAX')
elif (sys.platform == "win32"):
    path.setText('W:/PENTAX2020')
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
web.setHtml(hhtml.mapsFrame)

channel=QWebChannel()
handler = CallHandler()
channel.registerObject('pyjs', handler)
web.page().setWebChannel(channel)

# # //code of qwe
# channel=QWebChannel()
# myObject=MySharedObject()
# channel.registerObject('bridge',myObject)
# web.page().setWebChannel(channel)
# print(phoFormat)
def ppprint():
    global folderpath
    directory = fileDialog.getExistingDirectory(None, "getExistingDirectory", "./")
    path.setText(directory)





def showMap():   #start map ui
    global folderpath,phoFormat,mapLayer
    folderpath = path.text()
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
    #生成缩略图
    print("生成缩略图")
    sss.creatThumb(gps)
    # print(gps)
    if(gps):
        arr = sss.buildGPSArry(gps)
        # print(arr)
        h = hhtml.mapsFrame
        h = h.replace("var markerArr = [];", arr)
        # print(arr)
        baseloction="var lon={0},lat={1}; ".format(gps[0][1],gps[0][0])
        print(baseloction)
        h=h.replace("var lon=113,lat=22;",baseloction)
        if(mapLayer=='satellite'):
            h=h.replace("layers: [new AMap.TileLayer()],","layers: [new AMap.TileLayer.Satellite()],")
        else:
            pass

        curPath = os.getcwd()
        if (sys.platform == "darwin"):  #mac OS
            url_string = "file:///" + curPath + "//maps.html"

        elif (sys.platform == "win32"):  #Windows
            url_string = "file:///" + curPath.replace("\\", "/") + "//maps.html"


        # web.setHtml(h)
        ##write html
        f = open('maps.html', 'w')
        f.write(h)
        f.close()


        web.load(QUrl(url_string))
        web.show()

        #print(h)
        mapWindows.show()
        mapWindows.setWindowTitle("PhotoMap")
        mapWindows.showMaximized()
        screenX=1920
        screenY=1080
        if (sys.platform == "win32"):
            user=ctypes.windll.user32
            screenX = user.GetSystemMetrics(0)
            screenY = user.GetSystemMetrics(1)
        elif (sys.platform == "darwin"):
            screenX=mapWindows.width()
            screenY=mapWindows.height()
        web.setGeometry(0, 0, screenX, screenY)  # set size of web
        web.setGeometry(0, 0, screenX, screenY)  # set size of web
        mapWindows.setFixedSize(screenX, screenY)  # fix windows max
    else:
        print("找不到GPS信息")
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
standerLayer.move(20,0+baseSet)   #UI set


bg.addButton(standerLayer,0)
bg.addButton(satelliteLayer,1)

standerLayer.setChecked(True)

pathLab.setText("路径：")
formatLabel.setText('格式：')
startButton.setText("显示地图")
opwindows.setWindowTitle("Maps")
choiceButton.setText("选择")
formatLE.setText("jpg")
choiceButton.clicked.connect(ppprint)  #bind click event，inject select path dialog
startButton.clicked.connect(showMap)  #bind click event




opwindows.show()
opwindows.setWindowTitle("Options")
sys.exit(opAPP.exec_())
