from machine import Pin, Timer, UART
from time import sleep, ticks_ms

uart = UART(1, 57600, tx=Pin(4), rx=Pin(5))
reset = Pin(3, Pin.OUT, value=0)
tim = Timer()
cmd = ''

def decode(bytestream):
    try:
        rxdata = bytestream.decode('ascii').strip()
        if rxdata:
            print(rxdata[(rxdata.find(cmd) + len(cmd)):].strip())
    except:
        print('Error')

def send(cmd, timeout=2000):
    clear_buf()
    uart.write(cmd + "\r\n")
    t1 = ticks_ms()
    while not uart.any():
        t2 = ticks_ms()
        if t2 - t1 > timeout:
            break
    if uart.any():
        rxdata = uart.read()
        return rxdata
    else:
        return b''
    
def send1(cmd):
    clear_buf()
    uart.write(cmd + "\r\n")
    
def recv(timeout=1000):
    t1 = ticks_ms()
    while not uart.any():
        t2 = ticks_ms()
        if t2 - t1 > timeout:
            break
    if uart.any():
        rxdata = uart.read()
        return rxdata
    else:
        return b''    
    
def clear_buf():
    if uart.any():
        rxdata = uart.read()

def tick(timer):
    global cmd
    tim.deinit()
    if cmd:        
        decode(send(cmd))
        cmd = ''

    if uart.any():
        decode(recv())
    tim.init(freq=50, mode=Timer.PERIODIC, callback=tick)
#            decode(uart.read())

tim.init(freq=50, mode=Timer.PERIODIC, callback=tick)

rxdata = uart.read()
rxdata = ''
while True:
    cmd = input('> ')
    if cmd == 'quit':
        break

tim.deinit()
print('End')
