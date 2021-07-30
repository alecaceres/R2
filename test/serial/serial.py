import serial
import time

def send_cmd(ser, string):
    ser.write(string)

def format_str(ID, coor_robot, coor_target):
    '''

    '''
    xr, yr = coor_robot
    xt, yt = coor_target
    string = f"{ID}{xr:03d}{yr:03d}{xt:03d}{yt:03d}"
    return bytes(string, 'utf-8')

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

for i in range(1000):
    b = ser.readline()
    string_n = b.decode()
    time.sleep(0.1)
ser.close()