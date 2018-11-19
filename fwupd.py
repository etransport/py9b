#!python2-32
from sys import argv, exit
from os.path import getsize
from py9b.link.base import LinkOpenException, LinkTimeoutException
from py9b.link.tcp import TCPLink
from py9b.link.ble import BLELink
from py9b.link.serial import SerialLink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.xiaomi import XiaomiTransport
from py9b.command.regio import ReadRegs, WriteRegs
from py9b.command.update import *

def checksum(s, data):
	for c in data:
		s += ord(c)
	return (s & 0xFFFFFFFF)


fw_dev = BT.BMS
fw_name = "bms.bin"
fw_size = getsize(fw_name)
fw_page_size = 0x80

link = SerialLink(timeout=0.5)
#link = TCPLink()
#link = BLELink()

with link:
	print "Scanning..."
	ports = link.scan()
	print ports

	tran = XiaomiTransport(link)

	#link.open(("192.168.1.45", 6000))
	link.open(ports[0][1])
	print "Connected"

	print "Pinging..."
	for retry in xrange(20):
		print ".",
		try:
			tran.execute(ReadRegs(BT.BMS, 0x10, "14s"))
		except LinkTimeoutException:
			continue
		break
	else:
		exit("Timed out !")
	print ""
	
	hfi = open(fw_name, "rb")

	print "Starting..."
	tran.execute(StartUpdate(fw_dev, fw_size))

	print "Writing..."
	page = 0
	chk = 0
	while fw_size:
		print "{0:X}".format(page*0x80)
		chunk_sz = min(fw_size, fw_page_size)
		data = hfi.read(chunk_sz)
		chk = checksum(chk, data)
		tran.execute(WriteUpdate(fw_dev, page, data))
		page += 1
		fw_size -= chunk_sz
	hfi.close()

	print "Finalizing..."
	tran.execute(FinishUpdate(fw_dev, chk ^ 0xFFFFFFFF))

	print "Reboot"
	tran.execute(RebootUpdate(fw_dev))

