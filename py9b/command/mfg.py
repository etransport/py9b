"""Manufacturer commands"""

from struct import pack, unpack
from .base import BaseCommand, InvalidResponse


class AuthError(Exception):
	pass


class WriteSN(BaseCommand):
	def __init__(self, dev, sn, auth):
		super(WriteSN, self).__init__(dst=dev, cmd=0x18, arg=0x10, data=pack("<14sL", sn, auth), has_response=True)
		self.dev = dev

	def handle_response(self, response):
		if len(response.data)!=0:
			raise InvalidResponse("WriteSN {0:X}".format(self.dev))
		if response.arg!=1:
			raise AuthError("WriteSN {0:X}".format(self.dev))
		return True


__all__=["AuthError", "WriteSN"]
