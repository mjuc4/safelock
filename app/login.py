# -*- coding: utf-8 -*-
import sys
from PySide import QtCore, QtGui
from __init__ import *
from login import *
import datetime

users = {"dhtpwjd":"60142301","rkalstjr":"60132633","wkdtjsgn":"60152233","gksdnwn":"60155355","ghdgywjd":"60152258"}

#now = datetime.datetime.now()
#start_time = now.replace(hour=4, minute=0, second=0, microsecond=0)
#end_time = now.replace(hour=23, minute=0, second=0, microsecond=0)

class Example(QtGui.QWidget):

    def __init__(self):
     super(Example, self).__init__()
    
     
     self.setWindowTitle("safelock ")
     self.resultsBox = QtGui.QTextEdit()
     self.resultsBox.setReadOnly(True)
  
     self.startBox = QtGui.QLineEdit()
     self.startBox.setPlaceholderText(u'아이디')
     self.endBox = QtGui.QLineEdit()
     self.endBox.setPlaceholderText(u'비밀번호')


     self.searchButton = QtGui.QPushButton(u'로그인')
     self.searchButton.clicked.connect(self.runSearch)

     layout = QtGui.QGridLayout(self)
     layout.addWidget(self.resultsBox, 0, 0, 1, 2)
     layout.addWidget(self.startBox, 1, 0)
     layout.addWidget(self.endBox, 1, 1)

     layout.addWidget(self.searchButton, 1, 3)

     btn2 = QtGui.QPushButton(u"도움말", self)
     btn2.move(400, 150)
     btn2.clicked.connect(self.helpUser)

    def helpUser(self):
        Amsg = u"<center>도움말"
        Amsg += u"파일 또는 디렉토리 암호화 프로그램입니다"
        Amsg += u"암호화 하고자 하는 파일 또는 디렉토리를 마우스로 드래그 앤 드랍하세요  <br><br>"
        Amsg += u"암호화 진행 시 비밀 번호를 2번 입력하여 설정 합니다  "
        Amsg += u"암호화가 완료된 파일 또는 디렉토리는 .sid파일로 저장이되며  "
        Amsg += u"해당 파일 또는 디렉토리를 다시 복구시키고자 하면 입력해 두었던 비밀 번호를 재입력하세요 "
        Amsg += u"해당 프로그램 사용 가능 시간은 오전 4시 부터 오후 11시까지 입니다 "
        QMessageBox.about(self,
                          u"도움말",
                          Amsg
                          )
        return True



    def runSearch(self):
     global users
     ida = self.startBox.text()
     pwa = self.endBox.text()

     self.resultsBox.clear()
     self.resultsBox.append('Name: %s' % ida)
     self.resultsBox.append('PassWord: %s' % pwa)

     #if start_time < now and end_time > now:
     if not ida in users:
             results = u'로그인 실패'
             self.resultsBox.append(results)
     elif users[ida]==pwa:
             results = u'로그인 성공'
             self.resultsBox.append(results)

             example = Example()
             self.close()

             guia()

     else:
             results = u"로그인 실패"
             self.resultsBox.append(results)
     #else:
     #    results = u'현재 시간에는 프로그램을 이용 할 수 없습니다'
     #    self.resultsBox.append(results)



def guia():
        window = SafeLock()
        window.show()
        
        exec_()
