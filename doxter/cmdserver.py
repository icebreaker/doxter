# -*- coding: utf-8 -*-
import os
import SimpleHTTPServer
import SocketServer

class CmdTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	daemon_threads = True
	allow_reuse_address = True

	def __init__(self, server_address, RequestHandlerClass):
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

class CmdServer(object):
	def __init__(self, port=4000):
		self.httpd = CmdTCPServer(('', port), SimpleHTTPServer.SimpleHTTPRequestHandler)

	def serve(self, public_dir):
		os.chdir(public_dir)

		try:
			self.httpd.serve_forever()
		except OSError:
			self.shutdown()
		except KeyboardInterrupt:
			self.shutdown()

		return 0

	def shutdown(self):
		print('\nBye, Bye ...')
		self.httpd.shutdown();
