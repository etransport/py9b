class LinkTimeoutException(Exception):
	pass

class LinkOpenException(Exception):
	pass

class BaseLink(object):
	DEF_TIMEOUT = 1

	def __init__(self, timeout=DEF_TIMEOUT, dump=False):
		self.dump = dump
		self.timeout = timeout
	

	def scan(self):
		raise NotImplementedError()


	def open(self, port):
		raise NotImplementedError()

		
	def close(self):
		pass		


	def read(self, size):
		raise NotImplementedError()

	def write(self, data):
		raise NotImplementedError()
	

__all__ = ["LinkTimeoutException", "LinkOpenException", "BaseLink"]
