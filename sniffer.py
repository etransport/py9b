#!python2-32
from struct import unpack
from py9b.link.base import LinkOpenException, LinkTimeoutException
#from py9b.link.tcp import TCPLink
#from py9b.link.ble import BLELink
from py9b.link.serial import SerialLink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.packet import BasePacket as PKT
from py9b.transport.xiaomi import XiaomiTransport
from py9b.transport.ninebot import NinebotTransport

link = SerialLink()
#link = TCPLink()
#link = BLELink()

with link:
	print "Scanning..."
	ports = link.scan()
	print ports

	#tran = XiaomiTransport(link)
	tran = NinebotTransport(link)

	#link.open(("192.168.1.45", 6000))
	link.open(ports[0][1])
	print "Connected"

	last_esc_64 = ""
	last_esc_65 = ""
	last_ble_64 = ""
	try:
		while True:
			try:
				rsp = tran.recv()
				if not rsp:
					continue
				if rsp.src==BT.HOST and rsp.dst==BT.ESC and rsp.cmd in (0x64, 0x65):
					if len(rsp.data)==5:
						if rsp.data==last_esc_65:
							continue
						ll, throttle, brake, u2, u3 = unpack("<BBBBB", rsp.data)
						print "BLE->ESC: TH: %02X, BR: %02X, %02X %02X" % (throttle, brake, u2, u3)
						last_esc_65 = rsp.data
						continue
					elif len(rsp.data)==7:
						if rsp.data==last_esc_64:
							continue
						ll, throttle, brake, u2, u3, ver = unpack("<BBBBBH", rsp.data)
						print "BLE->ESC: TH: %02X, BR: %02X, %02X %02X, VER: %04X" % (throttle, brake, u2, u3, ver)
						last_esc_64 = rsp.data
						continue
				elif rsp.src==BT.HOST and rsp.dst==BT.BLE and rsp.cmd==0x64:
					if len(rsp.data)==4:
						if rsp.data==last_ble_64:
							continue
						u0, u1, u2, u3 = unpack("<BBBB", rsp.data)
						print "ESC->BLE: %02X %02X %02X %02X" % (u0, u1, u2, u3)
						last_ble_64 = rsp.data
						continue
				print rsp
			except LinkTimeoutException:
				pass
	except KeyboardInterrupt:
		pass
		
	link.close()
