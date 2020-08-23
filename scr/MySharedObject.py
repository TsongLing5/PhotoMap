from PyQt5.QtCore import  QObject
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QWidget,QMessageBox

class MySharedObject(QWidget):
    def __init__(self,strval = '100'):
        super(MySharedObject,self).__init__()
        self.strval = strval
    def _getStrValue(self):
        return self.strval
    def _setStrValue(self,str):
        self.strval = str
        print('获得页面参数：%s'% str)
        QMessageBox.information(self,"Infomation", '获得的页面参数%s' % str)
    #需要定义的对外发布的方法
    strValue= pyqtProperty(str,_getStrValue,_setStrValue)