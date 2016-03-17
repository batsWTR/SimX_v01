# Class that read Simx configuration file
# it must contain:
# PORT=8090
# IP=192.168.1.20
# // comment lines
# list of var from uipcxdatos.txt
# 







class SimxConf() :
	'''open simx.conf and extractdatas IP, PORT et VAR iocp'''
	def __init__(self, file) :
		self.confFile = file
		self.port = None
		self.ip = None
		self.var = {} # list



	def get (self) :
		""" open file and get datas """
		print("Open ",self.confFile)

		'''Ouverture fichier'''
		try:
			fichier = open(self.confFile, "r")
		except:
			print("File does not exist")
			return None

		# read datas
		lire = True
		while lire:
			ligne = fichier.readline()
			#p if end of file
			if ligne == "":
				lire = False
			# if port
			elif ligne[0] == 'P':
				index = ligne.index('=')
				port = ligne[index+1:-1]
				port = port.strip()
				self.port = int(port)
			# if IP
			elif ligne[0] == 'I':
				index = ligne.index('=')
				ip = ligne[index+1:-1]
				ip = ip.strip()
				self.ip = ip
			# if empty line
			elif ligne[0] == "\n":
				pass
			# if comment
			elif ligne[0] == '/':
				pass
			# if var line
			else:
				tmp = ligne.split("	")
				var = int(tmp[0])
				var2 = tmp[1].split('/')
				self.var[var] = var2[-1]
			


		fichier.close()
		print("Close ",self.confFile)
		print("ip: ", self.ip)
		print("port: ",self.port)
		print('---- Vars List ----')
		for var, name in self.var.items():
			print(var,' -> ',name)
		# returns int
		return 0



	def getPort (self) :
		""" return port """
		# returns int
		return self.port

	def getIp (self) :
		""" return IP """
		# returns String
		return self.ip

	def getVar (self) :
		""" return var list """
		# returns list
		return self.var

