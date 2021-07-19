import sys
import asyncio
import logging
import tkinter as tk
from bleak import BleakClient

# window  = tk.TK()
    
ADDRESS = "18:04:ED:62:5B:AC"
if len(sys.argv) == 2:
    ADDRESS = sys.argv[1]


MODE_CHAR = "02a65821-0003-1000-2000-b05cb05cb05c"
GENERICCMD_CHAR = "02a65821-0004-1000-2000-b05cb05cb05c"
DEVNAME_CHAR = "00002a04-0000-1000-8000-00805f9b34fb"

async def run(address, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address) as client:
        log.info(f"Connected: {client.is_connected}")
            
#Mode Selection Read
        mode_selection = await client.read_gatt_char(MODE_CHAR)
        print("Mode Selection: {0}".format(int(mode_selection[0])))
#Mode Selection Write
        await client.write_gatt_char(MODE_CHAR,  bytearray(
                [
                    255, # Yazılacak değer 
                ]))
        await asyncio.sleep(1.0)
        
        print("Write Process OK")
        
#Mode Selection Read        
        mode_selection = await client.read_gatt_char(MODE_CHAR)
        print("Mode Selection: {0}".format(int(mode_selection[0])))
        
#Generic Command Read
        gencmd_selection = await client.read_gatt_char(GENERICCMD_CHAR)
        print("Interface Version: {0}".format(int(gencmd_selection[0])))
        
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(ADDRESS, True))      

# window.mainloop()