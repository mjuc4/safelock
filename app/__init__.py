# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import division
from PySide.QtGui import QApplication, QLabel, QWidget, QMessageBox
from PySide.QtGui import QStatusBar, QProgressBar, QPushButton
from PySide.QtGui import QVBoxLayout, QHBoxLayout, QFileDialog
from PySide.QtGui import QDesktopWidget, QInputDialog, QLineEdit
from PySide.QtGui import QIcon, QFont, QPixmap
from PySide.QtCore import Qt, Slot, QEvent, QUrl
from sys import exit, platform, argv
from os import name, system, path, remove, listdir
from sys import platform as sysname
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Binary, Unicode
from sqlalchemy.orm import sessionmaker
from threads import EncryptTH, DecryptTH
from ex_functions import encryptit, isenct, r_path
from hashlib import sha256
from login import *

class SafeLock(QWidget):
    def __init__(self):
        super(SafeLock, self).__init__()
        main_layout = QVBoxLayout(self)
        self.Version = '0.5 beta'
        self.s_error = "QStatusBar{color:red;font-weight:1000;}"
        self.s_loop = "QStatusBar{color:black;font-weight:1000;}"
        self.s_norm = "QStatusBar{color:blue;font-style:italic;"
        self.s_norm += "font-weight:500;}"
        self.Processing = None
        self.CP = None
        self.PPbar = None
        self.key = None
        self.DFiles = []

        self.picon = r_path("images/favicon.png")
        self.plogo = r_path("images/logo.png")
        if name == 'nt':
            self.picon = r_path("images\\favicon.png")
            self.plogo = r_path("images\\logo.png")
        self.icon = QIcon(self.picon)
        self.logo = QIcon(self.plogo)
        self.center()
        self.setStyle()
        self.setMW(main_layout)
        self.setSB(main_layout)
        self.show()

    def db(self, password="password", dbname="untitled.sld", dc=True):
        eng = create_engine("sqlite:///%s" % dbname,
                            connect_args={'check_same_thread': False})
        Base = declarative_base(bind=eng)
        Session = sessionmaker(bind=eng)
        session = Session()

        class Identifier(Base):
            __tablename__ = "identifier"
            id = Column(Integer, primary_key=True)
            version = Column(Binary)
            kvd = Column(Binary)

            def __init__(self, version, kvd):
                self.id = 0
                self.version = version
                self.kvd = kvd

        class Folder(Base):
            __tablename__ = 'folders'
            id = Column(Integer, primary_key=True)
            path = Column(Unicode)

            def __init__(self, path="Empty"):
                self.path = path

        class File(Base):
            __tablename__ = 'files'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            f_id = Column(Integer, ForeignKey('folders.id'), nullable=True)
            bb = Column(Binary)

            def __init__(self, name="empty", f_id=0, bb=1010):
                self.name = name
                self.f_id = f_id
                self.bb = bb
        if dc:
            Base.metadata.create_all()
            enc = encryptit(sha256(self.Version).digest(),
                            sha256(password).digest())
            session.add(Identifier(enc[0], enc[1]))
            session.commit()

        return [eng, Base, session, File, Folder, Identifier, password]

    def checkP(self, db):
        try:
            d = db[2].query(db[5]).filter_by(id=0).first()
            if d is not None:
                if isenct(self.Version, d.version, db[6], d.kvd):
                    return True
        except:
            pass
        return False

    def setStyle(self):
        self.setMaximumWidth(410)
        self.setMinimumWidth(410)
        self.setMaximumHeight(370)
        self.setMinimumHeight(370)
        self.setWindowIcon(self.icon)
        self.activateWindow()
        self.setWindowTitle("safelock " + self.Version)
        self.setToolTip(
            u"단순히 끌어다 놓는 것으로 파일이나 폴더를 암호화하거나" +
            u" .sld 파일을 복호화할 수 있습니다.")
        self.setAcceptDrops(True)
        self.show()

    def center(self):
        qrect = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qrect.moveCenter(cp)
        self.move(qrect.topLeft())

    def setMW(self, ml):
        ll = QVBoxLayout()
        self.mIcon = QLabel()
        self.mIcon.setAlignment(Qt.AlignCenter)
        mmicon = self.logo.pixmap(250, 230, QIcon.Active, QIcon.On)
        self.mIcon.setPixmap(mmicon)
        self.mInst = QLabel(
         #   u"<center>(Drag and drop files or folders to encrypt them)<br>" +
            u"<center>(마우스로 끌어다 놓으십시오)<br>" +
            u"<u>최대 2GB 파일 또는 디렉토리만 가능</u></center>")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.fInst = QLabel('<center></center>')
        self.mInst.setFont(font)
        ll.addWidget(self.mIcon)
        ll.addWidget(self.mInst)
        ll.addWidget(self.fInst)
        ml.addLayout(ll)

    def setSB(self, ml):
        self.statusb = QStatusBar()
        ml.addWidget(self.statusb)

    def modSB(self):
        if self.PPbar is None:
            self.PPbar = True
            self.statusb.clear()
            self.pbar = QProgressBar()
            self.pbar.setMaximum(100)
            self.pbar.setMinimum(0)
            self.plabel = QLabel()
            self.statusb.addWidget(self.plabel, 0.5)
            self.statusb.addWidget(self.pbar, 3)
        else:
            self.PPbar = None
            self.statusb.removeWidget(self.plabel)
            self.statusb.removeWidget(self.pbar)
            self.statusb.clear()

    # def searchF(self, dirname):
    #     filelist = []
    #     try:
    #         filenames = listdir(dirname)
    #         for filename in filenames:
    #             full_filename = path.join(dirname, filename)
    #             if path.isdir(full_filename):
    #                 tmplist = self.searchF(full_filename)
    #                 for tmpfile in tmplist:
    #                     filelist.append(tmpfile)
    #             else:
    #                 tmp = full_filename.replace('\\','/')
    #                 filelist.append(tmp)
    #     except PermissionError:
    #         pass
    #     return filelist

    def saveFile(self, fl):
        fname, _ = QFileDialog.getSaveFileName(self,
                                               u"암호화 경로 설정",
                                               fl,
                                               "Safelock file (*.sld)")
        if '.' in fname:
            tm = fname.split('.')
            tm = tm[len(tm) - 1]
            if tm == "sld":
                try:
                    if path.isfile(fname):
                        remove(fname)
                except:
                    pass
                return fname
        if len(fname) <= 0:
            return None
        fname += ".sld"
        try:
            if path.isfile(fname):
                remove(fname)
        except:
            pass
        return fname

    def extTo(self, fl):
        fname = QFileDialog.getExistingDirectory(self, u"복호화 경로 설정",
                                                 fl)
        if len(fname) <= 0:
            return None
        return fname

    def getPass(self):
        passwd, re = QInputDialog.getText(self, u"비밀번호", u"입력하신 비밀번호 :",
                                          QLineEdit.Password)
        if len(passwd) > 0 :
            passwd2, re = QInputDialog.getText(self, u"비밀번호", u"다시한번 입력하세요 :",
                                          QLineEdit.Password)
            if passwd != passwd2:
                self.errorMsg(u"비밀번호가 맞지 않습니다")
                return False
            else:
                if not re:
                    return False
                if len(passwd) <= 0:
                    return None
                return passwd
        else:
            if not re:
                return False
            else:
                return None

    def getPass2(self):
        passwd, re = QInputDialog.getText(self, u"비밀번호", u"입력하신 비밀번호 :",
                                          QLineEdit.Password)
        if not re:
            return False
        if len(passwd) <= 0:
            return None
        return passwd

    def errorMsg(self, msg=u"에러 발생 !"):
        QMessageBox.critical(self, "Error", msg)
        return True

    def aboutMsgg(self):
        Amsg = u"<center>SafeLock %s " % self.Version
        Amsg += u"은 Mozilla Public License 버전 2.0에 "
        Amsg += u"따라 허가된 무료 오픈소스 프로젝트 입니다.<br><br>"
        Amsg += u" 본 프로그램에 대한 더 많은 정보를 원하시면:<br> "
        Amsg += u"<b><a href='https://github.com/mjuc4/safelock'> "
        Amsg += u"https://github.com/mjuc4/safelock/ </a> </b></center>"
        QMessageBox.about(self, "About", Amsg)
        return True

    def getSession(self):
        self.eng = eng(self.password, self.dbname)
        Session = sessionmaker(bind=self.eng)
        self.Base = declarative_base(bind=self.eng)
        self.Base.metadata.create_all()
        self.session = Session()
        return self.session

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            self.DFiles = []
            for url in e.mimeData().urls():
                try:
                    if sysname == 'darwin':
                        from Foundation import NSURL
                        fname = NSURL.URLWithString_(
                            url.toString()).filePathURL().path()
                    else:
                        fname = url.toLocalFile()
                    self.DFiles.append(fname)
                except:
                    pass
            self.dealD(self.DFiles)
        else:
            event.ignore()

    def in_loop(self):
        if self.Processing is None:
            self.Processing = True
            self.setAcceptDrops(False)
            self.mIcon.setEnabled(False)
            self.mInst.setEnabled(False)
            self.fInst.setText(u"<center>| 취소는 더블 클릭 |</center>")
            self.setToolTip("Double-Click anywhere to cancel")
        else:
            self.Processing = None
            self.setAcceptDrops(True)
            self.mIcon.setEnabled(True)
            self.mInst.setEnabled(True)
            self.fInst.setText(u"<center>| 취소는 더블 클릭 |</center>")
            self.setToolTip(
                u"단순히 끌어다 놓는 것으로 파일이나 폴더를 암호화하거나" +
                u" .sld 파일을 복호화할 수 있습니다.")

    def dealD(self, files):
        def tpp(inp):
            a = path.basename(inp)
            return inp.replace(a, '')
        if len(files) < 1:
            return False
        elif len(files) >= 1:
            if len(files) == 1:
                tf = files[0].split('.')
                tf = tf[len(tf) - 1]
                if tf == 'sld':
                    pw = self.getPass2()
                    if pw is None:
                        self.errorMsg(u"비밀번호 입력하십쇼!")
                        return False
                    elif not pw:
                        return False
                    if not self.checkP(self.db(sha256(pw).digest(), files[0],
                                               dc=False)):
                        self.errorMsg(
                            u"비밀번호가 맞지 않습니다. 다시 시도하세요")
                        return False
                    else:
                        fold = self.extTo(tpp(files[0]))
                        if fold is not None:
                            self.CP = fold
                            self.in_loop()
                            self.P = DecryptTH(fold, self.db(pw,
                                                             files[0],
                                                             dc=False),
                                               sha256(pw).digest())
                            self.P.start()
                            self.P.somesignal.connect(self.handleStatusMessage)
                            self.P.setTerminationEnabled(True)
                            return True
            pw = self.getPass()
            if pw is None:
                self.errorMsg(u"비밀번호 입력하십시오 !")
            elif not pw:
                pass
            else:
                fil = self.saveFile(tpp(files[0]))
                if fil is not None:
                    if path.isfile(fil):
                        try:
                            remove(fil)
                        except:
                            pass
                    self.CP = fil
                    self.in_loop()
                    self.P = EncryptTH(files, self.db(pw, fil),
                                       sha256(pw).digest())
                    self.P.start()
                    self.P.somesignal.connect(self.handleStatusMessage)
                    self.P.setTerminationEnabled(True)
        return True

    @Slot(object)
    def handleStatusMessage(self, message):
        self.statusb.setStyleSheet(self.s_loop)

        def getIT(f, o):
            return int((f / o) * 100)
        mm = message.split('/')
        if mm[len(mm) - 1] == '%':
            if self.PPbar is None:
                self.modSB()
            self.pbar.setValue(getIT(int(mm[0]), int(mm[1])))
            self.setWindowTitle("Processing : " + str(getIT(int(mm[0]),
                                                            int(mm[1]))) + "%")
            self.plabel.setText(mm[0] + '/' + mm[1])
        else:
            self.unsetCursor()
            if self.PPbar is not None:
                self.modSB()
            if message[:7] == '# Error':
                if self.Processing:
                    self.in_loop()
                self.statusb.setStyleSheet(self.s_error)
                self.cleanup()
            elif message[:6] == '# Stop':
                self.statusb.setStyleSheet(self.s_error)
            elif message[:6] == '# Done':
                if self.Processing:
                    self.in_loop()
                self.statusb.setStyleSheet(self.s_norm)
                if message.find('encrypted')>=0 :
                    QMessageBox.question(None,'success',"Encrypted succes")
                else:    
                    QMessageBox.question(None,'success',"Decrypted succes")
            elif message == "# Loading":
                self.setCursor(Qt.BusyCursor)
                self.statusb.setStyleSheet(self.s_norm)
            self.setWindowTitle('safelock ' + self.Version)
            self.statusb.showMessage(message)

    def mousePressEvent(self, event):
        if event.type() == QEvent.Type.MouseButtonDblClick:
            if self.Processing is None:
                self.aboutMsgg()
            else:
                self.closeEvent()

    def closeEvent(self, event=None):
        if self.Processing is not None:
            if event is not None:
                r = QMessageBox.question(
                    self,
                    "Making sure",
                    "Are you sure you want to exit, during an active" +
                    " process ?",
                    QMessageBox.Yes | QMessageBox.No)
            else:
                r = QMessageBox.question(
                    self,
                    "Making sure",
                    "Are you sure, you to cancel ?",
                    QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.Yes:
                self.P.stop()
                self.cleanup()
                if event is not None:
                    self.in_loop()
                    event.accept()
                else:
                    self.in_loop()
            else:
                if event is not None:
                    event.ignore()
        else:
            if self.CP is not None:
                try:
                    if path.isfile(self.CP + '-journal'):
                        remove(self.CP + '-journal')
                except:
                    pass
            if event is not None:
                event.accept()

    def cleanup(self):
        if self.CP is not None:
            try:
                if path.isfile(self.CP + '-journal'):
                    remove(self.CP + '-journal')
                if path.isfile(self.CP):
                        remove(self.CP)
            except:
                pass


def gui():
    app = QApplication(argv)
    example = Example()
    example.show()

    app.exec_()
