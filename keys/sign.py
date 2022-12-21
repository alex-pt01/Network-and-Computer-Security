import socket
import json


        
# operating on IPv4 addressing scheme
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM); 

# Bind and listen
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(("192.168.1.4",8002));

serverSocket.listen();

# Accept connections
while(True):

    (clientConnected, clientAddress) = serverSocket.accept();

    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));

    # Getting the certificate from client
    dataFromClient = clientConnected.recv(2048)
    
    with open('CA.crt','w') as f:
    	f.write(dataFromClient.decode())

    #print(dataFromClient);
    

    in_file = open("server.csr", "rb") # opening for [r]eading as [b]inary
    certificado = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()
    
    
    # Send the certificate, TS and nonce to the client
    clientConnected.send(certificado);
    
    
    dataFromClient = clientConnected.recv(2048)
    
    with open('server.crt','w') as f:
    	f.write(dataFromClient.decode())
    
    
    
    
    
