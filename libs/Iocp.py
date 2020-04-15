# This class is used to connect to the UIPC	server through an IOCP protocol
# First, connect to server with the "Connect" function with IP address an Port (8090)
# Register the list of all variable you wwish to receive with "Register" function with the list of variables 
# as parameter.
# "Recv" function allow you to receive an update in case of variable change as a dict: [number][var]
# "Send" function allow you to change a variable, it send a dict to the class [number][var]
# Close function will close the connection to the server
#		IOCP Protocol
#  connect: Server send welcome message -> Arn.Tiposrv:xxxx:CRLF
#  register: client send Arn.Inicio:11:12:13:17:CRLF
# server response or if client want to change a variable Arn.Resp:1=112:5=554:CRLF
# to stop communication in both way: Arn.Fin:CRLF
# client can ask a variable even if he's not register: Arn.Preg:1:4:33:CRLF



# IOCP ver 2 2020

# written by B.Wentzler baptiste.wentzler@wanadoo.fr


import socket
import time



class Iocp:
	""" This class is used to connect to an UIPC server"""

	def __init__(self,IP = "", Port = 0):
		self.IP = IP
		self.Port = Port
		self.s  = 0
		self.listRegister = list()
		self.isConnected = False

	def remplieDict(self, line, dico):
		lineList = line.split('=')
		num = lineList[0]
		val = lineList[1]
		dico[num] = val
		


	def connect(self,IP="", Port= 0):
		""" This function is used to establish the connection, give it the IP and Port"""
		if self.IP == "": self.IP = IP
		if self.Port == 0: self.Port = Port
		print('Try to connect to ',self.IP, self.Port,"......")
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setblocking(0)
		self.s.settimeout(2.0)
		try:
			self.s.connect((self.IP,self.Port))
			data = self.s.recv(1024)
			self.isConnected = True
			print("Connexion with ",self.IP,"established\n\n\n")
			data = data.decode()
			return 0
		except:
			print("Connexion error")
			self.isConnected = False
			return -1
		
		
	def is_connected(self):
		""" are we connected to the server ?"""
		return self.isConnected


	def register(self,register):
		""" Register to the server with a list of variable as parameter"""
		if len(register) == 0 or self.isConnected == False:
			print("Unable to register")
			return -1


		self.listRegister = register
		reg = "Arn.Inicio:"
		for l in self.listRegister:
			reg = reg + str(l) + ":"
		reg = reg + "\r\n"
		print("Registration of: " + reg)
		reg = reg.encode()
		
		# send data to register
		self.s.send(reg)
		time.sleep(1)

		# values from registration
		reg = self.recvData()
		print("Registration from server: " + str(reg))
		return reg
		


	def recvData(self):
		""" Look if something comes from server, the function returns a dict ["number"]["var"] or -1"""
		dataDict = {}

		try:
			data = self.s.recv(1024)
		except:
			return -1
		

		# test server connexion""
		if(len(data) == 0):
			print("No connexion with server")
			return -1
			
		data = data.decode()
		data = data.split("\n")
		for i in data:
			if i.find("\r") != -1:
				if i.find("A") != -1:
					tmpList = i.split(':') 	
					tmpList.pop(0)
					tmpList.pop()   
					for n in tmpList:
						self.remplieDict(n, dataDict)


		return dataDict




	def sendData(self,var,val):
		""" If client want to mofify a registered variable var = char, val = char"""

		resp = "Arn.Resp:"
		resp = resp + var + "=" + val + ":" + "\r\n"
		resp = resp.encode()
		
		if self.isConnected:
	 		self.s.sendall(resp)
		print("Sending: " + str(resp))
		return

	
	def close(self):
		""" This function will close the connection"""
		print("Connexion with server closed")
		if self.isConnected:
			fin = "Arn.Fin:\r\n"
			fin = fin.encode()
			self.s.send(fin)
			self.s.close()
			self.isConnected = False



def main():
	print("main")
	iocp = Iocp()
	while iocp.connect("127.0.0.1", 8090) == -1:
		time.sleep(2)
	iocp.register([500,501,502,503,510])
	while 1:
		print(iocp.recvData())
		time.sleep(2)





if __name__ == "__main__":
	main()







		
