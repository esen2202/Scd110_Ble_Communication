import Modules.Scd_Characteristic
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

class SCD110Ble:

    def __init__(self,mac):
        self.mac = mac
        self.is_connected = False

    # disconnect Method   
    async def disconnect(self):
        response = False
        if self.device:
            try:
                response = await self.client.disconnect() 
                print("------ DISCONNECT RESPONSE", response)
            except BleakError:
                print("Device couldn't be disconnected")
        return response 

    # connect Method  
    async def connect(self):
        if self.device:
            async with BleakClient(self.device,loop=loop) as self.client:
                if self.client.__class__.__name__ == "BleakClientBlueZDBus":
                    await self.client._acquire_mtu()
               
            result = await self.client.unpair()
            print("------ ###Unpair:", result)  

        return True
    
    # check device address Method 
    async def checkAddress(self):
        self.device = await BleakScanner.find_device_by_address(self.mac, timeout=3.0)
        if not self.device:
            raise BleakError(f"A device with address {self.mac} could not be found.")
        return True


async def run(mac):
    client = SCD110Ble(mac)
    try :
        isAvailable = await client.checkAddress()
        if isAvailable :
            print("--- {0} Device is Active".format(client.mac))
             
            if await client.connect() :
                print("------ Connected to {0} ".format(client.mac))

            if await client.disconnect() :
                print("------ Finished {0} ".format(client.mac))
        else:
            print("--- {0} Device not found".format(client.mac))
    except Exception as e:
        print("--- {0} Exception catched : \n ###{1}".format(client.mac,e))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run("18:04:ED:62:5B:B6"))
