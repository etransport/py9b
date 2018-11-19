from struct import pack, unpack, calcsize
from .base import BaseCommand, InvalidResponse


class ReadMem(BaseCommand):
	def __init__(self, dev, addr, format):
		super(ReadMem, self).__init__(dst=dev, cmd=0x80, arg=calcsize(format), data=pack("<H", addr), has_response=True)
		self.dev = dev
		self.format = format

	def handle_response(self, response):
		if len(response.data)!=calcsize(self.format):
			raise InvalidResponse("ReadMem {0:X}".format(self.dev))
		return unpack(self.format, response.data)


__all__=["ReadMem"]
