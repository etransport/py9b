from py9b.link.base import LinkOpenException, LinkTimeoutException
from py9b.link.tcp import TCPLink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.packet import BasePacket as PKT
from py9b.transport.xiaomi import XiaomiTransport

#link = SerialLink()
with TCPLink() as link:
	ports = link.scan()
	print ports
	
	tran = XiaomiTransport(link)

	#link.open(("192.168.1.45", 6000))
	link.open(ports[0][1])

	#req = PKT(src=BT.HOST, dst=BT.ESC, cmd=0x01, reg=0x10, data="\x10")
	req = PKT(src=BT.HOST, dst=BT.BMS, cmd=0x01, reg=0x10, data="\x10")

	while raw_input("Press ENTER to send...")!="q":
		tran.send(req)
		try:
			rsp = tran.recv()
		except LinkTimeoutException:
			print "No response"
			continue
		print rsp

	link.close()
