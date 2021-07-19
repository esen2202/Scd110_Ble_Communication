import sys
import asyncio
import logging
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

ADDRESS = "18:04:ED:62:5B:B6"
if len(sys.argv) == 2:
    ADDRESS = sys.argv[1]

# replace with real characteristic UUID
CHAR_UUID = "00000000-0000-0000-0000-000000000000"

DEVNAME_CHAR = "00002a00-0000-1000-8000-00805f9b34fb"
PPC_CHAR = "00002a04-0000-1000-8000-00805f9b34fb"
SYSID_CHAR = "00002a23-0000-1000-8000-00805f9b34fb"
SERIAL_CHAR = "00002a25-0000-1000-8000-00805f9b34fb"
FIRMWARE_CHAR = "00002a26-0000-1000-8000-00805f9b34fb"
HARDWARE_CHAR = "00002a27-0000-1000-8000-00805f9b34fb"
SOFTWARE_CHAR = "00002a28-0000-1000-8000-00805f9b34fb"
MANUFACT_CHAR = "00002a29-0000-1000-8000-00805f9b34fb"

SELFTESTRES = "02a65821-0002-1000-2000-b05cb05cb05c"

MODE_CHAR = "02a65821-0003-1000-2000-b05cb05cb05c"
GENERICCMD_CHAR = "02a65821-0004-1000-2000-b05cb05cb05c"


SHORTTERMEXP_SERV = "02a65821-1000-1000-2000-b05cb05cb05c"
STERESULTS_CHAR = "02a65821-1002-1000-2000-b05cb05cb05c"
 
async def run(ble_address: str, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)
        
    device = await BleakScanner.find_device_by_address(ble_address, timeout=3.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    
    async with BleakClient(device) as client:
        log.info(f"Connected: {client.is_connected}")
        
        if client.__class__.__name__ == "BleakClientBlueZDBus":
            await client._acquire_mtu()
        print("MTU:", client.mtu_size)
        
#Device name Read
        devname = await client.read_gatt_char(DEVNAME_CHAR)
        print("Device Name: {0}".format(devname))
        
#System Id Read
        sysid = await client.read_gatt_char(SYSID_CHAR)
        print("System Id: {0}".format(sysid))
#Serial Number Read
        serial = await client.read_gatt_char(SERIAL_CHAR)
        print("Serial No: {0}".format(serial))
#Firmware Revisin Number Read
        firm = await client.read_gatt_char(FIRMWARE_CHAR)
        print("Firmware No: {0}".format(firm))
#Hardware Revision Number Read
        hard = await client.read_gatt_char(HARDWARE_CHAR)
        print("Hardware No: {0}".format(hard))                
#Software Revision Number Read
        soft = await client.read_gatt_char(SOFTWARE_CHAR)
        print("Software No: {0}".format(soft))    
#Manufacture Name Read
        manufact = await client.read_gatt_char(MANUFACT_CHAR)
        print("Manufacture Name: {0}".format(manufact))    

#Mode Selection Read
        mode_selection = await client.read_gatt_char(MODE_CHAR)
        print("Mode Selection: {0}".format(int(mode_selection[0])))
#Mode Selection Write
        await client.write_gatt_char(MODE_CHAR,  bytearray(
                [
                    0, # Yazılacak değer 
                ]))
        await asyncio.sleep(1.0)
        
        print("Mode Selection Process OK")
        
#Generic Start Stop Write
        await client.write_gatt_char(GENERICCMD_CHAR, b"\x20")
        await asyncio.sleep(3.0)
        
        print("Generic Start Writre OK")

#Generic Command Read
        generic_cmd= await client.read_gatt_char(GENERICCMD_CHAR)
        print("Generic Code: {0}".format(int(generic_cmd[0])))

#mtu size max 23 byte bizim result ise 33 byte o yüzden mtu yu yeniden boyutlandırmamız gerekiyor.
        
        
#STE Results Read       
        cond = 0
        while cond == 0:
            #Results      
            ste_results = await client.read_gatt_char(STERESULTS_CHAR)
            print("Readed Results :" , len(ste_results))
            print(ste_results)
            #Mode Selection Read        
            mode_selection = await client.read_gatt_char(MODE_CHAR)
            print("Mode Selection: {0}".format(int(mode_selection[0])))
            
            var = await client.read_gatt_char(SELFTESTRES)
            print("Self Test Results: {0}".format(var))
            
            cond = int(input("Devam etmek için 0 : "))
        
        print("Okuma Bitti")
        
        
loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(run(ADDRESS, True))

 
