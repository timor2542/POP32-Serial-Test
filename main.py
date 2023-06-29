import serial
import serial.tools.list_ports
import time
import os
# import keyboard

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

        if 'USB Serial Device' in strPort and 'USB VID:PID=0483:5740' in strHwid: # POP-32 and POP-32i
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    return commPort

while True:
    if state == "PORT_NOT_FOUND":
        foundPorts = serial.tools.list_ports.comports()        
        connectPort = findPOP32(foundPorts)

        if connectPort != 'None':
            ser = serial.Serial(connectPort,baudrate = 9600, timeout=1)
            os.system('cls')
            print('\nConnected POP-32 to ' + connectPort + '\n')
            state = "PORT_FOUND"

        else:
            os.system('cls')
            print('\nPOP-32 not found. Please connect POP-32 via HID-USB Port.')
            state = "PORT_NOT_FOUND"
        time.sleep(1)
    elif state == "PORT_FOUND":
        while True:
            try:
                result = ser.readline().strip().decode("utf-8").split()
                if(len(result) == 11):
                    for i in range(len(result)-1):
                        result[i] = "{:4d}".format(int(result[i]))
                elif(len(result) == 12):
                    for i in range(len(result)-2):
                        result[i] = "{:4d}".format(int(result[i]))
                elif(len(result) == 1):
                    pass
                else:
                    continue
                os.system('cls')
                print('\n' + connectPort,'-',result)
            except serial.serialutil.SerialException:
                os.system('cls')
                print('\nOops! POP-32 has been disconnected!')
                state = "PORT_NOT_FOUND"
                break
            except:
                os.system('cls')
                print('\nOops! POP-32 has been disconnected!')
                state = "PORT_NOT_FOUND"
                break