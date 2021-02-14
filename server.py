#part of the code was from the textbook

from socket import *

#dict for registered contact-name database
register = {}

#dict for contact-list-name database
conlistname = {}



serverPort = 3555
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
 message, clientAddress = serverSocket.recvfrom(2048)
 print('recieved',clientAddress)
 modifiedMessage = message.decode()
 keyword = modifiedMessage.split(' ',1)[0]

 if keyword == "register":
  contactname = modifiedMessage.split(" ")[1]
  ip = modifiedMessage.split(" ")[2]
  port = modifiedMessage.split(" ")[3]
  if contactname not in register:
   register[contactname] = [ip, port]
   serverSocket.sendto("Success".encode(), clientAddress)
  else:
   serverSocket.sendto("Failure".encode(), clientAddress)

 elif keyword == "create":
  contactlistname = modifiedMessage.split(" ")[1]
  if contactlistname not in conlistname:
   conlistname[contactlistname] = []  # create a empty list for the name(as dict key)
   serverSocket.sendto("Success".encode(), clientAddress)
  else:
   serverSocket.sendto("Failure".encode(), clientAddress)

 elif keyword == "query-lists":
  returnstr = str(len(conlistname)) + " " + str(conlistname.keys())
  serverSocket.sendto(returnstr.encode(), clientAddress)

 elif keyword == "join":
  contactlistname2 = modifiedMessage.split(" ")[1]
  contactname2 = modifiedMessage.split(" ")[2]
  if contactname2 in register:  # check to see if the contact name is registered
   if contactlistname2 in conlistname:  # check to see if the contact-name-list exists
    if contactname2 not in conlistname.get(contactlistname2):  # check to see if the contact name is already in the contact-name-list
     conlistname[contactlistname2].append(contactname2)
     conlistname[contactlistname2].append(register.get(contactname2))
     serverSocket.sendto("Success".encode(), clientAddress)
    else:
     serverSocket.sendto("Failure".encode(), clientAddress)
   else:
    serverSocket.sendto("Failure".encode(), clientAddress)
  else:
   serverSocket.sendto("Failure".encode(), clientAddress)


 elif keyword == "exit":
  exitcontactname = modifiedMessage.split(" ")[1]
  exitIPandport = register.get(exitcontactname)
  del register[exitcontactname]
  for key in conlistname:
   if exitcontactname in conlistname[key]:
    conlistname[key].remove(exitcontactname)
    conlistname[key].remove(exitIPandport)
    serverSocket.sendto("Success".encode(), clientAddress)
   else:
    serverSocket.sendto("Failure".encode(), clientAddress)


 elif keyword == "save":
  with open("file-name.txt", "w") as text_file:
   print(len(register), file=text_file)
   print(register, file=text_file)
   print(len(conlistname), file=text_file)
   for key2 in conlistname:
    print(key2, (len(conlistname[key2]) / 2), file=text_file)

   serverSocket.sendto("Success".encode(), clientAddress)



 print(register)  # print all registered contact-names
 #serverSocket.sendto(modifiedMessage.encode(), clientAddress)

