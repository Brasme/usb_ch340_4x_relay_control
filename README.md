# See also
If problems, look at https://github.com/williamblair333/usb_ch340_relay_control. He commented "I uninstalled serial and installed pyserial. Everything seemed to work after that.".

# usb_ch340_4x_relay_control
"LCUS-4 USB CH340 Chip 4x Relay Control" written in Python

I bought a "LCUS-4 4 Channel USB Relay Module Smart Switch" to control some power supply's for my DIY kits.

Python is probably the easiest way to control this device - using "tera term" or another serial port interface that supports binary/hex strings is another.

Or C# / C++ .. but then we are stuck with issues like "Linux or Windows"...

I wrote it using Python 3.7.  I did not put a big effort in making it pretty (a mix of globals & functions..) and lacking __main__ pattern.

# License 
Non at all

Feel free to use this as you wish, but don't blame me for any bugs or credit me in any way :)

# Prerequesites
%> pip install serial
%> pip install pyserial
or:
%> python -m pip install ./serial-0.0.97.tar.gz (download from https://pypi.org/project/serial/)

# Usage
Edit the file to choose the com port used - for me, the CH340 ended up with COM7

Run it (cmd) - pure "app":
```
%> python ch340_relay.py
```

Or as TCP server & clients :
```
%> python ch340_relay_server.py <port>
%> python ch340_relay_client.py <host> <port>
```

# Typical output

```
--------------------------------
USB Serial CH340 - Relay control
--------------------------------
Checking status
Relay: 1 = Off
Relay: 2 = Off
Relay: 3 = Off
Relay: 4 = Off
--------------------------------
Menu:
 1 : toggle 1 (Off)
 2 : toggle 2 (Off)
 3 : toggle 3 (Off)
 4 : toggle 4 (Off)
 5 : status query
 6 : turn all on
 7 : turn all off
 8 : toggle all
 9 : exit
 %> 1
Turn relay  1  on
Menu:
 1 : toggle 1 (On)
 2 : toggle 2 (Off)
 3 : toggle 3 (Off)
 4 : toggle 4 (Off)
 5 : status query
 6 : turn all on
 7 : turn all off
 8 : toggle all
 9 : exit
 %>
```


