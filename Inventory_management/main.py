#!/usr/bin/python

#import libraries
import serial
import threading
import time
import signal
import json
import threading
import os
from gpio_96boards import GPIO

#serial communication settings
data = json.load(open('config.json'))
usb_setting = data['usb_setting']
se = serial.Serial(usb_setting, 115200)
sensor_count = int(data['sensor_count'])
print(sensor_count)

#GPIO settings
GPIO_A = GPIO.gpio_id('GPIO_A')
GPIO_B = GPIO.gpio_id('GPIO_B')
GPIO_C = GPIO.gpio_id('GPIO_C')
GPIO_D = GPIO.gpio_id('GPIO_D')
GPIO_E = GPIO.gpio_id('GPIO_E')
GPIO_H = GPIO.gpio_id('GPIO_H')
GPIO_K = GPIO.gpio_id('GPIO_K')

pins_a = ((GPIO_A, 'in'), )
pins_b = ((GPIO_B, 'in'), )
pins_c = ((GPIO_C, 'in'), )
pins_d = ((GPIO_D, 'in'), )
pins_e = ((GPIO_E, 'in'), )
pins_h = ((GPIO_H, 'in'), )
pins_k = ((GPIO_K, 'in'), )

gpio_arr = [GPIO_A, GPIO_B, GPIO_C, GPIO_D, GPIO_E, GPIO_H, GPIO_K]
pins = [pins_a, pins_b, pins_c, pins_d, pins_e, pins_h, pins_k]

i = 0
val = 0 
t = []
send_status = [-1, -1, -1, -1, -1, -1, -1]
isSuccess = 0

#AT commands
apn_setup = 'at+qicsgp=1,1,"'+str(data['apn'])+'","'+str(data['username'])+'","'+str(data['password'])+'",'+str(data['auth_id'])

#url setting
url = str(data['url_connect'])
connect = 'at+qhttpurl='+str(len(url))+','+str(data['response_time'])

#All commands to run one after another
command_group = ['at+qeng="servingcell"', apn_setup, 'at+qhttpcfg="contextid",1', 'at+qiact=1', connect, url]
success_print_group = ['Serving cell setup done!', 'APN setup done!', 'HTTP Context setup done!', 'Activate context 1!', 'Setting up the connection...', url]


def blink(i):
    with GPIO(pins[i]) as gpio: 
        while True:
            val = gpio.digital_read(gpio_arr[i])
            print("Sensor "+str(i)+" : "+str(val))
            try:
                if(val == 0 and send_status[i] == 0):
                    command = 'at+qhttpget='+str(data['response_time'])
                    se.write(command + '\r\n')
                    print(command)
                    send_status[i] = 1
                elif(val == 1):
                    send_status[i] = 0
                    
            except KeyboardInterrupt:
                break
            time.sleep(1)



def start_sensor_read():
    i = 0
    while(i < sensor_count):
        t = threading.Thread(target=blink, args=(i, )) 
        t.start()
        i += 1
    

#Reading data from serial
def serial_read():
    global isSuccess
    global i
    while True:
        strng = se.readline()
        if 'NOCONN' in strng:
            while 'OK' not in strng:
                strng = se.readline()
            
        else:
            if 'OK' in strng:
                pass
            elif 'CONNECT' in strng:
                pass
            else:
                continue

        if( i < len(command_group)):
            isSuccess = 1
            print(success_print_group[i])
            i += 1


#Writing to serial
def serial_main():
    read_th = threading.Thread(target = serial_read, args=())
    read_th.start()
    global isSuccess
    global i
    
    while( i < len(command_group)):
        try: 
            command  = command_group[i]
            if(command):
                se.write(command + '\r\n')
                time.sleep(2)
                if isSuccess == 1:             
                    isSuccess = 0
        except KeyboardInterrupt:
            pass
    print("Network setup is done...")       


#Keyboard interrupt handle
def intr_handle(signum, sig):
    se.close()
    print('Exiting with pid '+ str(os.getpid()))
    os.kill(os.getpid(), signal.SIGTERM)


#main function
if __name__ == '__main__':

    signal.signal(signal.SIGINT, intr_handle)
    serial_main()   #creating serial communication
    start_sensor_read()
    signal.pause()


