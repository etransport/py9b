"""Transport abstract class"""

def checksum(data):
	s = 0
	for c in data:
		s += ord(c)
	return (s & 0xFFFF) ^ 0xFFFF


class BaseTransport(object):
	DEV01 = 1
	ESC = 0x20
	BLE = 0x21
	BMS = 0x22
	HOST = 0x3E

	def __init__(self, link):
		self.link = link

	def recv(self):
		raise NotImplementedError()

	def send(self, src, dst, cmd, param, data=""):
		raise NotImplementedError()


__all__ = ["checksum", "BaseTransport"]
