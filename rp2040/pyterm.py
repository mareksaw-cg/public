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

def send(cmd, timeout=1000):
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
    
def clear_buf():
    if uart.any():
        rxdata = uart.read()

def tick(timer):
    global cmd
    if cmd:
        tim.deinit()
        decode(send(cmd))
        cmd = ''
        tim.init(freq=20, mode=Timer.PERIODIC, callback=tick)
    else:
        if uart.any():
            decode(uart.read())

tim.init(freq=20, mode=Timer.PERIODIC, callback=tick)

rxdata = uart.read()
rxdata = ''
while True:
    cmd = input('> ')
    if cmd == 'quit':
        break
    sleep(0.1)

tim.deinit()
print('End')
