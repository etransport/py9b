"""Xiaomi packet transport"""
from struct import pack, unpack
from .base import checksum, BaseTransport as BT
from .packet import BasePacket


class XiaomiTransport(BT):
	HEAD2ESC = 0x20
	ESC2HEAD = 0x23
	HEAD2BMS = 0x22
	BMS2HEAD = 0x25
	DEV01	 = 0x01

	_SaDa2Addr = { 	BT.HOST : { BT.DEV01 : DEV01, BT.ESC  : HEAD2ESC, BT.BMS : HEAD2BMS },
					BT.ESC	: { BT.HOST : ESC2HEAD, BT.BMS : HEAD2BMS, BT.DEV01 : DEV01 },
					BT.BMS  : { BT.HOST : BMS2HEAD, BT.ESC : BMS2HEAD, BT.DEV01 : DEV01 },
					BT.DEV01 : {BT.HOST : DEV01, BT.ESC : DEV01, BT.BMS : DEV01 } }

	# TBC
	_BleAddr2SaDa = { 	HEAD2ESC : (BT.HOST, BT.ESC), 
						ESC2HEAD : (BT.ESC, BT.HOST),
						HEAD2BMS : (BT.HOST, BT.BMS),
						BMS2HEAD : (BT.BMS, BT.HOST),
						DEV01	 : (BT.DEV01, BT.HOST) }

	_BmsAddr2SaDa = { 	HEAD2ESC : (BT.BMS, BT.ESC), 
						ESC2HEAD : (BT.ESC, BT.BMS),
						HEAD2BMS : (BT.ESC, BT.BMS),
						BMS2HEAD : (BT.BMS, BT.ESC),
						DEV01	 : (BT.DEV01, BT.BMS) }


	def __init__(self, link, device=BT.HOST):
		super(XiaomiTransport, self).__init__(link)
		self.device = device


	def _make_addr(self, src, dst):
		return XiaomiTransport._SaDa2Addr[src][dst]

			
	def _split_addr(self, addr):
		if self.device==BT.BMS:
			return XiaomiTransport._BmsAddr2SaDa[addr]
		else:
			return XiaomiTransport._BleAddr2SaDa[addr]


	def _wait_pre(self):
		while True:
			while True:
				c = self.link.read(1)
				if c=="\x55":
					break
			while True:
				c = self.link.read(1)
				if c=="\xAA":
					return True 
				if c!="\x55":
					break # start waiting 55 again, else - this is 55, so wait for AA


	def recv(self):
		self._wait_pre()
		pkt = self.link.read(1)
		l = ord(pkt)+3
		for i in xrange(l):
			pkt += self.link.read(1)
		ck_calc = checksum(pkt[0:-2])
		ck_pkt = unpack("<H", pkt[-2:])[0]
		if ck_pkt!=ck_calc:
			print "Checksum mismatch !"
			return None
		sa, da = self._split_addr(ord(pkt[1]))
		return BasePacket(sa, da, ord(pkt[2]), ord(pkt[3]), pkt[4:-2]) # sa, da, cmd, param, data

	
	def send(self, packet):
		dev = self._make_addr(packet.src, packet.dst)
		pkt = pack("<BBBB", len(packet.data)+2, dev, packet.cmd, packet.reg)+packet.data
		pkt = "\x55\xAA" + pkt + pack("<H", checksum(pkt))
		self.link.write(pkt)


__all__ = ["XiaomiTransport"]
