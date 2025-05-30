from tkinter import Tk
import yaml
from SerialDevice.ui.serial_devices_bar import SerialDevicesBar

class MainApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self.load_config()
        self.serial_devices_bar = SerialDevicesBar(self)
        self.init_gui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_gui(self,):
        self.title(self.config['main_app']['title'])
        self.geometry(f"{self.config['main_app']['width']}x{self.config['main_app']['height']}")
        self.serial_devices_bar.pack(side='left', expand=True, fill='both')
    
    def on_close(self):
        if self.serial_devices_bar is not None:
            self.serial_devices_bar.disconnect_arduino()
        self.destroy()

    @staticmethod
    def load_config():
        with open('SerialDevice/config.yaml', 'r') as f:
            return yaml.safe_load(f)

if __name__ == '__main__':
    print("Main code running")
    app = MainApp()
    app.mainloop()