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





# written by B.Wentzler baptiste.wentzler@wanadoo.fr


import socket



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
		self.IP = IP
		self.Port = Port
		print('Essai de connexion sur',self.IP, self.Port,"......")
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.s.settimeout(5.0)
		try:
			self.s.connect((self.IP,self.Port))
			data = self.s.recv(1024)
			self.isConnected = True
			print("Connexion avec",self.IP,"etablie")
			data = data.decode()
			return 0
		except:
			print("Erreur de connexion")
			self.isConnected = False
			return -1
		
		



	def register(self,register):
		""" Register to the server with a list of variable as parameter"""
		if len(register) == 0 or self.isConnected == False:
			return -1
		self.listRegister = register
		reg = "Arn.Inicio:"
		for l in self.listRegister:
			reg = reg + str(l) + ":"
		reg = reg + "\r\n"
		reg = reg.encode()
		self.s.send(reg)
		data = self.s.recv(1024)
		print(data)
		data = data.decode() 
		tmpList = data.split(':') 	
		tmpList.pop(0)
		tmpList.pop()   # ATTENTION
		dataDict = {}
		for n in tmpList:
			self.remplieDict(n, dataDict)

		return dataDict


	def recvData(self):
		""" Look if something comes from server, the function returns a dict [number][var]"""
		dataDict = {}

		data = self.s.recv(1024)

		# test la connexion au serveur est coupé, renvoie ""
		if(len(data) == 0):
			self.isConnected = False
			print("Perte de la connexion au serveur")
			return -1
		print(data)
		data = data.decode() 
		tmpList = data.split(':') 	
		tmpList.pop(0)
		tmpList.pop()   # ATTENTION
		for n in tmpList:
			self.remplieDict(n, dataDict)


		return dataDict




	def sendData():
		""" If client want to mofify a registered variable"""

	
	def close(self):
		""" This function will close the connection"""
		print("Connexion terminee")
		if self.isConnected:
			fin = "Arn.Fin:\r\n"
			fin = fin.encode()
			self.s.send(fin)
			self.s.close()


#------------------------------------------------------------










		
