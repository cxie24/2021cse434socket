#part of the code was from the textbook


from socket import *
serverName = '127.0.0.129'
serverPort = 3555
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    message = input('Enter String:')
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    #if "exit" in message:
clientSocket.close()
