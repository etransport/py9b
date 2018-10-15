from binascii import hexlify

class BasePacket(object):
	def __init__(self, src=0, dst=0, cmd=0, reg=0, data=""):
		self.src = src
		self.dst = dst
		self.cmd = cmd
		self.reg = reg
		self.data = data

	def __str__(self):
		return "%02X->%02X: %02X @%02X %s" % (self.src, self.dst, self.cmd, self.reg, hexlify(self.data).upper())
		

__all__ = ["BasePacket"]
