from binascii import hexlify
from .base import BaseTransport as BT

class BasePacket(object):
	def __init__(self, src=0, dst=0, cmd=0, arg=0, data=""):
		self.src = src
		self.dst = dst
		self.cmd = cmd
		self.arg = arg
		self.data = data

	def __str__(self):
		return "%s->%s: %02X @%02X %s" % (BT.GetDeviceName(self.src), BT.GetDeviceName(self.dst), self.cmd, self.arg, hexlify(self.data).upper())
		

__all__ = ["BasePacket"]
