#!python2-32
from __future__ import print_function
from sys import exit
from py9b.link.base import LinkOpenException, LinkTimeoutException
from py9b.link.tcp import TCPLink
from py9b.link.ble import BLELink
from py9b.link.serial import SerialLink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.packet import BasePacket as PKT
from py9b.transport.xiaomi import XiaomiTransport
from py9b.transport.ninebot import NinebotTransport
from py9b.command.regio import ReadRegs, WriteRegs
from py9b.command.mfg import WriteSN
from time import sleep


#new_sn = "16133/00101234"
#new_sn = "N2GTR1826C1234"

def CalcSnAuth(oldsn, newsn, uid3):
	s = 0
	for i in xrange(0x0E):
		s += ord(oldsn[i])
		s *= ord(newsn[i])
	s += uid3+(uid3<<4)
	s &= 0xFFFFFFFF		
	if (s & 0x80000000)!=0:
		s = 0x100000000-s

	return s % 1000000


#link = SerialLink(dump=True)
#link = TCPLink()
link = BLELink(dump=True)

with link:
	print("Scanning...")
	ports = link.scan()
	print(ports)

	#tran = XiaomiTransport(link)
	tran = NinebotTransport(link)

	#link.open(("192.168.1.45", 6000))
	link.open(ports[0][1])
	print("Connected")

	print("Pinging...")
	for retry in xrange(20):
		print(".", end="")
		try:
			old_sn = tran.execute(ReadRegs(BT.ESC, 0x10, "14s"))[0]
		except LinkTimeoutException:
			continue
		break
	else:
		exit("Timed out !")
	print("")

	
	#lock
	#tran.execute(WriteRegs(BT.ESC, 0x70, "<H", 0x01))

	old_sn = tran.execute(ReadRegs(BT.ESC, 0x10, "14s"))[0]
	print("Old S/N:", old_sn)

	uid3 = tran.execute(ReadRegs(BT.ESC, 0xDE, "<L"))[0]
	print("UID3: %08X" % (uid3))

	auth = CalcSnAuth(old_sn, new_sn, uid3)
	#auth = 0
	print("Auth: %08X"  % (auth))

	try:
		tran.execute(WriteSN(BT.ESC, new_sn, auth))
		print("OK")
	except LinkTimeoutException:
		print("Timeout !")

	# save config and restart
	tran.execute(WriteRegs(BT.ESC, 0x78, "<H", 0x01))
	sleep(3)

	old_sn = tran.execute(ReadRegs(BT.ESC, 0x10, "14s"))[0]
	print("Current S/N:", old_sn)

	link.close()
