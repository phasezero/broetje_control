from binascii import hexlify
from time import localtime
from serial import Serial
from PyCRC.CRCCCITT import CRCCCITT

'''
Configurations

ToDo:
create a config file for configurations like
Serial Device and if an eBus reader is used so
the bytes read must be inverted or not.

Paritys:
{'S': 'Space', 'M': 'Mark', 'E': 'Even', 'O': 'Odd', 'N': 'None'}
'''

DEVICE = '/dev/ttyUSB0'
BAUD = 4800
STOP_BITS = 1
INVERT = True
PARITY = 'O'
LENGTH_BYTE = 4
START_BYTE = ['0xdc'] # NUR HEX DARSTELLUNG MIT KLEINBUCGSTABEN


class Bus:
	'''Common class for using LPB bus'''
	def __init__(self, device, baud, stop_bits, bus_parity, byte_size, invert_bytes):
		self.__device = device
		#if baud in (75,300,1200,2400,4800,9600,14400,19200,28800,38400,57800,115200)
		self.__baud = baud
		#{'S': 'Space', 'M': 'Mark', 'E': 'Even', 'O': 'Odd', 'N': 'None'}
		self.__parity = bus_parity
		self.__stop_bits = stop_bits
		self.__byte_size = byte_size
		self.__invert = invert_bytes
		self.__tty = (Serial(self.__device, self.__baud, timeout=0, parity=self.__parity, stopbits=self.__stop_bits, bytesize=self.__byte_size, xonxoff=False, rtscts=False))
	def __read__(self):
		'''
		function to read one byte from serial and return int value of it
		'''
		buffer=[]
		self.__tty.in_waiting
		if self.__tty.in_waiting >= 4:
			if self.__invert:
				for e in self.__tty.read_all():
					buffer.append(e^255)
				return(buffer)
			else:
				return self.__tty.read_all()		
	def isConnected(self):
		if self.__tty:
			return(True)
		else:
			return(False)
	def disconnect(self):
		self.__tty.close()
	def read_buffer(self):
		return(self.__read__())



	'''
		Eyample:
	  + DC 8A 7F 14 02 05 00 00 6C 00 72 0B 09 07 14 02 26 00 AE DF
		|  |  |  |  |  |     |        |  |  |  |  |           |
		|  |  |  |  |  |     |        |  |  |  |  Uhrzeit: 20:02:38
		|  |  |  |  |  |     |        |  |  |  Wochentag: Sonntag
		|  |  |  |  |  |     |        |  |  |  |  |           |
	  + DC 8A 7F 14 02 05 00 00 6C 00 72 0B 0A 01 14 34 23 00 25 4A
		|  |  |  |  |  |     |        |  |  |  |  |           |
		|  |  |  |  |  |     |        |  |  |  |  Uhrzeit: 20:52:35
		|  |  |  |  |  |     |        |  |  |  |  |           |
	  + DC 8A 7F 14 02 05 00 00 6C 00 72 0B 0A 01 16 0C 25 00 0E 80
		|  |  |  |  |  |     |        |  |  |  |  |           |
		|  |  |  |  |  |     |        |  |  |  |  |           CRC
		|  |  |  |  |  |     |        |  |  |  |  Uhrzeit: 22:12:37
		|  |  |  |  |  |     |        |  |  |  Wochentag: Montag
		|  |  |  |  |  |     |        |  |  Tag: 10
		|  |  |  |  |  |     |        |  Monat: 11
		|  |  |  |  |  |     |        Jahr: 1900 + 0x72 (114) = 2014
		|  |  |  |  |  |     Message A1/A2 : 0x006C
		|  |  |  |  |  Message U1/U2 : 0x0500
		|  |  |  |  Message type  : 0x02 – INFO
		|  |  |  Frame length  : 20 Bytes
		|  |  Source Address: 0x7F - Broadcast
		|  Dest. Address : 0x8A – Display
		Start of Frame: 0xDC
	'''
class LPB_Frame:
	def __init__(self, start_byte=220):
		self.timestamp = localtime()
		self.start_byte=start_byte
		self.frame = [start_byte]
	def __str__(self):
		return(self.__repr__())
	def __repr__(self):
		str=[]
		for e in self.frame:
			str.append(hex(e))
		return(str)
	def append(self, data):
		self.frame.append(data)
	def len(self):
		return(len(self.frame))
	def length(self):
		if self.len() >= 4:
			return(self.frame[3])
		return(-1)
	def get_data(self):
		return(self.frame)
	der get_time(self)
		return(self.timestamp)
	def check(self):
		CRC=int(hex(self.frame[-2])+hex(self.frame[-1])[-2:],16)
		CRC2=b''
		for e in self.frame[0:-2]:
			CRC2 += bytes([e])
		if CRC == CRCCCITT().calculate(CRC2):
			return(True)
		return(False)

 
def lpb_handler():
	'''
	function to read lpb bus via serial interface
	Requieres: serial, time, binascii
	'''
	bus = Bus(DEVICE, 4800, 1, 'O', 8, True)
	raw=[]
	if bus.isConnected():
		zeit = time.time()+28800
		while zeit>=time.time():
			time.sleep(2)
			# Soweit bisher bekannt beginnen die Datenpakete mit dem Byte \xDC 
			buffer=bus.read_buffer()
			if buffer:
				print(buffer)
				with open('heizungsdaten.txt','a') as f:
					f.write(str(buffer)+'\n')
				f.close()
				frame = None
				for b in buffer:
					if hex(b) in START_BYTE:
						frame = LPB_Frame(b)
					elif frame:
						frame.append(b)
						if frame.len() == frame.length(): 
							raw.append(frame)
							frame = None
		
	bus.disconnect()
	return(raw)
					
