#!/usr/bin/env python3

import select
import socket
import sys

# usage: ./client.py [PORT] [HOST]

if __name__ == "__main__":

	if len(sys.argv) == 1:
		HOST = ("localhost", 10000)
	elif len(sys.argv) == 2:
		HOST = ("localhost", int(sys.argv[1]))
	else:
		HOST = (sys.argv[2], int(sys.argv[1]))

	main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		main_socket.connect(HOST)
		sys.stdout.write("Connected to " + HOST[0] + ":" + str(HOST[1]) + '\n')
		sys.stdout.flush()
	except:
		sys.stdout.write("Could not connect to " + HOST[0] + ":" + str(HOST[1]) + '\n')
		sys.stdout.flush()
		exit(2)

	while True:
		read_buffers = [sys.stdin, main_socket]
		try:
			read_list, write_list, error_list = select.select(read_buffers, [], [])

			for sock in read_list:
				if sock == main_socket:
					data = sock.recv(4096)
					if data:
						data = data.decode()
						sys.stdout.write(data)
						sys.stdout.flush()
					else:
						print("Disconnected from server!")
						exit(2)
				else:
					msg = sys.stdin.readline()
					sys.stdout.write("You> " + msg)
					sys.stdout.flush()
					main_socket.send(msg.encode())

		except KeyboardInterrupt:
			print("Disconnected from server!")
			exit(1)
