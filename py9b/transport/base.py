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

	def send(self, src, dst, cmd, arg, data=""):
		raise NotImplementedError()

	def execute(self, command):
		self.send(command.request)
		if not command.has_response:
			return True
		#TODO: retry ?
		rsp = self.recv()
		return command.handle_response(rsp)


__all__ = ["checksum", "BaseTransport"]
