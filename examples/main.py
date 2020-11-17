#test devboard code

from machine import Pin
from pyb import CAN
import utime

print("initializing")
can = CAN(1, CAN.LOOPBACK)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))


#Setup Pins
hbt_led = Pin("D13", Pin.OUT)
func_butt = Pin("D5", Pin.IN, Pin.PULL_UP) 
can_wakeup = Pin("D6", Pin.OUT)
can_wakeup.value(0)

keys = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D'],
        ]
for i in range(4):
    for j in range(4):
        print(keys[i][j])
        
COLUMN = ["E17", "E15", "E14", "E13"]
ROW = ["E12", "E11", "E10", "SD_DETECT"]        

for i in range(len(ROW)):
    ROW[i] = Pin(ROW[i], Pin.OUT)
    ROW[i].value(0)
    
for i in range(len(COLUMN)):
    COLUMN[i] = Pin(COLUMN[i], Pin.IN, Pin.PULL_DOWN)

#Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
hbt_led.value(hbt_state)



print("starting")

def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            hbt_led.value(hbt_state)
        else:
            hbt_state = 1
            hbt_led.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

def chk_buttons():
    global next_button_chk
    now = utime_ms()
    if utime.ticks_diff(next_button_chk, now) <= 0:
        pass
        

def send():
    can.send('EVZRTST', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
        

      
      
while True:
    chk_hbt()
    
    if not (func_butt.value()):
        print("function button")
        utime.sleep_ms(200)
    
    for i in  range(len(ROW)):
        ROW[i].value(1)
        for j in range(len(COLUMN)):
            if (COLUMN[j].value()):
                print(keys[i][j])
                utime.sleep_ms(200)
        ROW[i].value(0)

    
   