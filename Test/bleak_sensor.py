import sys
import asyncio
import logging

from bleak import BleakClient

ADDRESS = "18:04:ED:62:5B:AC"
if len(sys.argv) == 2:
    ADDRESS = sys.argv[1]


MODE_CHARACTERISTIC = "02a65821-0003-1000-2000-b05cb05cb05c"
GENERICCMD_CHARACTERISTIC = "02a65821-0004-1000-2000-b05cb05cb05c"
DEVNAME_CHARACTERISTIC = "00002a04-0000-1000-8000-00805f9b34fb"

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

#         paired = await client.pair(protection_level=2)
#         log.info(f"Paired: {paired}")

            
        mode_selection = await client.read_gatt_char(MODE_CHARACTERISTIC)
        print("Mode Selection: {0}".format(int(mode_selection[0])))
        await client.write_gatt_char(MODE_CHARACTERISTIC,  bytearray(
                [
                    255, # Yazılacak değer 
                ]))
        await asyncio.sleep(1.0)
        
        print("Write Process OK")
        
#         print("Write Process : {0}",int(mode_selection[0])==0?"OK":"Failed")
        
        mode_selection = await client.read_gatt_char(MODE_CHARACTERISTIC)
        print("Mode Selection: {0}".format(int(mode_selection[0])))
        
        gencmd_selection = await client.read_gatt_char(GENERICCMD_CHARACTERISTIC)
        print("Interface Version: {0}".format(int(gencmd_selection[0])))
        
        
        
#         version_selection = await client.read_gatt_char(DEVNAME_CHARACTERISTIC)
#         print("Interface Version: {0}".format("".join(map(chr, version_selection))))
            
        
"""
        print("Turning Light off...")
        await client.write_gatt_char(LIGHT_CHARACTERISTIC, b"\x00")
        await asyncio.sleep(1.0)
        print("Turning Light on...")
        await client.write_gatt_char(LIGHT_CHARACTERISTIC, b"\x01")
        await asyncio.sleep(1.0)

        print("Setting color to RED...")
        color = convert_rgb([255, 0, 0])
        await client.write_gatt_char(COLOR_CHARACTERISTIC, color)
        await asyncio.sleep(1.0)

        print("Setting color to GREEN...")
        color = convert_rgb([0, 255, 0])
        await client.write_gatt_char(COLOR_CHARACTERISTIC, color)
        await asyncio.sleep(1.0)

        print("Setting color to BLUE...")
        color = convert_rgb([0, 0, 255])
        await client.write_gatt_char(COLOR_CHARACTERISTIC, color)
        await asyncio.sleep(1.0)

        for brightness in range(256):
            print(f"Set Brightness to {brightness}...")
            await client.write_gatt_char(
                BRIGHTNESS_CHARACTERISTIC,
                bytearray(
                    [
                        brightness,
                    ]
                ),
            )
            await asyncio.sleep(0.2)

        print(f"Set Brightness to {40}...")
        await client.write_gatt_char(
            BRIGHTNESS_CHARACTERISTIC,
            bytearray(
                [
                    40,
                ]
            ),
        )
"""

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(ADDRESS, True))