from socket import *
import socket
from pip._vendor.distlib.compat import raw_input

# take input from the user indicating port number and server name
serverPort = int(input('Enter server port: '))
serverName = raw_input('Enter server name: ')
# socket.SOCK_STREAM indicates TCP
clientSocket = socket.socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
# take input from the user for file name
fileName = raw_input('Enter file name: ')
print("\nclient requesting file", fileName)
fileNameSentToServer = 'GET /' + fileName + ' HTTP/1.0\n'
clientSocket.send(fileNameSentToServer.encode())

# receiving message from server
full_msg = ''
while True:
    msg = clientSocket.recv(8)
    if len(msg) <= 0:
        break
    full_msg += msg.decode()
# this breaks up the full message line by line for printing purposes
full_msg_split = full_msg.split('\n')
# if message from server is a '400 Bad Request' message
if full_msg == 'HTTP/1.0 400 Bad Request':
    print(full_msg)
    clientSocket.close()
# if message from server is a '404 File Not Found' message
elif full_msg == 'HTTP/1.0 404 Not Found':
    print(full_msg)
    clientSocket.close()
# else, print text in to a file in the client folder
else:
    # this will remove all text that isn't content from the message received from the server
    print(full_msg_split[0])
    print(full_msg_split[1])
    msg_content = ''
    f = open(fileName, "w+")
    for i in range(3, len(full_msg_split)):
        f.write(full_msg_split[i] + '\n')
    f.close
    clientSocket.close()
