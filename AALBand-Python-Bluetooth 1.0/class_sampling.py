# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:14:03 2020

@author: dlsgr
"""

import sys
import time
import serial
import struct
from dataclasses import dataclass, field
import numpy as np
import glob


# From https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
def get_serial_ports():
    """
    Lists serial ports.
    :return: ([str]) A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        #ports = glob.glob('/dev/tty[A-Za-z]*')
        #ports = glob.glob('/dev/[A-Za-z]*')
        ports = glob.glob('/dev/rfcomm*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    results = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            results.append(port)
        except (OSError, serial.SerialException):
            pass
    print(f"{results}\n")
    return results

@dataclass
class data_class:
    raw_buffer: list = field(default_factory=list)
    selected_rms: dict = field(default_factory=dict)
    svm_data: dict = field(default_factory=dict)  # Basis for training of svm. This is purely a 'backup'
    testing_data: np.ndarray = field(default_factory=lambda: np.zeros((1, 10)))
  

class Armband:
    def __init__(self):
        super(Armband, self).__init__()
        
        self.baud = 250000
        self.dataNumBytes = 1
        self.numFSR = 20
        self.num_frames = 1
        self.print_rate = False
        self.rawData = bytearray(self.numFSR * self.dataNumBytes)
        self.dataType = None
        if self.dataNumBytes == 1:
            self.dataType = 'B'     # 1 byte unsigned char
        elif self.dataNumBytes == 2:
            self.dataType = 'h'     # 2 byte integer
        elif self.dataNumBytes == 4:
            self.dataType = 'f'     # 4 byte float
        #self.data_decoded = list()
        self.CONNECTED = False
        self.isRun = True
        self.isReceiving = False
        self.process_serial = None
        self.fsr_publisher = None
        self.imu_publisher = None

                
        self.data_deposit = data_class()
        self.s = serial.Serial(baudrate=self.baud,timeout=0.5, write_timeout=0.5,bytesize=8)
    
    
    def armband_connect(self):
        print("Attempting connection... Please wait.")
        serial_ports = get_serial_ports() 
        for serial_port in serial_ports:
            self.s.port = serial_port
            print(f"Handshaking at port: {serial_port}")
            try:
                self.s.open()
                self.s.write(b'0')
                time.sleep(1)
                print(f"Bytes inWaiting: {self.s.in_waiting}")
                handshake_return = self.s.read(1)
                print(handshake_return)


                print(f"Acknowledgement recieved: {handshake_return}")
                
                if handshake_return == b'1':
                    print(f"Connected at port: {serial_port}")
                    self.CONNECTED = True
                    print(f"Connected = {self.CONNECTED}")
                    self.s.reset_input_buffer()
                    break
                else:
                    self.s.close()
                    print("no device")    
            except (serial.SerialException, OSError, ValueError) as e:
                if self.s.is_open:
                    self.s.close()
                continue

    def armband_calibrate(self):
        self.s.write(b'5')
        print("Calibration finished.")

    def armband_reset_gain(self):
        self.s.write(b'4')
        print("Gain reset.")

    def armband_start_transmission(self):
        for i in range(10):
            time.sleep(0.001)
            self.s.reset_input_buffer()

        self.s.write(b'2')
        time.sleep(0.001)
        print("Transmission started...")

    def armband_end_transmission(self):
        self.s.write(b'3')
        print("Transmission ended.")

        while self.s.in_waiting > 0:
            self.s.read(self.s.in_waiting)
            time.sleep(0.01)

    def armband_close_exit(self):
        self.s.write(b'6')
        self.s.flushInput()
        self.s.close()
        print("Disconnected")
        self.s.__del__()


    def armband_get_sample(self):
        data_buffer = list()
        print(f"Bytes in waiting 1: {self.s.in_waiting}")
        data = self.s.read(208)
        
        print(f"Bytes in waiting 2: {self.s.in_waiting}")
        print(f"Data length: {len(data)}")
        #if len(data) == 20:
            
        for i in range(20):
            data_decoded = list()
            if len(data) == 208:
                for j in range(8):
                    dataDecode = data[(i*8)+(j*1) : (i*8)+(1+j*1)]
                    value, = struct.unpack('B', dataDecode)
                    data_decoded.append(value * 3.3/255)
                data_buffer.append(data_decoded)
            else:
                data_decoded = [1,1,1,1,1,1,1,1]
            
        imu_decoded = list()
        if len(data) == 208:
            for i in range(12):
                imuDecode = data[160+i*4 : 160+4+i*4]
                value_imu, = struct.unpack('f', imuDecode)            
                imu_decoded.append(value_imu)
        else:
            imu_decoded = [1,1,1,1,1,1,1,1,1,1,1,1]
            
        for sample in range(len(data_buffer)):
            data_buffer[sample].extend(imu_decoded + [time.time()])
        #else:
        #    data_decoded = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        return data_buffer




# [0,1,2,3,4,5,6,7, 8,9,10, 11,12,13, 14,15,16, 17,18,19]
if __name__ == '__main__':
    s = Armband()
    s.armband_connect()
    # s.armband_start_transmission()
    # s.armband_calibrate()
    # st = time.time()
    # t = 0
    # sampletime = 5

    # Sample = True
    # #a = s.new_armband_get_sample()
    # while t < sampletime:

    #     try:
    #         a = s.armband_get_sample()
    #         s.data_deposit.raw_buffer.extend(a)
    #         t = time.time() - st
    #         Sample = False
    #     except KeyboardInterrupt:
    #         print("Exiting...")
    #         break
    # b = s.data_deposit.raw_buffer
    # print(len(s.data_deposit.raw_buffer)/sampletime)
    
    # s.armband_end_transmission()
    # s.armband_close_exit()


    # header_fsr = ["FSR_1","FSR_2","FSR_3","FSR_4","FSR_5","FSR_6","FSR_7","FSR_8"]
    # header_gravity = ["GRAVITY_X","GRAVITY_Y","GRAVITY_Z"]
    # header_angular_velocity = ["ANGULAR_VELOCITY_X","ANGULAR_VELOCITY_Y","ANGULAR_VELOCITY_Z"]
    # header_linear_acceleration = ["LINEAR_ACCELERATION_X","LINEAR_ACCELERATION_Y","LINEAR_ACCELERATION_Z"]
    # header_euler_angle = ["EULER_ANGLE_X","EULER_ANGLE_Y","EULER_ANGLE_Z"]
    # header_imu = header_gravity + header_angular_velocity + header_linear_acceleration + header_euler_angle
    # header = header_fsr + header_imu + ["t"]
   
    # df = pd.DataFrame(b, columns=header)
    # df.to_csv(dt.datetime.now().strftime("%Y_%m_%d_%H%M%S") + ".csv", index=False)
    #p1 = plt.plot(df[header_fsr])
    #p2 = plt.plot(df[header_gravity])
    #p3 = plt.plot(df[header_angular_velocity])
    #p4 = plt.plot(df[header_linear_acceleration])
    #p5 = plt.plot(df[header_euler_angle])
    