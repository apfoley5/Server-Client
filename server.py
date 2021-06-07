from socket import*
import socket
import os

#socket.SOCK_STREAM indicates TCP
serverPort = int(input('Enter server port: '))
serverName = 'localhost'
serverSocket = socket.socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print('The server is ready to receive\n')

while True:
    (connectionSocket, address) = serverSocket.accept()
    #received from client
    fileNameFromClient = connectionSocket.recv(1024).decode()
    print('Request from client: ' + fileNameFromClient)
    fileNameFromClientSplit = fileNameFromClient.split()
    #this isolates the text in the request that indicates the name of the file
    file = fileNameFromClientSplit[1]
    file = file[1:]

    #this section tests if the client's request has the proper format
    badFormatMsg = ''
    if fileNameFromClientSplit[0] != 'GET':
        badFormatMsg = 'HTTP/1.0 400 Bad Request'
        print('HTTP/1.0 400 Bad Request\n')
        connectionSocket.send(badFormatMsg.encode())
        connectionSocket.close()
    elif fileNameFromClientSplit[2] != 'HTTP/1.0':
        badFormatMsg = 'HTTP/1.0 400 Bad Request'
        print('HTTP/1.0 400 Bad Request\n')
        connectionSocket.send(badFormatMsg.encode())
        connectionSocket.close()
    else:
        print('Open file: ' + file)
        #this handles whether or not the file exists
        #if the file exists then open it
        fileNotFoundMsg = ''
        try:
            f = open(file, "r")
            fileReal = True
        except FileNotFoundError:
            fileReal = False
            print('HTTP/1.0 404 Not Found\n')
            fileNotFoundMsg = 'HTTP/1.0 404 Not Found'
            connectionSocket.send(fileNotFoundMsg.encode())
            connectionSocket.close()

        if (fileReal == True):
            if f.mode == 'r':
                contents = f.read()
            # this determines the file size
            def file_size(fname):
                statinfo = os.stat(fname)
                return statinfo.st_size
            # the whole message to be sent to the client
            msg = 'HTTP/1.0 200 OK\n' + 'Content-Length: ' + str(file_size(file)) + ' bytes\n\n' + contents
            # send to client
            connectionSocket.send(msg.encode())
            connectionSocket.close()
