#!/usr/bin/env python
"""
Pymodbus Asynchronous Server Example
pip install twisted
pip install pymodbus
"""
# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.version import version
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.asynchronous import StartUdpServer
from pymodbus.server.asynchronous import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import (ModbusRtuFramer,
                                  ModbusAsciiFramer,
                                  ModbusBinaryFramer)
from custom_message import CustomModbusRequest
from twisted.internet.task import LoopingCall
# --------------------------------------------------------------------------- # 
# configure the service logging
# --------------------------------------------------------------------------- # 
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def updating_writer(a):

    log.debug("updating the context")
    context  = a[0]
    register = 3 # mode 3
    slave_id = 0x00
    address  = 0x10 #16. word adresi
    values   = context[slave_id].getValues(register, address, count=5)
    #values   = [v + 1 for v in values]
    values   = [12,43,67,89,45]  
    log.debug("new values: " + str(values))
    context[slave_id].setValues(register, address, values) # server da ki 16. word adresinden itibaren values dizisini yükle.

def run_async_server():
    # Modbus kullanılabilir adress dizisini maple
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [17]*100),
        ir=ModbusSequentialDataBlock(0, [17]*100))
    store.register(CustomModbusRequest.function_code, 'cm',
                   ModbusSequentialDataBlock(0, [17] * 100))
    context = ModbusServerContext(slaves=store, single=True)
    
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()
    


    time = 5 # 5 seconds delay
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(time, now=False) # initially delay by time
    StartTcpServer(context, identity=identity, address=("localhost", 5020),
                   custom_functions=[CustomModbusRequest])
 

if __name__ == "__main__":
    run_async_server()
