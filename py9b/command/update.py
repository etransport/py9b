from struct import pack, unpack
from .base import BaseCommand, InvalidResponse


class UpdateError(Exception):
	pass


class StartUpdate(BaseCommand):
	def __init__(self, dev, size):
		super(StartUpdate, self).__init__(dst=dev, cmd=0x07, data=pack("<L", size), has_response=True)
		self.dev = dev

	def handle_response(self, response):
		if len(response.data)!=0:
			raise InvalidResponse("StartUpdate {0:X}".format(self.dev))
		if response.arg!=0:
			raise UpdateError("StartUpdate {0:X} error {1:d}".format(self.dev, response.arg))
		return True


class WriteUpdate(BaseCommand):
	def __init__(self, dev, page, data):
		super(WriteUpdate, self).__init__(dst=dev, cmd=0x08, arg=page, data=data, has_response=True)
		self.dev = dev
		self.page = page

	def handle_response(self, response):
		if len(response.data)!=0:
			raise InvalidResponse("WriteUpdate {0:X} @{1:X}".format(self.dev, self.page))
		if response.arg!=0:
			raise UpdateError("WriteUpdate {0:X} @{1:X} error {2:d}".format(self.dev, self.page, response.arg))
		return True


class FinishUpdate(BaseCommand):
	def __init__(self, dev, checksum):
		super(FinishUpdate, self).__init__(dst=dev, cmd=0x09, data=pack("<L", checksum), has_response=True)
		self.dev = dev

	def handle_response(self, response):
		if len(response.data)!=0:
			raise InvalidResponse("FinishUpdate {0:X}".format(self.dev))
		if response.arg!=0:
			raise UpdateError("FinishUpdate {0:X} error {1:d}".format(self.dev, response.arg))
		return True


class RebootUpdate(BaseCommand):
	def __init__(self, dev):
		super(RebootUpdate, self).__init__(dst=dev, cmd=0x0A, has_response=False)
		self.dev = dev

	def handle_response(self, response):
		return True


__all__ = ["UpdateError", "StartUpdate", "WriteUpdate", "FinishUpdate", "RebootUpdate"]
