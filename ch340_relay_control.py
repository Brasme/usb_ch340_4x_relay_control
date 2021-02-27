# License - Non at all - feel free to use this as you wish. Don't blame me for any bugs or credit me in any way :)
# Bent Gramdal, Feb. 2021

import threading
import serial
import time

serialPort = serial.Serial('COM7', 9600)

state = [0,0,0,0]
onOffStr=['Off','On']

# Spawn a thread that receives and decode any data from the CH340
# The only response is for the "Status" (0xff) command, where the return is
# a text string, with format typically as:
#  'CH1: OFF\r\n' / 'CH1: ON\r\n'
#  'CH2: OFF\r\n' / 'CH2: ON\r\n'
#  'CH3: OFF\r\n' / 'CH3: ON\r\n'
#  'CH4: OFF\r\n' / 'CH4: ON\r\n'

def read_from_port(ser):
        connected=1
        while connected==1:
           try:
               chars = ser.readline()
               a=chars.split()
               if len(a) == 2:
                   n={b'CH1:':1,b'CH2:':2,b'CH3:':3,b'CH4:':4}.get(a[0],0)
                   onOff={b'OFF':0,b'ON':1}.get(a[1],0)
                   if n > 0:
                       print('Relay:',n,'=',onOffStr[onOff])
                       state[n-1]=onOff
               elif len(chars) > 0:
                   print('Relay:',chars)
           except:
               print('Relay: Terminated')
               connected=0


thread = threading.Thread(target=read_from_port, args=(serialPort,))
thread.start()


def menu():        
        str  = 'Menu:\n'
        str += ' 1 : toggle 1 ({})\n'.format(onOffStr[state[0]])
        str += ' 2 : toggle 2 ({})\n'.format(onOffStr[state[1]])
        str += ' 3 : toggle 3 ({})\n'.format(onOffStr[state[2]])
        str += ' 4 : toggle 4 ({})\n'.format(onOffStr[state[3]])
        str += ' 5 : status query\n'
        str += ' 6 : turn all on\n'
        str += ' 7 : turn all off\n'
        str += ' 8 : toggle all\n'
        str += ' 9 : exit\n'
        str += ' %> '
        choice = input(str)
        if choice > '0' and choice <= '9':
            return int(choice) 
        else:
            return 0

# The CH340 accepts a binary coded message to turn on/off or query the status
onMsg  = [ b'\xA0\x01\x01\xA2', b'\xA0\x02\x01\xA3', b'\xA0\x03\x01\xA4', b'\xA0\x04\x01\xA5' ]
offMsg = [ b'\xA0\x01\x00\xA1', b'\xA0\x02\x00\xA2', b'\xA0\x03\x00\xA3', b'\xA0\x04\x00\xA4' ]
statMsg = b'\xFF'

def check_status():
    print('--------------------------------')
    print('Checking status')
    serialPort.write(statMsg)
    # Wait until thread has received status
    time.sleep(0.5)
    print('--------------------------------')


print('--------------------------------')
print('USB Serial CH340 - Relay control')
time.sleep(1)
check_status()

loop=1
while loop == 1:
    choice=menu()
    if choice > 0 and choice < 5:
        r=choice-1
        if state[r] == 0:
            print('Turn relay ',choice,' on')
            state[r] = 1
            serialPort.write(onMsg[r])
        else:
            print('Turn relay ',choice,' off')
            state[r] = 0
            serialPort.write(offMsg[r])
    elif choice == 5:
        check_status()
    elif choice == 6:
        for i in range(4):
            serialPort.write(onMsg[i])
            # We need to add some delay. The CH340 only can handle one command at a time
            time.sleep(0.1)
            state[i]=1
    elif choice == 7:
        for i in range(4):
            serialPort.write(offMsg[i])
            # We need to add some delay. The CH340 only can handle one command at a time
            time.sleep(0.1)
            state[i]=0
    elif choice == 8:
        for i in range(4):
            if state[i] == 1:
                serialPort.write(offMsg[i])
                state[i]=0
            else:
                serialPort.write(onMsg[i])
                state[i]=1
            # We need to add some delay. The CH340 only can handle one command at a time
            time.sleep(0.1)
    elif choice == 9:
        loop = 0
    else:
        print('Unknown choice ',choice)


print('Exit..')
# This is a dirty way to terminate the read_from_port thread (causing an exception), but ... why not :)
serialPort.close()
time.sleep(1)
