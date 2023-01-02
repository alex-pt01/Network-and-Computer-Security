#----- A simple TCP client program in Python using send() function -----

import socket
import subprocess
from sys import argv

if len(argv) != 2:
    print("INVALID NUMBER OF ARGUMENTS, YOU SHOULD PUT THE NAME receive_signature.py PLUS <name_of_request>.csr")
	
else:
	# Create a client socket

	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	# Connect to the server
	print("GOING")
	clientSocket.connect(("192.168.0.100",7555))
	print("IN")
	# Send data to server
	dataFromServer = clientSocket.recv(2048)
	with open('CA.crt','w') as f:
		f.write(dataFromServer.decode())

	in_file = open(argv[1], "rb") # opening for [r]eading as [b]inary
	certificado = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
	in_file.close()


	# Send the certificate, TS and nonce to the client
	clientSocket.send(certificado)


	dataFromClient = clientSocket.recv(2048)

	nama_of_crt=argv[1].split(".")[0]
	with open(nama_of_crt+".crt",'w') as f:
		f.write(dataFromClient.decode())

