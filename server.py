#!/usr/bin/env python3

import socketserver
import sys
import threading

# usage: ./server.py [PORT] [HOST]

CLIENTS = []


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

	# Class is instantiated once per connection to the server

	def handle(self):
		CLIENTS.append(self.request)
		welcomeMsg = self.client_address[0] + ":" + str(self.client_address[1]) + " joined." + '\n'
		sys.stdout.write(welcomeMsg)
		sys.stdout.flush()
		for cli in CLIENTS:
			if cli is not self.request:
				cli.sendall(welcomeMsg.encode())
		while True:
			data = self.request.recv(4096)
			if data:
				data = data.decode()
				sendMsg = self.client_address[0] + ":" + str(self.client_address[1]) + "> " + data
				sys.stdout.write(sendMsg)
				sys.stdout.flush()
				for cli in CLIENTS:
					if cli is not self.request:
						cli.sendall(sendMsg.encode())
			else:
				sendMsg = self.client_address[0] + ":" + str(self.client_address[1]) + " left." + '\n'
				sys.stdout.write(sendMsg)
				sys.stdout.flush()
				CLIENTS.remove(self.request)
				for cli in CLIENTS:
					cli.sendall(sendMsg.encode())
				break


if __name__ == "__main__":

	if len(sys.argv) == 1:
		HOST = ("localhost", 10000)
	elif len(sys.argv) == 2:
		HOST = ("localhost", int(sys.argv[1]))
	else:
		HOST = (sys.argv[2], int(sys.argv[1]))

	server = ThreadedTCPServer(HOST, ThreadedTCPRequestHandler)
	server.daemon_threads = True

	server_thread = threading.Thread(target=server.serve_forever)

	# Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()

	sys.stdout.write("Server is up." + '\n')
	sys.stdout.flush()

	# Main execution will push
	while True:
		try:
			msg = sys.stdin.readline()
			msg = "Server> " + msg
			sys.stdout.write(msg)
			sys.stdout.flush()
			for client in CLIENTS:
				client.sendall(msg.encode())

		except KeyboardInterrupt:
			break

	server.shutdown()
	server.server_close()
	sys.stdout.write("Server is closed." + '\n')
	sys.stdout.flush()
