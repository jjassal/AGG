#!/usr/bin/env python
#coding:utf-8

#UI libs
import sys
from PyQt4 import QtCore,QtGui,QtWebKit,QtNetwork
from ui import Ui_Form
from os.path import exists
#from threadproxy import startServer

#For requests Auth
import requests
import hashlib
import random

#proxy libs
import SocketServer
from threading import Thread,RLock
import pdb
import logging
import collections
from urlparse import urlparse
import socket
import re
from simplejson.decoder import JSONDecodeError
def startServer(userkey,port,ua,req_cookie,set_cookie,**kwargs):
    
    
    class CaseInsensitiveDict(collections.MutableMapping):
        def __init__(self, data=None, **kwargs):
            self._store = dict()
            if data is None:
                data = {}
            self.update(data, **kwargs)
    
        def __setitem__(self, key, value):
            # Use the lowercased key for lookups, but store the actual
            # key alongside the value.
            self._store[key.lower()] = (key, value)
    
        def __getitem__(self, key):
            return self._store[key.lower()][1]
    
        def __delitem__(self, key):
            del self._store[key.lower()]
    
        def __iter__(self):
            return (casedkey for casedkey, mappedvalue in self._store.values())
    
        def __len__(self):
            return len(self._store)
    
        def lower_items(self):
            """Like iteritems(), but with all lowercase keys."""
            return (
                (lowerkey, keyval[1])
                for (lowerkey, keyval)
                in self._store.items()
            )
    
        def __eq__(self, other):
            if isinstance(other, collections.Mapping):
                other = CaseInsensitiveDict(other)
            else:
                return NotImplemented
            # Compare insensitively
            return dict(self.lower_items()) == dict(other.lower_items())
    
        # Copy is required
        def copy(self):
            return CaseInsensitiveDict(self._store.values())
    
        def __repr__(self):
            return str(dict(self.items()))
    
    
    class Handler(SocketServer.StreamRequestHandler):
        def handle(self):
            # try:
            # pdb.set_trace()
            self.raw_requestline = self.rfile.readline() 
            if not self.raw_requestline:
                return        
            logging.info("RAW_REQYEST"+self.raw_requestline)
            self.method=self.raw_requestline.split(" ")[0]
            self.requestline=self.raw_requestline.split(" ")[1]
            logging.info("REQUEST"+self.requestline)
            r=urlparse(self.requestline)
            
            self.p2sSock=socket.socket()
            self.p2sSock.connect((r.netloc,80))
            self.pwfile=self.p2sSock.makefile('wb',0)
            self.prfile=self.p2sSock.makefile('rb',-1)
            # if not self.raw_requestline:
            #     return
    
    
            self.headers=CaseInsensitiveDict()
            #self.header_line=''
    
            # pdb.set_trace()
            while 1:
                line=self.rfile.readline()
                if line=="\r\n":
                    break
                self.headers.update([map(lambda i: i.strip(),line.split(":",1))])  #max split ->2 ref: http://abc  2:in one line
                #self.header_line+=line
            if self.raw_requestline.find("zj_game.json")!=-1:
                self.headers.update({"User-Agent":"Mozilla/5.0 ZMTransaction/1.0"})
                self.headers.update({"X-Has-Persistent-Storage":"true","X-User-Key":self.server.userkey})
            else:
                self.headers.update({"User-Agent":self.server.ua})
              
            #if self.server.req_cookie_flag:
            if self.headers.get("Cookie") and self.server.req_cookie_flag:                
                self.headers.update({"Cookie":re.sub(cookie_pattern,self.server.req_cookie,self.headers.get("Cookie",""))})#modify cookie  self.headers.get("Cookie","")+";"+
                self.server.req_cookie_flag=0
            #print self.headers.get("Cookie")
            #self.server.req_cookie_flag=0
                # self.headers.update(*line.split(":"))
               
            self.header_line=""
            for key in self.headers.keys():
                self.header_line+=key+": "+self.headers[key]+'\r\n'
            
            # logging.info("Headers DONE")
            if self.method.upper()=="GET":
                self.data=''
            else:
                self.data=self.rfile.read(int(self.headers.get("content-length",1024)))
    
            # pdb.set_trace()
            self.real_req=self.requestline[self.requestline.find(self.headers.get("host"))+len(self.headers.get("host")):]
            # logging.info("DATA READ")
            
            # pdb.set_trace()
            self.pwfile.write(self.method+" "+self.real_req+" HTTP/1.1\r\n"+self.header_line+"\r\n"+self.data)
            print "------------------------------------"
            print "Sent:"
            print self.method+" "+self.real_req+" HTTP/1.1\r\n"+self.header_line+"\r\n"+self.data
            print "------------------------------------"
            self.pwfile.flush()
    
            if self.server.set_cookie_flag:
                self.server.set_cookie_flag=0
                self.resp_line=self.prfile.readline()
                self.resp_headers=CaseInsensitiveDict()
                while 1:
                    line=self.prfile.readline()
                    if line=="\r\n":
                        break
                    self.resp_headers.update([map(lambda i: i.strip(),line.split(":",1))])  #max split ->2 ref: http://abc  2:in one line    
                self.resp_headers.update({"Set-Cookie":self.server.set_cookie.split(",")[1]})
                self.resp_data=self.prfile.read(int(self.resp_headers.get("Content-Length",1024)))
                self.resp_header_line=""
                for key in self.resp_headers.keys():
                    self.resp_header_line+=key+": "+self.resp_headers[key]+'\r\n'                
                self.wfile.write(self.resp_line+self.resp_header_line+"\r\n"+self.resp_data)
                
            else:
                r=self.prfile.read()
                self.wfile.write(r)        
            self.wfile.flush()
    
            #actually send the response if not already done.
            # except Exception as e:
            #     print "in debug"
            #     pass
            # #     #a read or a write timed out.  Discard this connection
            #     print e.message
            #     return    
    class ThreadTCPServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
        pass    
    
    
    cookie_pattern=re.compile("PHPSESSID=(\w*)")
    server=ThreadTCPServer(("localhost",port),Handler)
    server.userkey=userkey
    server.ua=ua
    server.req_cookie=req_cookie
    server.set_cookie=set_cookie
    
    #ready to use lock
    #server.lock=RLock()
    server.req_cookie_flag=1
    server.set_cookie_flag=1
    
    server_thread=Thread(target=server.serve_forever)
    server_thread.daemon=True
    server_thread.start()




class ThreadWorker(QtCore.QThread):
    def __init__(self,userkey=None,ua=None):
        QtCore.QThread.__init__(self)
        self.userkey=userkey
        self.ua="Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a ZyngaBundleIdentifier/com.zynga.zjayakashi.0 ZyngaBundleVersion/2.9.0"     
        pass

    def start(self):
        #not run but start ?why?
        try:
            startServer(self.userkey,self.port,self.ua,self.req_cookie,self.set_cookie)
        except socket.error:
            self.emit(QtCore.SIGNAL("socketerror"))
        pass

class AuthHelper():
    req0_seq='''
{
  "signedParams": {
    "zySnid": "0",
    "zyUid": "0",
    "zySnuid": "0",
    "zySig": "0"
  },
  "transactions": {
    "0": {
      "authHash": "%s",
      "params": {},
      "functionName": "MobileGameController.init",
      "sequence": "0"
    },
    "1": {
      "authHash": "%s",
      "params": {
        "localizationVersions": {
          "locale": "zh-Hans"
        },
        "remote_notification_badges": false,
        "remote_notification_alerts": false
      },
      "functionName": "MobileUserController.initUser",
      "sequence": "1"
    }
  },
  "headers": {
    "device_name": "iPhone",
    "batch_format_version": "1",
    "device_model": "iPhone5,2",
    "os_version": "7.0.4",
    "userKey": "%s",
    "device_family": "ios",
    "locale": "zh-Hans",
    "batch_sequence": "1",
    "bundle_version": "2.8.0",
    "device_type": "1",
    "bundle_identifier": "com.zynga.zjayakashi.0"
  }
}'''
    req1_seq='''{"signedParams":{"zySnid":"0","zyUid":"0","zySnuid":"0","zySig":"0"},"transactions":{"1":{"authHash":"%s","params":{"localizationVersions":{"locale":"zh-Hans"},"remote_notification_badges":false,"remote_notification_alerts":false},"functionName":"MobileUserController.initUser","sequence":"1"}},"headers":{"device_name":"iPhone","batch_format_version":"1","device_model":"iPhone5,2","os_version":"7.0.4","userKey":"%s","device_family":"ios","locale":"zh-Hans","batch_sequence":"1","bundle_version":"2.8.0","device_type":"1","bundle_identifier":"com.zynga.zjayakashi.0"}}'''
    
    
    @staticmethod
    def authRequest(user_key):
        def generateMd5():
            return hashlib.new("md5",str(random.random())).hexdigest()


        req0=AuthHelper.req0_seq%(generateMd5(),generateMd5(),user_key)
        #print req0
        try:
            resp0=requests.post("http://zc2.ayakashi.zynga.com/zj_game.json?authentication=none&manager=shared", data=req0,headers={"User-Agent":"Mozilla/5.0 ZMTransaction/1.0","X-User-Key":user_key})
        # print resp0.content
            if resp0.content.find('"Status":"OK"'):
                req1=AuthHelper.req1_seq%(generateMd5(),user_key)
                resp1=requests.post("http://zc2.ayakashi.zynga.com/zj_game.json?authentication=none&manager=shared", data=req1,headers={"User-Agent":"Mozilla/5.0 ZMTransaction/1.0","X-User-Key":user_key})
                # print resp1.content
                if resp1.json().get(u"responses")  and resp1.json().get(u"responses").get(u"1") and  resp1.json().get(u"responses").get(u"1").get(u"ZJSESSIONID"):
                    zjsessionid=str(resp1.json().get(u"responses").get(u"1").get(u"ZJSESSIONID"))
                    resp3=requests.get("http://zc2.ayakashi.zynga.com/app.php?_c=ZJLogin&action=GetCookie&next=Entry.start&ZJSESSIONID="+zjsessionid,headers={"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a ZyngaBundleIdentifier/com.zynga.zjayakashi.0 ZyngaBundleVersion/2.9.0"})
                    return [resp3.request.headers.get("cookie",""),resp3.history[0].headers.get("set-cookie","")]
        except JSONDecodeError:
            pass
        except (requests.RequestException,requests.ConnectionError,requests.HTTPError):
            pass
        except socket.error:
            pass


        return ["",""] #For QStringList
                

class GetUserKeyWorker(QtCore.QThread):

    def run(self):
        self.userkey_pattern=re.compile(r'X-User-Key: (\w*)',re.I)        
        try:
            uSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            uSocket.bind(("0.0.0.0",self.port))  #all interface!
            uSocket.listen(1)
            while 1:
                (recvSocket,_)=uSocket.accept()
                raw=recvSocket.recv(65536)
                result=self.userkey_pattern.findall(raw)
                if result:
                    self.emit(QtCore.SIGNAL("GetUserKey(QString)"),result[0])                
                    break
            uSocket.close()
        except socket.error:
            self.emit(QtCore.SIGNAL("socketerror()"))
        except OverflowError:
            #wait to do something
            pass
        pass
    


class ValidateWorker(QtCore.QThread):
    def __init__(self,userkey):
        QtCore.QThread.__init__(self)
        self.userkey=userkey
        pass
    
    def run(self):
        result=AuthHelper.authRequest(self.userkey)
        self.emit(QtCore.SIGNAL("validate(QStringList)"),result)

class MainWindow(QtGui.QWidget):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)

        self.settings=QtCore.QSettings('./settings.ini',QtCore.QSettings.IniFormat)
        if not exists("./settings.ini"):
            self.settings.setValue("PORT",12345)
        self.settings.sync()#to create the ini file


        self.ui=Ui_Form()
        self.ui.setupUi(self)
        #read config ->userkey ->ua

        self.ui.Button_USERKEY.clicked.connect(self.on_Button_USERKEY_Clicked)
        self.ui.Button_GETKEY.clicked.connect(self.on_Button_GETKEY_Clicked)
        #self.ui.LineEdit_USERKEY.setText("86cbb0f770854622874dd3222cb6243c")
        self.worker=ThreadWorker() #Key
        self.connect(self.worker,QtCore.SIGNAL("socketerror()"),self.afterSocketError)

        
        self.userkey=self.settings.value("USERKEY")
        self.ui.LineEdit_USERKEY.setText(self.userkey.toString())
        
        self.show()
        self.port=self.settings.value("PORT").toInt()[0]
        if not 1024<self.port<65535:
            self.port=12345
            QtGui.QMessageBox.critical(self,u"错误" ,u"端口号必须在1024~65535之间\n现在强制设置为12345\n如需更改请重新设置settings.ini的PORT")
            #how to quit?
            pass 
        

    def on_Button_GETKEY_Clicked(self):
        self.ui.Button_GETKEY.setEnabled(False)
        self.ui.Button_USERKEY.setEnabled(False)
        self.ui.Label_INFO.setText(u"正在监听端口"+str(self.port))
        self.getuserkeyworker=GetUserKeyWorker()
        self.getuserkeyworker.port=self.port
        self.getuserkeyworker.start()
        self.connect(self.getuserkeyworker,QtCore.SIGNAL("GetUserKey(QString)"),self.afterGetUserKey)
        self.connect(self.getuserkeyworker,QtCore.SIGNAL("socketerror()"),self.afterSocketError)
        
        pass

    def on_Button_USERKEY_Clicked(self):
        if not self.ui.LineEdit_USERKEY.text().isEmpty():
            self.ui.LineEdit_USERKEY.setEnabled(False)

            self.ui.Label_INFO.setText(u"验证账号中")
            self.ui.Button_USERKEY.setEnabled(False)
            self.ui.Button_GETKEY.setEnabled(False)
            self.validateworker=ValidateWorker(self.ui.LineEdit_USERKEY.text())
            self.validateworker.start()
            self.connect(self.validateworker,QtCore.SIGNAL("validate(QStringList)"),self.afterValidate)
    
    def afterGetUserKey(self,userkey):
        self.ui.LineEdit_USERKEY.setText(userkey)
        # self.ui.Button_USERKEY.click()
        self.on_Button_USERKEY_Clicked()
        pass

    def afterValidate(self,stringList):
        self.req_cookie=str(stringList[0])
        self.set_cookie=str(stringList[1])
        print self.req_cookie
        print self.set_cookie
        
        if self.set_cookie=="" or self.req_cookie=="":
            self.ui.Label_INFO.setText(u"验证失败")
            self.ui.Button_USERKEY.setEnabled(True)
            self.ui.Button_GETKEY.setEnabled(True)
            self.ui.LineEdit_USERKEY.setEnabled(True)
        else:
            self.ui.Label_INFO.setText(u"验证完毕")
            self.settings.setValue("USERKEY",self.ui.LineEdit_USERKEY.text())
            self.worker.userkey=self.ui.LineEdit_USERKEY.text()
            self.worker.req_cookie=self.req_cookie
            self.worker.set_cookie=self.set_cookie
            self.worker.port=self.port
            self.worker.start()
            self.ui.Label_INFO.setText(u"正在监听 127.0.0.1:"+str(self.port))
            self.ui.LineEdit_USERKEY.setEnabled(True)

    def afterSocketError(self):
        QtGui.QMessageBox.warning(u"Socket连接异常，请检查网络或换一个端口")
        self.ui.Button_USERKEY.setEnabled(True)
        self.ui.Button_GETKEY.setEnabled(True)



if __name__=="__main__":
    #AuthHelper.authRequest("86cbb0f770854622874dd3222cb6243c")
    app=QtGui.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon("icon.png"))
    w=MainWindow()
    sys.exit(app.exec_())
    