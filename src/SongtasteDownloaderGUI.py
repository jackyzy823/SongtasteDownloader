#!/usr/bin/env python
#coding:utf-8
import re
import sys
import os.path
from os import getenv
from PyQt4 import QtCore,QtGui
from base64 import decodestring
from urllib import urlopen, urlretrieve, urlencode

class Dialog(QtGui.QDialog):
    def __init__(self,parent=None,message=''):
        QtGui.QDialog.__init__(self,parent)
        infomation=QtGui.QLabel(message)
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
        layout.addWidget(infomation)
        layout.addWidget(buttonbox)
        self.setLayout(layout)
        
        
class DialogwithoutConfirm(QtGui.QDialog):
    def __init__(self,message='',title='',parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setWindowTitle(title)
        infomation=QtGui.QLabel(message)
        confirm=QtGui.QPushButton(u'确定')
        self.resize(150,100)
        layout=QtGui.QVBoxLayout()
        layout.addWidget(infomation)
        layout.addWidget(confirm)
        self.setLayout(layout)
        confirm.clicked.connect(self.close)

class Downloader(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle('SongtasteDownloader')
        self.setWindowIcon(QtGui.QIcon('favicon.ico'))
        self.resize(360,250)
#         fb=QtGui.QFileDialog()
        #elements
        label1=QtGui.QLabel(u'URL or SongID')
        label2=QtGui.QLabel(u'保存路径')
        
        self.line=QtGui.QLineEdit(parent=self)
        self.line2=QtGui.QLineEdit(os.path.join(getenv('USERPROFILE'),'Music'),parent=self)
        #default should be set
        
        button=QtGui.QPushButton(u'下载',parent=self)
        button2=QtGui.QPushButton(u'浏览',parent=self)
        
        self.progress=QtGui.QProgressBar(parent=self)
        
        self.t=QtGui.QTextBrowser()
        self.t.append('')
        
        self.check=QtGui.QCheckBox(u'下载前提示MP3文件大小')
        self.check.setChecked(True)
        
        aboutme=QtGui.QPushButton(u'About')
        #UI
#         layout=QtGui.QVBoxLayout()
#         layout.addWidget(label1)
#         layout.addWidget(self.line)
#         layout.addWidget(label2)
#         layout.addWidget(self.line2)
#         layout.addWidget(button2)
#         layout.addWidget(button)
#         layout.addWidget(self.progress)
#         layout.addWidget(t)
#         self.setLayout(layout)
#         
        #UI2
        layout=QtGui.QGridLayout()
        layout.addWidget(label1,0,0)
        layout.addWidget(self.line,0,1,1,1)
        layout.addWidget(button,0,2)
        layout.addWidget(label2,1,0)
        layout.addWidget(self.line2,1,1)
        layout.addWidget(button2,1,2)
        layout.addWidget(self.check,2,1,1,2)
        layout.addWidget(aboutme,2,2)
        layout.addWidget(self.t,3,0,1,3)
        layout.addWidget(self.progress,4,0,1,3)
        self.setLayout(layout)
        #event listen
        button.clicked.connect(self.clickTodown)
        button2.clicked.connect(self.getPath)
        aboutme.clicked.connect(self.about)
        
#path info
    def cbk(self,a,b,c):
        per = int(100.0 * a * b / c)
        self.progress.setValue(per)
        pass

    def Media(self,URL):
        URL=str(URL)
        if URL.isdigit():
            songid = URL
        else:
            songid = URL.split('/')[URL.split('/').index('song') + 1]
        mediadown = 'http://huodong.duomi.com/songtaste/?songid=' + songid
        mediapage = urlopen(mediadown).read()
        pattern = re.compile(r'http://[0-9A-Za-z/\-\.]*\.(mp3|MP3)')
        downloadURL = pattern.search(mediapage).group()
        try:
            pattern2 = re.compile('var songname = "([A-Za-z0-9\+/=]*)"')
            filename = decodestring(pattern2.search(mediapage).groups()[0])
            # filename = pattern2.search(mediapage).groups()[0].decode('base64')
        except:
            filename = decodestring(mediapage[mediapage.index(
                'var songname') + 16:mediapage.index('var url') - 16])
        filetype = downloadURL.split('.')[-1]
        Info = (downloadURL, filetype, filename)
        return Info
        
    def download(self,info,path):
        self.t.append(u'开始下载 :'+info[2])
        filepath = path + '%s' % info[2] + '.' + info[1]
        try:
            a, b = urlretrieve(info[0], filepath, self.cbk)
        except:
            DialogwithoutConfirm(title='Error',message=u"程序故障@download =w= Please Mail to jackyzy823@gmail.com")
        self.t.append(u'下载完成:'+info[2])
        
    def getSize(self,info):
        import httplib
        import urlparse
        up = urlparse.urlparse(info[0])
        httpCon = httplib.HTTPConnection(up[1])
        httpCon.request('HEAD', up[2])
        response = httpCon.getresponse()
        if response.status == 200:
            size = int(response.getheader('content-length')) / 1024.0 / 1024.0
        else:
            size = 0
        httpCon.close()
        return size
    
    def clickTodown(self):
        me=self.line.text()
        path=self.line2.text()+'\\'
        info=self.Media(me)
        if self.check.checkState()==2:
            res=Dialog(parent=self,message=u"文件大小为   %.2f MB"%self.getSize(info)).exec_()
            if res==1:
                self.download(info,path)
        else:
            #DialogwithoutConfirm(parent=None,title="Error",message=me).exec_()
            self.download(info, path)
#         print dia.exec_()
        pass
    
    def getPath(self):
        selectfile=QtGui.QFileDialog.getExistingDirectory()
#         selectfile=QtGui.QFileDialog.directory()
        if selectfile != "":
            self.line2.setText(selectfile)
    
    def about(self):
        message=u'''这是一个SongtasteDownloader\n使用链接\nhttp://www.songtaste.com/song/***** \n或 歌曲ID:*****来下载\n'''
        title=u"关于"
        DialogwithoutConfirm(message,title).exec_()
        pass
    

app=QtGui.QApplication(sys.argv)
window=Downloader()
window.show()
sys.exit(app.exec_())