#!python2-32
from __future__ import print_function
from sys import argv, exit
import os
import argparse
from progressbar import ProgressBar

from py9b.link.base import LinkOpenException, LinkTimeoutException
from py9b.link.tcp import TCPLink
from py9b.link.ble import BLELink
from py9b.link.serial import SerialLink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.packet import BasePacket as PKT
from py9b.transport.xiaomi import XiaomiTransport
from py9b.transport.ninebot import NinebotTransport
from py9b.command.regio import ReadRegs

READ_CHUNK_SIZE = 0x10

def ReadAllRegs(link, tran, dev, hfo):
	size = 0x200 if dev==BT.ESC else 0x100
	pb = ProgressBar(maxval=size).start()
	for i in xrange(0x0, size, READ_CHUNK_SIZE):
		pb.update(i)
		for retry in xrange(5):
			try:
				data = tran.execute(ReadRegs(dev, i>>1, '16s'))[0]
			except LinkTimeoutException:
				continue
			break
		else:
			print('No response !')
			return False
		hfo.write(data)
	pb.finish()
	print('OK')
	return True


##########################################################################################

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
	description='Xiaomi/Ninebot register reader',
	epilog='Example 1:  %(prog)s esc esc_regs.bin  - read ESC regs to esc_regs.bin using default communication parameters' 
	'\nExample 2:  %(prog)s -i tcp -a 192.168.1.10:6000 bms bms_regs.bin  - flash BMS regs over TCP-BLE bridge at 192.168.1.10:6000'
	'\nExample 3:  %(prog)s -i serial -a COM2 esc esc_regs.bin  - read ESC regs via COM2'
	'\nExample 4:  %(prog)s -i ble -a 12:34:56:78:9A:BC esc esc_regs.bin  - read ESC regs via BLE, use specified BLE address')
	
devices = {'esc' : BT.ESC, 'bms' : BT.BMS, 'extbms' : BT.EXTBMS }
parser.add_argument('device', help='device to read from', type=str.lower, choices=devices)

parser.add_argument('file', type=argparse.FileType('wb'), help='output file')

parser.add_argument('-i', '--interface', help='communication interface, default: %(default)s', type=str.lower,
	choices=('ble', 'serial', 'tcp'),  default='ble')

parser.add_argument('-a', '--address', help='communication address (ble: BDADDR, serial: port, tcp: host:port), default: first available')

protocols = {'xiaomi' : XiaomiTransport, 'ninebot' : NinebotTransport }
parser.add_argument('-p', '--protocol', help='communication protocol, default: %(default)s', type=str.lower,
	choices=protocols, default='xiaomi')

if len(argv)==1:
	parser.print_usage()
	exit()
args = parser.parse_args()

if args.device=='extbms' and args.protocol!='ninebot':
	exit('Only Ninebot supports External BMS !')

dev = devices.get(args.device)

if args.interface=='ble':
	try:
		from py9b.link.ble import BLELink
	except:
		exit('BLE is not supported on your system !')
	link = BLELink()
elif args.interface=='tcp':
	from py9b.link.tcp import TCPLink
	link = TCPLink()
elif args.interface=='serial':
	from py9b.link.serial import SerialLink
	link = SerialLink()
else:
	exit('!!! BUG !!! Unknown interface selected: '+args.interface)
		
with link:
	tran = protocols.get(args.protocol)(link)

	if args.address:
		addr = args.address
	else:
		print('Scanning...')
		ports = link.scan()
		if not ports:
			exit('No interfaces found !')
		print('Connecting to', ports[0][0])
		addr = ports[0][1]

	link.open(addr)
	print('Connected')
	try:
		ReadAllRegs(link, tran, dev, args.file)
		args.file.close()
	except Exception as e:
		print('Error:', e)
		raise
