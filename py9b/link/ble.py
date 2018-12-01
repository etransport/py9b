"""BLE link using BlueGiga adapter via PyGatt/BGAPI"""

from __future__ import absolute_import
import pygatt
from .base import BaseLink, LinkTimeoutException, LinkOpenException
from binascii import hexlify

SCAN_TIMEOUT = 3


import queue

class Fifo():
	def __init__(self):
		self.q = queue.Queue()

	def write(self, data): # put bytes
		for b in data:
			self.q.put(b)

	def read(self, size=1, timeout=None): # but read string
		res = ""
		for i in xrange(size):
			res += chr(self.q.get(True, timeout))
		return res


#_cccd_uuid = "00002902-0000-1000-8000-00805f9b34fb"
_rx_char_uuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
_tx_char_uuid = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

_write_chunk_size = 20 # as in android dumps

class BLELink(BaseLink):
	def __init__(self, *args, **kwargs):
		super(BLELink, self).__init__(*args, **kwargs)
		self._adapter = None
		self._dev = None
		self._wr_handle = None
		self._rx_fifo = Fifo()


	def __enter__(self):
		self._adapter = pygatt.BGAPIBackend()
		self._adapter.start()
		return self


	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

	
	def _make_rx_cb(self): # this is a closure :)
		def rx_cb(handle, value):
			self._rx_fifo.write(value)
		return rx_cb


	def scan(self):
		res = []
		devices = self._adapter.scan(timeout=SCAN_TIMEOUT)
		for dev in devices:
			if dev["name"].startswith(u"MISc"):
				res.append((dev["name"], dev["address"]))
		return res


	def open(self, port):
		try:
			self._dev = self._adapter.connect(port, address_type=pygatt.BLEAddressType.random)
			self._dev.subscribe(_tx_char_uuid, callback=self._make_rx_cb())
			self._wr_handle = self._dev.get_handle(_rx_char_uuid)
		except pygatt.exceptions.NotConnectedError:
			raise LinkOpenException
			

	def close(self):
		if self._dev:
			self._dev.disconnect()
			self._dev = None
		if self._adapter:
			self._adapter.stop()


	def read(self, size):
		try:
			data = self._rx_fifo.read(size, timeout=self.timeout)
		except queue.Empty:
			raise LinkTimeoutException
		if self.dump:
			print "<", hexlify(data).upper()
		return data


	def write(self, data):
		if self.dump:
			print ">", hexlify(data).upper()
		size = len(data)
		ofs = 0
		while size:
			chunk_sz = min(size, _write_chunk_size)
			self._dev.char_write_handle(self._wr_handle, bytearray(data[ofs:ofs+chunk_sz]))
			ofs += chunk_sz
			size -= chunk_sz


__all__ = ["BLELink"]
