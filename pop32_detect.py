import serial
import serial.tools.list_ports
import time
import keyboard

ser = None
state = "PORT_NOT_FOUND"
global foundPorts

def findPOP32(portsFound):
    
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)

        hwid = foundPorts[i].hwid
        strHwid = str(hwid)

        if 'USB Serial Device' in strPort and 'USB VID:PID=0483:5740' in strHwid: # POP-32
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    return commPort

while True:
    if state == "PORT_NOT_FOUND":
        foundPorts = serial.tools.list_ports.comports()        
        connectPort = findPOP32(foundPorts)

        if connectPort != 'None':
            ser = serial.Serial(connectPort,baudrate = 9600, timeout=1)
            print('\nConnected POP-32 to ' + connectPort + '\n')
            state = "PORT_FOUND"

        else:
            print('\nPOP-32 not found. Please connect POP-32 via HID-USB Port.')
            state = "PORT_NOT_FOUND"
        time.sleep(1)
    elif state == "PORT_FOUND":
        while True:
            try:
                print(connectPort,'-', ser.readline().strip().decode("utf-8").split())
            except:
                print('\nOops! POP-32 has been disconnected!')
                state = "PORT_NOT_FOUND"
                break