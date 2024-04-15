# License - Non at all - feel free to use this as you wish. Don't blame me for any bugs or credit me in any way :)
# Bent Gramdal, April 2024

class Status:
    def __init__(self):
        self.state = [False,False,False,False]
    
    def onOffStr(self,num):
        if num>=4 or num<0:
            return "Unknown"
        elif self.state[num]:
            return "On"
        else:
            return "Off"

    def isOn(self,num):
        if num>=4 or num<0:
            return False
        return self.state[num]
        
    def setOn(self,num):
        if num>=4 or num<0:
            return False
        elif self.state[num]:
            print('Turn relay ',num+1,' on - already on')
            return True
        else:
            print('Turn relay ',num+1,' on')
            self.state[num] = True            
            return True

    def setOff(self,num):
        if num>=4 or num<0:
            return False
        elif not self.state[num]:
            print('Turn relay ',num+1,' off - already off')            
            return True
        else :
            print('Turn relay ',num+1,' off')
            self.state[num] = False            
            return True

    def set(self,num,onOff):
        if num>=4 or num<0:
            return False
        self.state[num]=onOff
        
    def toggle(self,num):
        if num>=4 or num<0:
            return False
        if self.state[num]:
            return self.setOff(num)
        else:
            return self.setOn(num)
    
def menu(state):        
    str  = 'Menu:\n'
    str += ' 1 : toggle 1 ({})\n'.format(state.onOffStr(0))
    str += ' 2 : toggle 2 ({})\n'.format(state.onOffStr(1))
    str += ' 3 : toggle 3 ({})\n'.format(state.onOffStr(2))
    str += ' 4 : toggle 4 ({})\n'.format(state.onOffStr(3))
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

if __name__ == "__main__":
    # For test only
    print('--------------------------------')
    print('Menu test')
    status = Status()
    loop=True
    while loop:
        choice=menu(status)
        if choice > 0 and choice < 5:
            status.toggle(choice-1)            
        elif choice == 6:
            for i in range(4):
                status.setOn(i)
        elif choice == 7:
            for i in range(4):
                status.setOff(i)                
        elif choice == 8:
            for i in range(4):
                status.toggle(i)                
        elif choice == 9:
            loop = False
        else:
            print('Unhandled choice ',choice)
    print('Exit..')
