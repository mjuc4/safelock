# -*- coding: cp949 -*-
import sys
from PySide import QtCore, QtGui
from __init__ import *
from login import *
import datetime

users = {"dhtpwjd":"60142301","rkalstjr":"60132633","wkdtjsgn":"60152233","gksdnwn":"60155355","ghdgywjd":"60152258"}

now = datetime.datetime.now()
start_time = now.replace(hour=4, minute=0, second=0, microsecond=0)
end_time = now.replace(hour=23, minute=0, second=0, microsecond=0)

class Example(QtGui.QWidget):

    def __init__(self):
     super(Example, self).__init__()
     self.setWindowTitle("safelock ")
     self.resultsBox = QtGui.QTextEdit()
     self.resultsBox.setReadOnly(True)

     self.startBox = QtGui.QLineEdit()
     self.startBox.setPlaceholderText('Insert Name')
     self.endBox = QtGui.QLineEdit()
     self.endBox.setPlaceholderText('Insert PWD')


     self.searchButton = QtGui.QPushButton('Log In')
     self.searchButton.clicked.connect(self.runSearch)

     layout = QtGui.QGridLayout(self)
     layout.addWidget(self.resultsBox, 0, 0, 1, 4)
     layout.addWidget(self.startBox, 1, 0)
     layout.addWidget(self.endBox, 1, 1)

     layout.addWidget(self.searchButton, 1, 3)





    def runSearch(self):
     global users
     ida = self.startBox.text()
     pwa = self.endBox.text()

     self.resultsBox.clear()
     self.resultsBox.append('Name: %s' % ida)
     self.resultsBox.append('PassWord: %s' % pwa)

     if start_time < now and end_time > now:
         if not ida in users:
             results = 'LogIn Fail'
             self.resultsBox.append(results)
         elif users[ida]==pwa:
             results = 'LogIn Success'
             self.resultsBox.append(results)

             example = Example()
             self.close()

             guia()

         else:
             results = "LogIn Fail"
             self.resultsBox.append(results)
     else:
         results = 'The program can not be run at this time.'
         self.resultsBox.append(results)



def guia():

        window = SafeLock()

        window.show()

        exec_()
