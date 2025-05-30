from tkinter import Button
from tkinter import END
from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter import Label
from SerialDevice.serial_device import SerialDevice
from SerialDevice.serial_device import BAUDRATES
from tkinter import Text
from SerialDevice.caesar_cipher_arduino.cesar_cipher_arduino import caesar_cifrar

class SerialDevicesBar(Frame):
    def __init__(self, master = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        config = master.config  # <- Esto te da acceso al YAML
        font_family = config['style']['font_family']
        font_size = config['style']['font_size']
        font_color = config['style']['font_color']
        background_color = config['style']['background_color']
        self.arduino = None
        self.serial_devices_label = Label(
            self,
            text = "Pick a serial port:",
            font=(font_family, font_size),
            fg=font_color,
            bg=background_color
        )
        self.serial_devices_combobox = Combobox(
            self,
            values=self.get_available_serial_port(),
            font=(font_family, font_size)
        )
        self.baudrates_combobox = Combobox(
            self,
            values=BAUDRATES,
            font=(font_family, font_size)
        )
        self.textbox = Text(
            self,
            font=(font_family, font_size),
            fg=font_color,
            bg=background_color,
            height=2
        )
        self.send_message_button = Button(
            self,
            text = "Send Message",
            font=(font_family, font_size),
            fg=font_color,
            bg=background_color,
            command=self.send_message

        )
        self.send_message_label = Label(
            self,
            text = "Send Message to Arduino(Format:key:Message)",
            font=(font_family, font_size),
            fg=font_color,
            bg=background_color
        )
        self.read_message_label = Label(
            self,
            text = "Received a message from Arduino->",
            font=(font_family, font_size),
            fg=font_color,
            bg=background_color
        )
        self.textbox_received_message = Text(
            self,
            font=(font_family, font_size),
            fg=font_color,
            bg=background_color,
            height=2
        )
        self.disconnect_button = Button(
            self,
            text='Disconnect',
            font=('Arial', 18),
            command=self.disconnect_arduino
        )
        self.init_gui()

    def init_gui(self):
        self.serial_devices_label.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.serial_devices_combobox.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.baudrates_combobox.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.serial_devices_combobox.current(0)
        self.baudrates_combobox.current(0)
        self.serial_devices_combobox.bind('<<ComboboxSelected>>', self.connect_arduino)
        self.send_message_label.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.send_message_button.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.textbox.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.read_message_label.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.textbox_received_message.pack(side='top', padx=5, pady=5, expand=True, fill='x')
        self.disconnect_button = Button(self, text='Desconectar', command=self.disconnect_arduino)
        self.disconnect_button.pack(side='top', padx=5, pady=5, expand=True, fill='x')

    def get_available_serial_port(self)->list[str]:
        port_list = ['Port:']
        port_list.extend(SerialDevice.find_available_serial_ports())
        return port_list
    
    def connect_arduino(self):
        if self.arduino is None and self.serial_devices_combobox.get() != 'Port:':
            self.arduino = SerialDevice(
                port=self.serial_devices_combobox.get(),
                baudrate=int(self.baudrates_combobox.get())
            )
        elif self.serial_devices_combobox.get() != 'Port:':
            self.arduino.disconnect()
            self.arduino = SerialDevice(
                port=self.serial_devices_combobox.get(),
                baudrate=int(self.baudrates_combobox.get())
            )
    def send_message(self):
        text_to_send = self.textbox.get("1.0", END).strip()  # Elimina espacios y saltos innecesarios
        if ":" in text_to_send:
            desplazamiento, mensaje = text_to_send.split(":", 1)
            try:
                clave = int(desplazamiento)
                mensaje_cifrado = caesar_cifrar(mensaje, clave)  # Nota: mensaje primero, luego clave
                # Mostrar el mensaje cifrado en la textbox_received_message
                self.textbox_received_message.insert("1.0", f"Mensaje cifrado: {mensaje_cifrado}\n")
                if self.arduino is not None:
                    received = self.arduino.send_message(mensaje_cifrado + "\n")
            except ValueError:
                self.textbox_received_message.insert("1.0", "Error: la clave debe ser un número entero\n")
        else:
            self.textbox_received_message.insert("1.0", "Error: formato debe ser clave:mensaje\n")
    
    def disconnect_arduino(self):
        port = self.serial_devices_combobox.get()
        baudrate = self.baudrates_combobox.get()
        port_list = self.get_available_serial_port()
        baudrate_list = [str(b) for b in BAUDRATES]

        if port in port_list or baudrate in baudrate_list:
            if self.arduino is not None:
                self.arduino.disconnect()
                self.arduino = None
            self.serial_devices_combobox.set('Port:')
            self.baudrates_combobox.set('')
            self.textbox_received_message.insert("1.0", "Arduino desconectado correctamente.\n")
        else:
            self.textbox_received_message.insert("1.0", "No hay conexión activa.\n")