"""TCP-BLE bridge link"""
from __future__ import absolute_import
import socket
from binascii import hexlify
from .base import BaseLink, LinkTimeoutException, LinkOpenException

HOST, PORT = "127.0.0.1", 6000


def recvall(sock, size):
	data = ""
	while len(data)<size:
		try:
			pkt = sock.recv(size-len(data))
		except socket.timeout:
			raise LinkTimeoutException()
		data+=pkt
	return data


class TCPLink(BaseLink):
	def __init__(self, *args, **kwargs):
		super(TCPLink, self).__init__(*args, **kwargs)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(self.timeout)
		self.connected = False


	def __enter__(self):
		return self


	def __exit__(self, exc_type, exc_value, traceback):
		self.close()


	def scan(self):
		res = [("Android UART Bridge", (HOST, PORT))]
		return res


	def open(self, port):
		try:
			self.sock.connect(port)
		except socket.timeout:
			raise LinkOpenException
		self.connected = True


	def close(self):
		if self.connected:
			self.sock.close()
			self.connected = False


	def read(self, size):
		data = recvall(self.sock, size)
		if data and self.dump:
			print "<", hexlify(data).upper()
		return data


	def write(self, data):
		if self.dump:
			print ">", hexlify(data).upper()
		self.sock.sendall(data)


__all__ = ["TCPLink"]
