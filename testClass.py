import sys
import asyncio
from bleak import BleakClient, BleakScanner,discover
from bleak.exc import BleakError
import Modules.Scd_Characteristic as c

class BleSCD110:
# __init__
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.ble_address = ""
        self.device = None
        self.is_connected = False
        self.mode_on = False
        self.ste_on = False
# Get Ble Devices List
    async def __async__get_ble_list(self):
        return  await discover()

    def get_ble_list(self):
        return self.loop.run_until_complete(self.__async__get_ble_list())
          
# Connect The Ble Device
    async def __async__connect(self):
        self.device = await BleakScanner.find_device_by_address(self.ble_address, timeout=5.0)
        if not self.device:
            raise BleakError(f"A device with address {self.ble_address} could not be found.")
        self.is_connected = True

    def connect(self,ble_address):
        self.ble_address = ble_address
        return self.loop.run_until_complete(self.__async__connect())

# Get Device Services
    async def __async__get_services(self):
        if self.device:
            async with BleakClient(self.device) as client:
                return await client.get_services()
        self.is_connected = False
        raise BleakError(f"The device with address {self.ble_address} could not be connect.")

    def get_services(self):
        return self.loop.run_until_complete(self.__async__get_services())

# Get STE Result
    async def async_get_ste_result(self):
        if self.device:
            async with BleakClient(self.device) as client:
            #Ste Result Read
                self.ste_results = await client.read_gatt_char(c.ServiceShortTermExperiment["STEResults"])
                if(len(self.ste_results) == 33):
                    self.ste_on = self.ste_results[32]!=0

                return self.ste_on
        self.is_connected = False
        raise BleakError(f"The device with address {self.ble_address} could not be connect.")

    def get_ste_result(self):
        self.loop.run_until_complete(self.async_get_ste_result())
        return self.ste_on

# Toggle Stream Start Stop
    async def __async__toggle_stream(self,on = True):
        if self.device:
            async with BleakClient(self.device) as client:
            #Mode Selection Write
                write = 0 if on else 255
                await client.write_gatt_char(c.ServiceSCDSettings["SCDGenericCommands"],  b"\x20")
                return True
        self.is_connected = False
        raise BleakError(f"The device with address {self.ble_address} could not be connect.")

    def toggle_stream(self,on = True):
        return self.loop.run_until_complete(self.__async__toggle_stream(on))


# Get Mode Status
    async def __async__get_mode_status(self):
        if self.device:
            async with BleakClient(self.device) as client:
            #Mode Selection Read
                mode_selection = await client.read_gatt_char(c.ServiceSCDSettings["ModeSelection"])
                print("--> Mode Selection: {0}".format(int(mode_selection[0])))
                self.mode_on = int(mode_selection[0]) == 0 
                return self.mode_on
        self.is_connected = False
        raise BleakError(f"The device with address {self.ble_address} could not be connect.")

    def get_mode_status(self):
        self.loop.run_until_complete(self.__async__get_mode_status())
        return self.mode_on

# Change Mode Status
    async def __async__change_mode_status(self,on = True):
        if self.device:
            async with BleakClient(self.device) as client:
                #await self.__async__get_mode_status()
                if(not self.ste_on):
                #Mode Selection Write
                    write = 0 if on else 255
                    await client.write_gatt_char(c.ServiceSCDSettings["ModeSelection"],bytearray(
                [
                    0 if on else 255, # Yazılacak değer 
                ]))
                    await asyncio.sleep(1.0)
                return await self.__async__get_mode_status()
        self.is_connected = False
        raise BleakError(f"The device with address {self.ble_address} could not be connect.")

    def change_mode_status(self,on = True):
        return self.loop.run_until_complete(self.__async__change_mode_status(on))

# Get SCD110 information
    async def __async__get_scd_info(self):
        if self.device:
            async with BleakClient(self.device) as client:
            # MTU Size
                if client.__class__.__name__ == "BleakClientBlueZDBus":
                    await client._acquire_mtu()
                print(" MTU  ", client.mtu_size)
            #Device name Read
                devname = await client.read_gatt_char(c.ServiceGenericAccess["DeviceName"])
                print(" Device Name: {0}".format(devname))
            #System Id Read
                sysid = await client.read_gatt_char(c.ServiceDeviceInformation["ServiceID"])
                print(" System Id: {0}".format(sysid))
            #Serial Number Read
                serial = await client.read_gatt_char(c.ServiceDeviceInformation["SerialNumberString"])
                print(" Serial No: {0}".format(serial))
            #Firmware Revisin Number Read
                firm = await client.read_gatt_char(c.ServiceDeviceInformation["FirmwareRevisionString"])
                print(" Firmware No: {0}".format(firm))
            #Hardware Revision Number Read
                hard = await client.read_gatt_char(c.ServiceDeviceInformation["HardwareRevisionString"])
                print(" Hardware No: {0}".format(hard))                
            #Software Revision Number Read
                soft = await client.read_gatt_char(c.ServiceDeviceInformation["SoftwareRevisionString"])
                print(" Software No: {0}".format(soft))    
            #Manufacture Name Read
                manufact = await client.read_gatt_char(c.ServiceDeviceInformation["ManufacturerNameString"])
                print(" Manufacture Name: {0}".format(manufact))    
                return True
        self.is_connected = False
        raise BleakError(f"The device with address {self.ble_address} could not be connect.")

    def get_scd_info(self):
        return self.loop.run_until_complete(self.__async__get_scd_info())

# Disconnect Handling Event
    async def show_disconnect_handling(self):
        if self.device:
            disconnected_event = asyncio.Event()

            def disconnected_callback(client):
                print("Disconnected callback called!")
                disconnected_event.set()

            async with BleakClient(self.device, disconnected_callback=disconnected_callback) as client:
                print("Sleeping until device disconnects...")
                await disconnected_event.wait()
                print("Connected:", client.is_connected)

    def disconnect_handling(self):
        return self.loop.run(self.show_disconnect_handling())

"""
# ----------Main Start----------#
scd = BleSCD110()

# get active scd list
devices = scd.get_ble_list()

if len(devices) > 0:
    for idx, d in enumerate(devices):
        print("{0} ) Address : {1} | Device : {2} ".format(idx,d.address,d))
    selected = input("Select Device : ")

    try :
        scd.connect(devices[int(selected)].address)
        if scd.is_connected :
            print("+ Connected the : {0}".format(scd.device.name))
            #services = scd.get_services()
            #for idx,s in enumerate(services):
            #    print("-> {0} ) Service : {1} ".format(idx,s))
            #scd.get_scd_info()
            scd.get_ste_result()
            print("STE Mode : {0}".format("ON" if scd.ste_on else "OFF"))
            scd.toggle_stream()

            scd.get_ste_result()
            print("STE Toggle Denendi. Sonuç STE Mode : {0}".format("ON" if scd.ste_on else "OFF"))

            result = scd.get_mode_status()
            print("Mod okundu : {0}".format("ON" if result else "OFF"))
            result = scd.change_mode_status(not result)
            print("Mod yazıldı : {0}".format("ON" if result else "OFF"))
            result = scd.get_mode_status()
            print("Mod okundu : {0}".format("ON" if result else "OFF"))
    except Exception as ex:
        print("Exception : ".format(ex))
    except BleakError as ex:
        print("Exception Bleak : ".format(ex))   
"""