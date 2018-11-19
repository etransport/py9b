from ..transport.packet import BasePacket as PKT
from ..transport.base import BaseTransport as BT


class InvalidResponse(Exception):
	pass


class BaseCommand(object):
	def __init__(self, src=BT.HOST, dst=0, cmd=0, arg=0, data="", has_response=True):
		self.has_response = has_response
		self.request = PKT(src, dst, cmd, arg, data)


	def handle_response(self, response):
		return True


__all__ = ["BaseCommand", "InvalidResponse"]
