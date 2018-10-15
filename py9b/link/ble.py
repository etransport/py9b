"""BLE link using BlueGiga adapter via PyGatt/BGAPI"""

from __future__ import absolute_import
import pygatt
from binascii import hexlify

SCAN_TIMEOUT = 3

class BLELink():
	def __init__(self, dump=False):
		self.dev = None
		self.dump = dump


	def __enter__(self):
		self.adapter = pygatt.BGAPIBackend()
		self.adapter.start()
		return self


	def __exit__(self, exc_type, exc_value, traceback):
		self.close()


	def scan(self):
		res = []
		devices = self.adapter.scan(timeout=SCAN_TIMEOUT)
		for dev in devices:
			if dev["name"].startswith(u"MISc"):
				res.append((dev["name"], dev["address"]))
		return res


	def open(self, port):
		self.dev = self.adapter.connect(port, address_type=pygatt.BLEAddressType.random)


	def close(self):
		if self.dev:
			self.dev.disconnect()
			self.dev = None
		self.adapter.stop()


	def read(self, size):
		data = self.dev.read(size)
		if self.dump:
			print "<", hexlify(data).upper()
		return data


	def write(self, data):
		if self.dump:
			print ">", hexlify(data).upper()
		return self.dev.write(data)


__all__ = ["BLELink"]
