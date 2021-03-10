#part of the code was from the textbook


from socket import *
#set the hostname and port

serverName = '10.120.70.106'
serverPort = 3666
#creates the clients socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientPort = int(input("Enter client port:"))
clientSocket.bind(('', clientPort))


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

    if "im-start" == message.split(" ")[0]:
        meg = input('Text Message: ')
        print("Sent: " + meg)
        clientSocket.sendto(meg.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        if modifiedMessage.decode() == "Success":
            print("server received")
