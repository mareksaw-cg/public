from machine import Pin, Timer, UART
from time import sleep 

uart = UART(0, 57600, tx=Pin(16), rx=Pin(17))
tim = Timer()
cmd = ''

def tick(timer):
    global cmd
    if cmd:
        uart.write(cmd + '\r\n')
        sleep(0.1)
        
    if uart.any():
        try:
            rxdata = uart.read().decode('ascii').strip()
            if rxdata:
                print(rxdata[(rxdata.find(cmd) + len(cmd)):].strip())
        except:
            print('Error')
    cmd = ''

tim.init(freq=2, mode=Timer.PERIODIC, callback=tick) 

rxdata = uart.read()
rxdata = ''
while True:
    cmd = input()
    if cmd == 'quit':
        break
    sleep(0.1)
    
print('End')
