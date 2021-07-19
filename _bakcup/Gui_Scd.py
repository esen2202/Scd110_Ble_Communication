import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter.constants import FALSE
import scd_bleak_class as cl
import Modules.Scd_Print as printscd
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()

        self.title('Main Window')
        self.geometry("500x500")

        self.name_var = tk.StringVar()

        self.columnconfigure((0,1,2,3), weight=1)
 

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=10)

        self.create_widgets()
        self.t1 = threading.Thread(target= self.getvalues)
        self.toggle_stream_interrupt = False
    def create_widgets(self):

        padding = {'padx': 5, 'pady': 5}
        # label
        ttk.Label(self, text='BLE Devices:').grid(column=0, row=0, **padding)
        # List of BLE Devices
        self.current_ble_device = tk.StringVar()
        self.ble_devices = ttk.Combobox(self, width = 27, textvariable = self.current_ble_device)
        self.ble_devices.grid(column = 1, row = 0)
        self.ble_devices.current()
        # Button Refresh
        self.refresh_button = ttk.Button(self, text='Refresh', command=self.combobox_scd_device_list)
        self.refresh_button.grid(column=2, row=0, **padding)

        # Output label
        self.output_label = ttk.Label(self)
        self.output_label.grid(column=0, row=1, **padding)

        # Button Connect
        self.connect_button = ttk.Button(self, text='Connect', command=self.connect)
        self.connect_button.grid(column=2, row=1, **padding)

        # List of BLE Device Services
        self.current_service = tk.StringVar()
        self.ble_services = ttk.Combobox(self, width = 60, textvariable = self.current_service)
        self.ble_services.grid(column = 0, row = 3, columnspan=2)
        self.ble_services.current()

        # Button SCD Status ON
        self.steon_button = ttk.Button(self, text='Status ON', command=self.change_ste_on)
        self.steon_button.grid(column=0, row=4, **padding)
        # Button SCD Status OFF
        self.steoff_button = ttk.Button(self, text='Status OFF', command=self.change_ste_off)
        self.steoff_button.grid(column=1, row=4, **padding)
        # Output label
        self.stestat_label = ttk.Label(self)
        self.stestat_label.grid(column=2, row=4, **padding)

        # Button toggle_stream
        self.toggle_button = ttk.Button(self, text='Toggle Stream', command=self.toggle_stream)
        self.toggle_button.grid(column=0, row=5, **padding)
        # Output label
        self.stream_label = ttk.Label(self)
        self.stream_label.grid(column=1, row=5, **padding)    
        
        self.valuesList = tk.StringVar()
        self.valuesList.set((1,2,3,4))
        self.values_lb = tk.Listbox(self,width=50, listvariable=self.valuesList)
        self.values_lb.grid(column=0, row=6,columnspan=3,rowspan=2, **padding)
        self.values_lb.delete(0,"end")    

        self.scdClient =  cl.BleSCD110()  
        self.scdClient.subscribe(self.get_values_subs)
        self.combobox_scd_device_list()

    def combobox_scd_device_list(self):
        devices = self.scdClient.get_ble_list()
        self.listdevice = [] 
        for device in devices:
            self.listdevice.append(device.address)
        self.ble_devices['values'] = self.listdevice
        #self.output_label.config(text=self.name_var.get())
        #self.connect()
        #self.output_label.config(text=self.scdClient.mac)

    def connect(self):
        if self.scdClient.client !=None:

            self.scdClient.client = None    
        self.scdClient.is_connected = False
        self.output_label.config(text=" ")
        print("Device : {0}".format(self.current_ble_device.get()))
        if self.current_ble_device != None:
            
            ss = self.scdClient.connect(self.current_ble_device.get())
            if self.scdClient.is_connected :
                self.output_label.config(text="Baglandı")
                self.listservice = []
                self.ble_services['values'] = self.listservice   
                self.get_services()
                result = self.scdClient.get_mode_status()
                self.stestat_label.config(text="ON" if result else "OFF")   
                self.scdClient.get_ste_result()
                self.stream_label.config(text="ON" if self.scdClient.ste_on else "OFF")  
                if not self.t1.is_alive() :
                    self.t1 = threading.Thread(target= self.getvalues)
                    self.t1.start()
            else:
                self.output_label.config(text="Baglantı Yok")
 
    def get_services(self):
        services = self.scdClient.get_services()
        self.listservice = []
        for service in services:
            self.listservice.append(service)
        self.ble_services['values'] = self.listservice    
        
    def change_ste_on(self):
        result = self.scdClient.change_mode_status(True)
        self.stestat_label.config(text="ON" if result else "OFF")

    def change_ste_off(self):
        result = self.scdClient.change_mode_status(FALSE)
        self.stestat_label.config(text="ON" if result else "OFF")   

    def toggle_stream(self):
        self.toggle_stream_interrupt = False
        if not self.t1.is_alive():
            self.scdClient.toggle_stream()
            self.scdClient.get_ste_result()
            self.stream_label.config(text="ON" if self.scdClient.ste_on else "OFF") 
            if not self.t1.is_alive() :
                self.t1 = threading.Thread(target= self.getvalues)
                self.t1.start()
        else:
            self.toggle_stream_interrupt = True

    def getvalues(self):
        if self.scdClient.ste_on:
            while self.scdClient.ste_on:
                if  self.toggle_stream_interrupt:
                    self.scdClient.toggle_stream()
                    self.scdClient.get_ste_result()
                    self.stream_label.config(text="ON" if self.scdClient.ste_on else "OFF") 
                self.scdClient.get_ste_result()
                if(len(self.scdClient.ste_results) == 33):
                    printscd.printCharacteristic(self.scdClient.ste_results)
                    for idx,s in enumerate(printscd.Values):
                        self.values_lb.insert(idx,s)

    def get_values_subs(self):
        self.stream_label.config(text="ON" if self.scdClient.ste_on else "OFF") 
        for idx,s in enumerate(printscd.Values):
            self.values_lb.insert(idx,s)       

if __name__ == "__main__":
    app = App()
    app.mainloop()