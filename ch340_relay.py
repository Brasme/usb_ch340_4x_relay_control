# License - Non at all - feel free to use this as you wish. Don't blame me for any bugs or credit me in any way :)
# Bent Gramdal, April 2024

import threading
import serial
import time
import sys
import ch340_relay_cmd as m

class Relay:
    def __init__(self,serialPort='COM7'):
        self.port=serial.Serial(serialPort, 9600)
        self.connected=False
        self.status=m.Status()  
        self.verbose=0              
        # The CH340 accepts a binary coded message to turn on/off or query the status
        self.onMsg  = [ b'\xA0\x01\x01\xA2', b'\xA0\x02\x01\xA3', b'\xA0\x03\x01\xA4', b'\xA0\x04\x01\xA5' ]
        self.offMsg = [ b'\xA0\x01\x00\xA1', b'\xA0\x02\x00\xA2', b'\xA0\x03\x00\xA3', b'\xA0\x04\x00\xA4' ]
        self.statMsg = b'\xFF'

        # Spawn a thread that receives and decode any data from the CH340
        
        self.thread = threading.Thread(target=self.read_from_port_thread_, args=())
        self.thread.start()

    def onOffStr(self,num):
        return self.status.onOffStr(num)
            
    def close(self):
        self.connected=False
        self.port.close()

    def check_status(self):
        if self.connected and self.port.is_open:
            self.port.write(self.statMsg)
            return True
        else:
            print("Relay: Not connected")
            return False

    def setOn(self,num):
        if not self.status.setOn(num):
            return False        
        self.port.write(self.onMsg[num])
        # We need to add some delay. The CH340 only can handle one command at a time
        time.sleep(0.1)                
        return True

    def setOff(self,num):
        if not self.status.setOff(num):
            return False
        self.port.write(self.offMsg[num])
        # We need to add some delay. The CH340 only can handle one command at a time
        time.sleep(0.1)                
        return True
    
    def toggle(self,num):
        if num>=4 or num<0:
            return False
        if self.status.isOn(num):
            return self.setOff(num)
        else:
            return self.setOn(num)
            
    def read_from_port_thread_(self):
        # The only response is for the "Status" (0xff) command, where the return is
        # a text string, with format typically as:
        #  'CH1: OFF\r\n' / 'CH1: ON\r\n'
        #  'CH2: OFF\r\n' / 'CH2: ON\r\n'
        #  'CH3: OFF\r\n' / 'CH3: ON\r\n'
        #  'CH4: OFF\r\n' / 'CH4: ON\r\n'

        self.connected=True
        while self.connected:
            try:
                chars = self.port.readline()
            except:
                print('Relay: Terminated')
                connected=False
                break
            a=chars.split()
            if len(a) == 2:
                n={b'CH1:':1,b'CH2:':2,b'CH3:':3,b'CH4:':4}.get(a[0],0)
                onOff={b'OFF':False,b'ON':True}.get(a[1],0)
                if n > 0:
                    self.status.set(n-1,onOff)
                    if self.verbose>0:
                        print('Relay:',n,'=',self.onOffStr(n-1))                        
            elif len(chars) > 0:
                print('Relay:',chars)
        

if __name__ == "__main__":
    # For test only
    com='COM7'
    if len(sys.argv)>1:
        com=sys.argv[1]
    relay=Relay(com)

    print('--------------------------------')
    print('USB Serial CH340 - Relay control')
    relay.check_status()
    time.sleep(1)
    
    loop=True
    while loop:
        choice=m.menu(relay.status)
        if choice > 0 and choice < 5:
            relay.toggle(choice-1)            
        elif choice == 5:
            relay.check_status()
        elif choice == 6:
            for i in range(4):
                relay.on(i)
        elif choice == 7:
            for i in range(4):
                relay.off(i)                
        elif choice == 8:
            for i in range(4):
                relay.toggle(i)                
        elif choice == 9:
            loop = False
        else:
            print('Unknown choice ',choice)

    print('Exit..')
    # This is a dirty way to terminate the read_from_port thread (causing an exception), but ... why not :)
    relay.close()
    time.sleep(1)
