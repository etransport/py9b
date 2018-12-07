#!python2-32
from py9b.link.base import LinkOpenException, LinkTimeoutException
from py9b.link.tcp import TCPLink
from py9b.link.ble import BLELink
from py9b.link.serial import SerialLink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.packet import BasePacket as PKT
from py9b.transport.xiaomi import XiaomiTransport
from py9b.transport.ninebot import NinebotTransport
from py9b.command.regio import ReadRegs, WriteRegs

#link = SerialLink(dump=True)
#link = TCPLink()
link = BLELink()

with link:
	print "Scanning..."
	ports = link.scan()
	print ports

	#tran = XiaomiTransport(link)
	tran = NinebotTransport(link)

	#link.open(("192.168.1.45", 6000))
	link.open(ports[0][1])
	print "Connected"

	print('Power off...')
	tran.execute(WriteRegs(BT.ESC, 0x79, '<H', 0x0001)) 

	link.close()
