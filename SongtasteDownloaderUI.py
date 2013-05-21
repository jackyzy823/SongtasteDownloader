#!/usr/bin/env python
#coding:utf-8
from PyQt4 import QtCore,QtGui
import sys
from os import getenv
import os.path

class Dialog(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setWindowTitle("Ready to Down?")
        self.resize(100,100)
        buttonbox=QtGui.QDialogButtonBox(parent=self)
        buttonbox.setOrientation(QtCore.Qt.Horizontal)
#         buttonbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        buttonbox.addButton(u"确定",QtGui.QDialogButtonBox.AcceptRole)
        buttonbox.addButton(u"取消",QtGui.QDialogButtonBox.RejectRole)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        layout=QtGui.QVBoxLayout()
        layout.addWidget(buttonbox)
        self.setLayout(layout)
        


class main(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle('SongtasteDownloader')
        self.setWindowIcon(QtGui.QIcon('favicon.ico'))
        self.resize(300,250)
#         fb=QtGui.QFileDialog()
        #elements
        label1=QtGui.QLabel('Song URL or ID')
        label2=QtGui.QLabel('Path')
        
        self.line=QtGui.QLineEdit(parent=self)
        self.line2=QtGui.QLineEdit(os.path.join(getenv('USERPROFILE'),'Music'),parent=self)
        #default should be set
        
        button=QtGui.QPushButton('Down',parent=self)
        button2=QtGui.QPushButton('Browser',parent=self)
        
        self.progress=QtGui.QProgressBar(parent=self)
        
        t=QtGui.QTextBrowser()
        t.append('')
        
        #UI
        layout=QtGui.QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.line)
        layout.addWidget(label2)
        layout.addWidget(self.line2)
        layout.addWidget(button2)
        layout.addWidget(button)
        layout.addWidget(self.progress)
        layout.addWidget(t)
        self.setLayout(layout)
        
        #event listen
        button.clicked.connect(self.add)
        button2.clicked.connect(self.getPath)
        
    def add(self):
        self.line.text()
        dia=Dialog(parent=self)
        print dia.exec_()
        pass
    
    def getPath(self):
        selectfile=QtGui.QFileDialog.getExistingDirectory()
#         selectfile=QtGui.QFileDialog.directory()
        self.line2.setText(selectfile)
        

app=QtGui.QApplication(sys.argv)
qb=main()
qb.show()
sys.exit(app.exec_())