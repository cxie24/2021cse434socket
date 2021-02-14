#part of the code was from the textbook


from socket import *
#set the hostname and port
serverName = '192.168.2.122'
serverPort = 3554
#creates the clients socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    message = input('Enter String:')
    #convert to byte
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    #store the address and data
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    if "exit" == message.split(" ")[0]:
        if modifiedMessage.decode() == "Success":
            clientSocket.close()
            break
