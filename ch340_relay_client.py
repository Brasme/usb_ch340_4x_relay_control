# License - Non at all - feel free to use this as you wish. Don't blame me for any bugs or credit me in any way :)
# Bent Gramdal, April 2024

import ch340_relay as r
import ch340_relay_cmd as m
import sys
import socket
import threading
import time

class RelayClient:
    def __init__(self,hostname,tcpPort):
        self.running=False
        self.status=m.Status()
        self.verbose=0
        try:
            self.host=hostname
            self.tcpPort=tcpPort
            self.socket=socket.socket()
            self.socket.connect((self.host,self.tcpPort))            
        except socket.error:    
            print(f'Hmm... socket issues to TCP port {hostname}:{tcpPort}, bail out')
            return
        self.thread = threading.Thread(target=self.listener_, args=())
        self.thread.start()
        
    def close(self):
        self.running=False
        self.socket.close()
    
    def listener_(self):
        self.running=True
        print(f'Info: Server - listening on server {self.host}:{self.tcpPort}')
        while self.running:
            try:
                data  = self.socket.recv(1024).decode()
                # Status:On:On:On:Off:Cmd CMD: 5 from client 3
                a=data.lower().split(':')
                if len(a) >= 5 and a[0]=="status":
                    self.status.set(0,{"on":True,"off":False}.get(a[1],False))
                    self.status.set(1,{"on":True,"off":False}.get(a[2],False))
                    self.status.set(2,{"on":True,"off":False}.get(a[3],False))
                    self.status.set(3,{"on":True,"off":False}.get(a[4],False))        
                    print(f'Updated status: {data}')
                elif len(a)>0 and a[0]=="info" and self.verbose>0:
                    print(f'Info from server: {data}')
                elif self.verbose>0:
                    print(f'From server: {data}')
            except:
                print("Info: Server connection closed")
                self.running=False
        
    def onOffStr(self,num):
        return self.status.onOffStr(num)
    
    def send_option(self, choice):
        message =f'CMD: {choice}'
        try:
            self.socket.send(message.encode())
            time.sleep(1) # Just to get the reply & update state            
        except:
            print("Send failed")
                

if __name__ == "__main__":
    hostname=socket.gethostname()
    tcpPort=12355
    if len(sys.argv)>1:
        hostname=sys.argv[1];
    if len(sys.argv)>2:
        tcpPort=int(sys.argv[2]);
    client=RelayClient(hostname,tcpPort)    
    client.send_option(5)
    time.sleep(1)
    doRun=True
    while doRun:
        choice=m.menu(client.status)
        if choice > 0 and choice < 9:
            client.send_option(choice)
        elif choice == 9:
            doRun=False
        else:
            print('Unknown choice ',choice)

    client.close()
    print('Exit..')
