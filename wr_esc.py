#!python2-32
from py9b.link.base import LinkOpenException, LinkTimeoutException
from py9b.link.tcp import TCPLink
from py9b.link.ble import BLELink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.packet import BasePacket as PKT
from py9b.transport.xiaomi import XiaomiTransport

#link = SerialLink()
link = TCPLink()
#link = BLELink()

with link:
	print "Scanning..."
	ports = link.scan()
	print ports

	tran = XiaomiTransport(link)

	link.open(("192.168.1.45", 6000))
	#link.open(ports[0][1])
	print "Connected"

	req = PKT(src=BT.HOST, dst=BT.ESC, cmd=0x02, arg=0x41, data="\xCE\xAB\x00\x00")

	tran.send(req)
	try:
		rsp = tran.recv()
	finally:
		link.close()

	print rsp
