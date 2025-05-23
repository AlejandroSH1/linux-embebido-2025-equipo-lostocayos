#standard python libraries
import time
#3rd party libraries (like pyserial)
import serial
#Lastly local modules

SERIAL_PORT = 'COM5'
BAUDRATE = 9600
serial_device = serial.Serial(
    port = SERIAL_PORT,
    baudrate = BAUDRATE
)
time.sleep(2)
serial_device.write(b"Connect")
message = serial_device.readline()

#pregunta, qué tipo de dato es message?
print(type(message))
print(message.decode(encoding='utf-8'))

while True: 
    try:
        to_send = input('Mensaje a enviar: ')
        serial_device.write(to_send.encode())
        time.sleep(1)
        received = serial_device.readline()
        print(received.decode())
    except KeyboardInterrupt:
        break
serial_device.close()
print("Bye")