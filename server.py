# part of the code was from the textbook

from socket import *

# data structure for storing user name and list name
register_list = {}
name_list = {}
IMlist = []
# assign the same port number
serverPort = 3666
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# bind the port to the socket
# serverSocket.bind(('10.120.70.106', serverPort))
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
    # store data and address
    message, clientAddress = serverSocket.recvfrom(2048)
    print('recieved', clientAddress)
    # takes the message from client
    modifiedMessage = message.decode()
    # get the first word to identify the command
    keyword = modifiedMessage.split(' ', 1)[0]

    if keyword == "register":
        username = modifiedMessage.split(" ")[1]
        if username not in register_list:
            register_list[username] = [modifiedMessage.split(" ")[2],
                                       modifiedMessage.split(" ")[3]]  # store to data structure
            serverSocket.sendto("Success".encode(), clientAddress)
        else:
            serverSocket.sendto("Failure".encode(), clientAddress)

    elif keyword == "create":
        listname = modifiedMessage.split(" ")[1]
        if listname not in name_list:
            name_list[listname] = []  # create a new list
            serverSocket.sendto("Success".encode(), clientAddress)
        else:
            serverSocket.sendto("Failure".encode(), clientAddress)

    elif keyword == "query-lists":
        s = str(len(name_list)) + "\n"  # return the number of names
        for x in name_list:
            s += str(x) + str(name_list.get(x)) + "\n"  # return list name as well as people in the list
        serverSocket.sendto(s.encode(), clientAddress)

    elif keyword == "join":
        tmp_listname = modifiedMessage.split(" ")[1]
        tmp_username = modifiedMessage.split(" ")[2]
        if tmp_username in register_list and tmp_listname in name_list:  # check to see if name exits
            if tmp_username not in name_list.get(tmp_listname):  # join the list
                name_list[tmp_listname].append(tmp_username)
                name_list[tmp_listname].append(register_list.get(tmp_username))
                serverSocket.sendto("Success".encode(), clientAddress)
            else:
                serverSocket.sendto("Failure".encode(), clientAddress)
        else:
            serverSocket.sendto("Failure".encode(), clientAddress)


    elif keyword == "exit":
        user_exit = modifiedMessage.split(" ")[1]
        port_exit = register_list.get(user_exit)
        if user_exit in register_list:
            del register_list[user_exit]  # remove from register list
            for x in name_list:  # remove from contact list
                if user_exit in name_list[x]:
                    name_list[x].remove(user_exit)
                    name_list[x].remove(port_exit)
                    serverSocket.sendto("Success".encode(), clientAddress)
                else:
                    serverSocket.sendto("Failure".encode(), clientAddress)
        else:
            serverSocket.sendto("Failure".encode(), clientAddress)


    elif keyword == "save":
        try:
            file_name = modifiedMessage.split(" ")[1]
            # add info to the new file
            with open("%s.txt" % file_name, "w+") as txt:
                print(len(register_list), file=txt)
                print(register_list, file=txt)
                print(len(name_list), file=txt)
                for name in name_list:
                    print(name, (int(len(name_list[name]) / 2)), file=txt)
                    print((name_list[name]), file=txt)
                serverSocket.sendto("Success".encode(), clientAddress)
        except:
            serverSocket.sendto("Failure".encode(), clientAddress)

    elif keyword == "leave":
        list_leave = modifiedMessage.split(" ")[1]
        user_leave = modifiedMessage.split(" ")[2]
        ip_leave = register_list.get(user_leave)
        for x in name_list:
            if user_leave in name_list[x]:
                name_list[x].remove(user_leave)
                name_list[x].remove(ip_leave)
                serverSocket.sendto("Success".encode(), clientAddress)
            else:
                serverSocket.sendto("Failure".encode(), clientAddress)

    elif keyword == "im-start":
        list_im = modifiedMessage.split(" ")[1]
        user_im = modifiedMessage.split(" ")[2]
        IMstartname = user_im
        IMstartlist = list_im

        if list_im not in name_list:
            serverSocket.sendto("0".encode(), clientAddress)  # return 0 , command fail
            break
        else:
            if user_im in name_list[list_im]:  # if name exist
                output = ["Number of contact: " + str(len(name_list[list_im])/2) + '\n']

                for name in name_list[list_im]:
                    if name is user_im:
                        output.append(str(name) + str(register_list.get(str(name))) + '\n')  # get first name

                for name in name_list[list_im]:
                    if name is not user_im and type(name) is str:
                        output.append(str(name) + str(register_list.get(str(name))) + '\n')  # get the rest names

                serverSocket.sendto(" ".join(output).encode(), clientAddress)  # send contact list

                modifiedMessage, clientAddress = serverSocket.recvfrom(2048)

                print("Received: " + modifiedMessage.decode())
                i = 0
                for name in name_list[list_im]:
                    if type(name) is str:
                        IMlist.append(name)  # add to list
                        i += 2
                        if name is not user_im:
                            #print
                            if i >= len(name_list[list_im]) - 1:
                                sentmeg = [user_im + ' sent:' + modifiedMessage.decode() + '\nsent to' + user_im + ' at ' + " ".join(register_list.get(str(user_im)))]
                            else:
                                temp = name_list[list_im][i]
                                sentmeg = [temp + ' sent:' + modifiedMessage.decode() + '\nsent to' + user_im + ' at ' + " ".join(register_list.get(str(temp)))]

                            temp_address = (register_list.get(str(name))[0], int(register_list.get(str(name))[1]))
                            serverSocket.sendto(" ".join(sentmeg).encode(), temp_address)

                serverSocket.sendto("Success".encode(), clientAddress)






    elif keyword == "im-complete":
        imcompcontactlist = modifiedMessage.split(" ")[1]
        imcompcontactname = modifiedMessage.split(" ")[2]
        if IMstartname == imcompcontactname and IMstartlist == imcompcontactlist:
            IMlist = []
            serverSocket.sendto("Success".encode(), clientAddress)
        else:
            serverSocket.sendto("Failure".encode(), clientAddress)

    print(register_list)  # print all names
