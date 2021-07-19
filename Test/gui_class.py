import asyncio
import tkinter as tk
from tkinter import ttk
import testClass as cl

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tkinter StringVar')
        self.geometry("500x500")

        self.name_var = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=10)
        self.create_widgets()

    def create_widgets(self):

        padding = {'padx': 5, 'pady': 5}
        # label
        ttk.Label(self, text='Name:').grid(column=0, row=0, **padding)

        # Entry
        name_entry = ttk.Entry(self, textvariable=self.name_var)
        name_entry.grid(column=1, row=0, **padding)
        name_entry.focus()

        # Button
        submit_button = ttk.Button(self, text='Submit', command=self.submit)
        submit_button.grid(column=2, row=0, **padding)

        # Output label
        self.output_label = ttk.Label(self)
        self.output_label.grid(column=0, row=1, columnspan=3, **padding)
        
        self.scdClient =  cl.BleSCD110( "18:04:ED:62:5B:AC")
    
    def submit(self):
#         self.output_label.config(text=self.name_var.get())
        self.connect()
        self.output_label.config(text=self.scdClient.mac)
        
    def connect(self):
        loop = asyncio.new_event_loop()
        ss = loop.run_until_complete(self.scdClient.connect())
        loop.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()