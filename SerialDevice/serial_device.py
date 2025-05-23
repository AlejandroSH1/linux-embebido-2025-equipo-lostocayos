#standard python libraries
import sys
import os
import time
#3rd party libraries (like pyserial)
import serial
#Lastly local modules

BAUDRATE = [
    4800,
    9600,
    38400,
    57600,
    115200,
    230400,
    460800
]

class SerialDevice:
    def __init__(self, port:str, baudrate:int):
        if baudrate not in BAUDRATE:
            raise ValueError(f"Not a valid baudrate {baudrate}")
        if port not in self.find_available_serial_ports():
            raise ValueError(f"Not a valid port {port}")
        
        self.serial_device = serial.Serial(
            port = port,
            baudrate = baudrate
        )
        time.sleep(2)
        self.serial_device.write('Connect')
        time.sleep(1)
        m = self.serial_device.readline()
        print(m.decode())
        m = self.serial_device.readline()
        print(m.decode())
        
    def send_message(self, message:str)->str:
        self.serial_device(message.encode())
        time.sleep(1)
        return self.read_message()
    
    def read_message(self)->str:
        return self.serial_device.readline().decode()
    
    def disconnect(self)->None:
        self.serial_device.close()

    @staticmethod
    def find_available_serial_ports() -> list[str]:
        if sys.platform.startswith('darwin'):
            ports = os.listdir('/dev/') 
            ports = [f"/dev{port}" for port in ports if port.startswith('cu.')]
        elif sys.platform.startswith('linux'):
            ports = os.listdir('/dev/') 
            ports = [f"/dev{port}" for port in ports if port.startswith('ttyA')]
        elif sys.platform.startswith('win'):
            ports = [f'COM{n}' for n in range(1,256)]
        else:
            return []
            
        return ports