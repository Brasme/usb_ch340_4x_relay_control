# License - Non at all - feel free to use this as you wish. Don't blame me for any bugs or credit me in any way :)
# Bent Gramdal, April 2024

import ch340_relay as r
import ch340_relay_cmd as m
import sys
import socket
import threading
import time

class ClientConnection:
    def __init__(self,index,socket,address,on_close,on_cmd):
        self.index=index
        self.socket=socket
        self.address=address
        self.server=server
        self.running=False
        self.on_close=on_close
        self.on_cmd=on_cmd        
        self.thread = threading.Thread(target=self.client_handler_thread_, args=())
        self.thread.start()

    def close(self):
        if self.running:
            self.send_info("Server closed")
            self.running=False
            self.socket.close()
            
    def send_info(self,message):
        if self.running==False:
            return
        try:
            self.socket.send(message.encode())
        except socket.error:
            print("Info: Connection to: " + str(self.address) + " failed to send")
            self.running=False                        

    def client_handler_thread_(self):
        print("Info: Connection from: " + str(self.address))
        self.send_info(f'Welcome to {str(self.address)}')
        self.running=True
        while self.running:
            try:
                cmd = self.socket.recv(1024).decode()
                message=self.on_cmd(self.index,cmd)
                print(f'Info: {message}')
                self.send_info(message)
            except socket.error:
                print("Info: Connection from: " + str(self.address) + " close")#write error code to file
                self.running=False
        self.socket.close()
        self.on_close(self.index)
            
class RelayServer:
    def __init__(self,comPort,tcpPort):
        self.relay=r.Relay(comPort)
        self.relay.check_status()        
        time.sleep(1)
        self.running=False
        self.clients=[]
        self.client_index=0
        try:
            self.host=socket.gethostname()
            self.tcpPort=tcpPort
            self.socket=socket.socket()
            self.socket.bind((self.host,self.tcpPort))
            self.socket.listen(10)
        except socket.error:
            print(f'Hmm... socket issues to TCP port {tcpPort}, bail out')
            return
        self.thread = threading.Thread(target=self.listener_, args=())
        self.thread.start()

        
    def close(self):
        self.running=False
        self.socket.close()
        self.relay.close()
    
    def clientAddr(self,index):
        if index==0:
            return "Server"
        for client in self.clients:
            if client.index==index:
                return client.address
        return "Unknown"
        
    def on_cmd(self,index,cmd):
        a=str(cmd).split()
        if len(a) == 2 and a[0].lower()=="cmd:":
            try:
                choice=int(a[1])
            except:
                choice=0
            if choice>0 and choice<=4:
                server.toggle(choice-1)            
            elif choice == 5:
                server.check_status()
            elif choice == 6:
                for i in range(4):
                    server.setOn(i)
            elif choice == 7:
                for i in range(4):
                    server.setOff(i)                
            elif choice == 8:
                for i in range(4):
                    server.toggle(i)

        message=f'Status:{self.relay.onOffStr(0)}:{self.relay.onOffStr(1)}:{self.relay.onOffStr(2)}:{self.relay.onOffStr(3)}:Cmd {cmd} from client {index}'
        c = None
        for client in self.clients:
            if client.index==index:
                c=client
            client.send_info(message)
        if c!=None:
            return f'Info: Server handled {cmd} from client {index} at {str(c.address)}'
        return f'Info: Server handled {cmd}'
    
    def on_close(self,index):
        print(f'Server: Remove client {index}')
        for client in self.clients:
            if client.index==index:
                self.clients.remove(client)
                break
        
    def listener_(self):
        self.running=True
        print(f'Info: Server - listening for connections on {self.host}:{self.tcpPort}')
        while self.running:
            try:
                socket, address = self.socket.accept()  # accept new connection
                self.client_index += 1
                client=ClientConnection(self.client_index,socket,address,self.on_close,self.on_cmd)
                self.clients.append(client)
            except:
                print("Info: Server - client accept terminated, closing down")
                self.running=False
        for client in self.clients:
            client.close()

    def onOffStr(self,num):
        return self.relay.onOffStr(num)
            
    def check_status(self):
        ok=self.relay.check_status()
        # if ok:
        #    for client in self.clients:
        #    client.send_info('Server scanned status')
        return ok

    def setOn(self,num):
        return self.relay.setOn(num)
    
    def setOff(self,num):
        return self.relay.setOff(num)
        
    def toggle(self,num):
        return self.relay.toggle(num)        

if __name__ == "__main__":
    tcpPort=12355
    comPort='COM7'
    if len(sys.argv)>1:
        comPort=sys.argv[1];
    if len(sys.argv)>2:
        tcpPort=int(sys.argv[2]);
    server=RelayServer(comPort,tcpPort)    
    while server.running:
        choice=m.menu(server.relay.status)
        if choice > 0 and choice < 9:
            server.on_cmd(0,f'CMD: {choice}')            
        elif choice == 9:
            server.close()            
        else:
            print('Unknown choice ',choice)

    print('Exit..')
