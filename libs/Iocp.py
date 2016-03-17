# This class is used to connect to the UIPC	server through an IOCP protocol
# First, connect to server with the "Connect" function with IP address an Port (8090)
# Register the list of all variable you wwish to receive with "Register" function with the list of variables 
# as parameter.
# "RecvData" function allow you to receive an update in case of variable change as a dict: [number][var]
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

	def __init__(self, ip = None, port = None):
		self.IP = ip
		self.Port = port
		self.s  = 0
		self.listRegister = list()
		self.isConnected = False
		self.server_name = None

	def remplieDict(self, line, dico):
		lineList = line.split('=')
		num = lineList[0]
		val = lineList[1]
		dico[num] = val
		


	def connect(self,IP= None, Port= None):
		""" This function is used to establish the connection, give it the IP and Port return server name if ok or None"""

		if IP is not None:
			self.IP = IP
		if Port is not None:
			self.Port = Port

		print('IOCP: Essai de connexion sur',self.IP, self.Port,"......")
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.settimeout(2)

		# try to connect to server
		try:
			self.s.connect((self.IP,self.Port))
			server_name = self.s.recv(1024)
			# if receive empty string
			if (server_name == b' '):
				self.isConnected = False
				print('IOCP: Unable to receive server name')
				return None
			self.isConnected = True
			print("IOCP: Connexion avec",self.IP,"etablie")
			server_name = server_name.decode()
			serverList = server_name.split(':')
			self.server_name = serverList[1]
			return self.server_name
		except:
			print("IOCP: Erreur de connexion")
			self.isConnected = False
			return None
		
		



	def register(self,register):
		""" Register to the server with a list of variable as parameter and returna dict with initial values or None if unable to register"""

		# if register is empty -> return None
		if len(register) == 0 or self.isConnected == False:
			return None
		self.listRegister = register



		# the register line to send to server								
		registerLine = "Arn.Inicio:"
		for l in self.listRegister:
			registerLine = registerLine + str(l) + ":"
		registerLine = registerLine + "\r\n"
		registerLine = registerLine.encode()

		print('IOCP: try to register to ', self.server_name)
		# try to send datas
		try:
			self.s.send(registerLine)
		except:
			print('IOCP: Unable to send register vars')
			return None

		# try to receive
		data = None
		try:
			data = self.s.recv(1024)
		except:
			print('IOCP: Unable to receive initials datas')
			return None

		data = data.decode()
		

		# Split received data separated by :
		tmpList = data.split(':') 	
		# remove first index Arn.resp:
		tmpList.pop(0)
		# remove last index :CRLF
		tmpList.pop()   # ATTENTION

		print('IOCP: Datas registered to serveur: ',tmpList)
		
		dataDict = {}
		for n in tmpList:
			self.remplieDict(n, dataDict)

		# set non blocking mode 
		self.s.settimeout(0.0)

		return dataDict


	def recvData(self):
		""" Look if something comes from server, the function returns a dict [number][var] or None"""
		dataDict = {}
		
		# test if new data comes
		try:
			data = self.s.recv(1024)
		except:
			return None

		# test data len
		if(len(data) == 0):
			return None

		#print(data)
		data = data.decode() 
		tmpList = data.split(':') 	
		tmpList.pop(0)
		tmpList.pop()   # ATTENTION
		for n in tmpList:
			self.remplieDict(n, dataDict)


		return dataDict


	def recvRaw(self):
		'''Test for fata receive and return None or data string'''
		pass



	def sendData():
		""" If client want to mofify a registered variable"""
		pass
	
	def close(self):
		""" This function will close the connection"""
		print("IOCP: Connexion closed")
		if self.isConnected:
			fin = "Arn.Fin:\r\n"
			fin = fin.encode()
			self.s.send(fin)
			self.s.close()


#------------------------------------------------------------










		
