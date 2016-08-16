import minimalmodbus
import time

def readvol( idslave ):
	rs485 = minimalmodbus.Instrument('/dev/ttyAMA0', idslave, mode='rtu')
	rs485.debug = True         # this is the serial port name
	rs485.CLOSE_PORT_AFTER_EACH_CALL=True
	rs485.serial.baudrate = 2400   # Baud
	rs485.serial.bytesize = 8
	rs485.serial.parity   = minimalmodbus.serial.PARITY_NONE
	rs485.serial.stopbits = 1
	rs485.serial.timeout  = 3   # seconds
	vol = rs485.read_float(0, functioncode=4, numberOfRegisters=2)
	time.sleep(1)
	return vol

def readcurr( idslave ):
	rs485 = minimalmodbus.Instrument('/dev/ttyAMA0', idslave, mode='rtu')
	rs485.debug = True         # this is the serial port name
	rs485.CLOSE_PORT_AFTER_EACH_CALL=True
	rs485.serial.baudrate = 2400   # Baud
	rs485.serial.bytesize = 8
	rs485.serial.parity   = minimalmodbus.serial.PARITY_NONE
	rs485.serial.stopbits = 1
	rs485.serial.timeout  = 3   # seconds
	curr = rs485.read_float(6, functioncode=4, numberOfRegisters=2)
	time.sleep(1)
	return curr

def readappp( idslave ):
	rs485 = minimalmodbus.Instrument('/dev/ttyAMA0', idslave, mode='rtu')
	rs485.debug = True         # this is the serial port name
	rs485.CLOSE_PORT_AFTER_EACH_CALL=True
	rs485.serial.baudrate = 2400   # Baud
	rs485.serial.bytesize = 8
	rs485.serial.parity   = minimalmodbus.serial.PARITY_NONE
	rs485.serial.stopbits = 1
	rs485.serial.timeout  = 3   # seconds
	appp = rs485.read_float(18, functioncode=4, numberOfRegisters=2)
	time.sleep(1)
	return appp

def readenergy( idslave ):
	rs485 = minimalmodbus.Instrument('/dev/ttyAMA0', idslave, mode='rtu')
	rs485.debug = True         # this is the serial port name
	rs485.CLOSE_PORT_AFTER_EACH_CALL=True
	rs485.serial.baudrate = 2400   # Baud
	rs485.serial.bytesize = 8
	rs485.serial.parity   = minimalmodbus.serial.PARITY_NONE
	rs485.serial.stopbits = 1
	rs485.serial.timeout  = 3   # seconds
	totalace = rs485.read_float(342, functioncode=4, numberOfRegisters=2)
	time.sleep(1)
	return totalace
