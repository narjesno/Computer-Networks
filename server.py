
import socket
import pickle
import select 
import sys
import threading 
from _thread import start_new_thread


HEADER_LENGTH = 1024

LIST = "1"
SEND = "2"
RECEIVE = "3"
EXIT = "4"
OK = "OK"
OH = "NOT OK"
client_list = []

class Message:

	def	__init__(self, sender, message):
		self.sender = sender
		self.message = message

class Client:

	def __init__(self,client_address,client_socket):
		global client_list
		self.socket=client_socket
		self.address = client_address
		self.messages = []
		client_list.append(self)
		print (f"{client_address} connected")

	def set_name(self, name):
		self.client_name = name

	def kill_session(self):
		global client_list
		client_list.remove(self)

	def send(self, data):
		self.socket.send(data)

	def recv(self):
		return self.socket.recv(HEADER_LENGTH).decode()

	def get_name(self):
		return self.client_name

	def insert_message(self, message):
		self.messages.append(message)

	def get_messages(self):
		message_list = []
		for message in self.messages:
			message_str = message.sender + " : " + message.message
			message_list.append(message_str)
		return message_list


def run(client):

	global client_list

	client_name = client.socket.recv(HEADER_LENGTH).decode()
	if not client_name:
		print("Client closed connection")
		client.kill_session()
		return

	print(client_name)
	client.set_name(client_name)


	while True:

		command = client.recv()
		print(command)
		if not command:
			client.kill_session()
			print("client closed connection")
			break

		if command == LIST :

			client_names = []
			for client in client_list:
				client_names.append(client.get_name())
			data = pickle.dumps(client_names)
			client.send(data)

		elif command == SEND:

			receiver = client.recv()
			receiver_client = None

			for cl in client_list:
				if cl.get_name() == receiver:
					receiver_client = cl
			if receiver_client is None:
				client.send(OH.encode())
				continue
			else:
				client.send(OK.encode())

			message = client.recv()
			print(message)
			client_message = Message(client.get_name(), message)
			receiver_client.insert_message(client_message)

			print("message inserted")

		elif command == RECEIVE:
			message_list = client.get_messages()
			print(message_list)
			data = pickle.dumps(message_list)
			client.send(data)


		elif command == EXIT:
			print (str(client_name) + " disconnected.")
			client.kill_session()
			break
		else :
			print("None of the above :/ puta ")


#reserve a port on your computer, in our case :9000 . can be anyhting

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.TCPServer.allow_reuse_address = True
print ("Server Socket successfully created")



IP_address = 'localhost'
Port = '9000' 


server.bind((IP_address, int(Port)))	

#put socket into listening mode

server.listen(5) 

print(f"Listening for connections on {IP_address}:{Port}...")

#forever loop until client wants to exit

while True: 
	try:
		c, address = server.accept()
		#print(client)
		#client.settimeout(60)

		start_new_thread(run, (Client(address, c),))


	except Exception as e:
		print("Exiting")
		break

print("Closing server socket")
server.close()



