import SocketServer
from threading import Thread
import pdb
import logging
import pdb
import collections
from urlparse import urlparse
import socket
import re

def startServer(userkey,ua,req_cookie,set_cookie,**kwargs):
    
    
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
            else:
                self.headers.update({"User-Agent":self.server.ua})
              
            self.headers.update({"X-Has-Persistent-Storage":"true","X-User-Key":self.server.userkey})
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
            self.pwfile.write(self.method+" "+self.real_req+" HTTP/1.1\r\n"+self.header_line+"\r\n")
            # print self.method+" "+self.real_req+" HTTP/1.1\r\n"
            print self.header_line
            #self.pwfile.write(self.header_line)
            self.pwfile.write(self.data)
            self.pwfile.flush()
    
            if self.server.set_cookie_flag:
                self.resp_line=self.prfile.readline()
                self.resp_headers=CaseInsensitiveDict()
                while 1:
                    line=self.prfile.readline()
                    if line=="\r\n":
                        break
                    self.resp_headers.update([map(lambda i: i.strip(),line.split(":",1))])  #max split ->2 ref: http://abc  2:in one line    
                self.resp_headers.update({"Set-Cookie":self.server.set_cookie})
                self.resp_data=self.prfile.read(int(self.resp_headers.get("Content-Length",1024)))
                self.resp_header_line=""
                for key in self.resp_headers.keys():
                    self.resp_header_line+=key+": "+self.resp_headers[key]+'\r\n'                
                self.wfile.write(self.resp_line+self.resp_header_line+"\r\n"+self.resp_data)
                
            else:
                self.wfile.write(self.prfile.read())        
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
    server=ThreadTCPServer(("localhost",12345),Handler)
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

if __name__ == '__main__':
    # server=SocketServer.TCPServer(("localhost",12345),Handler)
    # server.serve_forever()
    USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a ZyngaBundleIdentifier/com.zynga.zjayakashi.0 ZyngaBundleVersion/2.8.0"
    USER_KEY="86cbb0f770854622874dd3222cb6243c"
    #startServer(USER_KEY,USER_AGENT)
    startServer(USER_KEY, USER_AGENT, "", "")
    while 1:
        pass

