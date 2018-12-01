"""Firmware update commands"""

from struct import pack, unpack
from .base import BaseCommand, InvalidResponse


# error codes:
#	1 - invalid parameter
#	2 - erase error
#	3 - flash error
#	4 - not locked
#	5 - address error
#	6 - command in progress
#	7 - invalid cmd/len
UpdateErrorCodes = { 0: 'OK', 1: 'Out of bounds', 2: 'Erase error', 3: 'Write error', 
	4: 'Not locked', 5: 'Invalid address', 6: 'Command in progress', 7: 'Invalid payload len'}


class UpdateError(Exception):
	pass


class StartUpdate(BaseCommand):
	def __init__(self, dev, size):
		super(StartUpdate, self).__init__(dst=dev, cmd=0x07, data=pack("<L", size), has_response=True)
		self.dev = dev

	def handle_response(self, response):
		if not len(response.data) in (0, 1):
			raise InvalidResponse("StartUpdate {0:X}".format(self.dev))
		if response.arg!=0:
			raise UpdateError("StartUpdate {0:X}: {1:s}".format(self.dev, UpdateErrorCodes.get(response.arg, str(response.arg))))
		return True


class WriteUpdate(BaseCommand):
	def __init__(self, dev, page, data):
		super(WriteUpdate, self).__init__(dst=dev, cmd=0x08, arg=page & 0xFF, data=data, has_response=True)
		self.dev = dev
		self.page = page

	def handle_response(self, response):
		if not len(response.data) in (0, 1):
			raise InvalidResponse("WriteUpdate {0:X} @{1:X}".format(self.dev, self.page))
		if response.arg!=0:
			raise UpdateError("WriteUpdate {0:X} @{1:X}: {2:s}".format(self.dev, self.page, UpdateErrorCodes.get(response.arg, str(response.arg))))
		return True


class FinishUpdate(BaseCommand):
	def __init__(self, dev, checksum):
		super(FinishUpdate, self).__init__(dst=dev, cmd=0x09, data=pack("<L", checksum), has_response=True)
		self.dev = dev

	def handle_response(self, response):
		if not len(response.data) in (0, 1):
			raise InvalidResponse("FinishUpdate {0:X}".format(self.dev))
		if response.arg!=0:
			raise UpdateError("FinishUpdate {0:X}: {1:s}".format(self.dev, UpdateErrorCodes.get(response.arg, str(response.arg))))
		return True


class RebootUpdate(BaseCommand):
	def __init__(self, dev):
		super(RebootUpdate, self).__init__(dst=dev, cmd=0x0A, has_response=False)
		self.dev = dev

	def handle_response(self, response):
		return True


__all__ = ["UpdateError", "StartUpdate", "WriteUpdate", "FinishUpdate", "RebootUpdate"]
