
import socket 
import select
import pickle
import sys 
from socket import error as SocketError
import errno

LIST = "1"
SEND = "2"
RECIEVE = "3"
EXIT = "4"
OK = "OK"

PORT = 9000

HEADER_LENGTH = 1024


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = 'localhost'
print(IP_address)	
server.connect((IP_address, PORT))
print("Connected to server ... ")

print("Enter client's name: ")
name = input()
server.send(name.encode())


while True: 

	try :

		print("Choose one of these options : 1.List 	 2.Send 	3.Receive 	4.Exit")
		
		command = input()

		server.send(command.encode())
				
		if command == LIST :

			data = server.recv(HEADER_LENGTH)
			client_list = pickle.loads(data)
			print(client_list)

		elif command == SEND :

			while True :
				print("Enter the name of your receiver:")
				receiver = input()
				server.send(receiver.encode())
				existance = (server.recv(HEADER_LENGTH)).decode()
				
				if existance != OK:
					print("Receiver not found, please try another receiver.")
					break	

				print("Enter the message: ")
				message = input()
				server.send(message.encode())
				break;


		elif command == RECIEVE :

			data = server.recv(HEADER_LENGTH)
			message_list = pickle.loads(data)
			if len(message_list) == 0 :
				print("Your inbox in empty")
			print(message_list)

		elif command == EXIT :
			print("Okay bye bye")
			exit()

		else: 
			print("Please try again ")	

	except Exception as e:
		print("Exiting")
		break
		# if e.errno != errno.ECONNRESET :
		# 	raise # Not error we are looking for
		# pass # Handle error here.



server.close() 
