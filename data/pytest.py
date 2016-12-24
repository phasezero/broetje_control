	#!/usr/bin/env python
import binascii


def read_log(log_file):
	a = []
	with open(log_file,'r') as f:
		for line in f:
			a.append(int(line[:-2].rsplit('<')[1]))
	return a


def read_raw(fname):

	'''
		read_raw

		Args:
			fname (str): Filename of binary file incl. full path

    Returns:
			list: List with integer values of each read byte.
	'''

	a = []
	with open(fname,'rb') as f:
		b = f.read(1)
		while b:
			a.append(ord(b))
			b = f.read(1)
	return a

def inv_byte(numb):
	'''
		Inverts a given byte value (int) bit by bit
		10 -> 1010 -> 0101 -> 5

		Args:
			numb (int): Byte value as int.

    Returns:
			int: Integer value of bitwise inverted byte.
	'''
	i=numb
	if (type(numb) != int) or (numb > 255) or (numb < 0):
		return(-1)

	# TODO: rausschmeißen wenn nicht mehr benöigt:
	# h='{:0<2}'.format(hex(i)[2:]) # HEX wird eigentlich nicht gebraucht bisher
	# b='{:0>8}'.format(bin(i)[2:])	# binary representation of the number
	# bi=bin(numb ^ (2 ** 9 - 1) - 256)[3:] # inverted binary representation
	# hi='{:0>2}'.format(hex(ii)[2:]) # HEX wird eigentlich nicht gebraucht bisher
	# print('Hex   : {} -> Int   : {: <3} -> Bin   : {}'.format(h,i,b))
	# print('HexInv: {} -> IntInv: {: <3} -> BitInv: {:1>8}'.format(hi,ii,bi))

	return(numb ^ (2 ** 9 - 1) - 256) # integer value of invertet binary

def calc_temp(fst_byte,snd_byte):
	'''
		Fuction to calculate the temperature from two bytes
		as given via LPB bus.

		Args:
			fst_byte (int): Interger value of the byte
			snd_byte (int): Interger value of the byte

    Returns:
			value: Temperature value with 0.1 accuracy
	'''
	if (type(fst_byte) ==  int):
		fst_byte = bytes([fst_byte])
	if (type(snd_byte) ==  int):
		snd_byte = bytes([snd_byte])
	value = int(binascii.hexlify(fst_byte+snd_byte),16)
	if value > 32767:
		value = value - 65535
	return(round((value / 64),1))


if __name__ == "__main__":
	FILE='output_2016-12-19_22-57-34_pur.hex'
	try:
		raw=read_log(FILE)
	except:
		raw=read_raw(FILE)
	data=[]
	for r in raw:
		data.append(inv_byte(r))

	with open('invers_2016-12-19_22-57-34_pur.hex','wb') as out:

		print(data)
		for d in data:
			out.write(binascii.unhexlify(binascii.hexlify(bytes([d]))))
		out.close()





