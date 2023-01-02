import socket
import json
import subprocess


        
# operating on IPv4 addressing scheme
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM); 

# Bind and listen
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(("192.168.0.100",7555))

serverSocket.listen()

# Accept connections
while(True):

    print("WAITING")
    (clientConnected, clientAddress) = serverSocket.accept()

    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
    # SEND THE CA CERTIFICATE
    in_file = open("CA.crt", "rb") # opening for [r]eading as [b]inary
    data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()

    clientConnected.send(data)


    # Getting the certificate from client
    dataFromClient = clientConnected.recv(2048)

    with open('server.crt','w') as f:
        f.write(dataFromClient.decode())

    #print(dataFromClient);
    output = subprocess.check_output("openssl x509 -req -days 365 -in server.csr -CA CA.crt -CAkey CA.key -out server.crt", shell=True)
    # Print to the console
    #print(dataFromServer.decode());

    in_file = open("server.crt", "rb") 
    data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()

    clientConnected.send(data)


