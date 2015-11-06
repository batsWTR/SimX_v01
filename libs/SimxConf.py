class SimxConf() :
	'''ouverture du fichier simx.conf et extraction des donnees IP, PORT et VAR iocp'''
	def __init__(self, file) :
		self.confFile = file
		self.port = 0 # int
		self.ip = " " # String
		self.var = {} # dict
		pass


	def get (self) :
		""" ouverture du fichier et recuperation des donnees """
		print("Overture du fichier ",self.confFile)

		'''Ouverture fichier'''
		try:
			fichier = open(self.confFile, "r")
		except:
			print("Le fichier n existe pas")
			return -1

		'''Lecture des info'''
		lire = True
		while lire:
			ligne = fichier.readline()
			#print(ligne)
			if ligne == "":
				lire = False
			elif ligne[0] == 'P':
				index = ligne.index('=')
				port = ligne[index+1:-1]
				self.port = int(port)
			elif ligne[0] == 'I':
				index = ligne.index('=')
				ip = ligne[index+1:-1]
				self.ip = ip
			elif ligne[0] == "\n":
				pass
			elif ligne[0] == '/':
				pass
			else:
				tmp = ligne.split("	")
				var = int(tmp[0])
				var2 = tmp[1].split('/')
				self.var[var] = var2[-1]
			


		fichier.close()
		print("Fermeture de ",self.confFile)
		# returns int
		return 0



	def getPort (self) :
		""" retourne le port """
		print("port: ",self.port)
		# returns int
		return self.port
		pass
	def getIp (self) :
		""" retourne l IP """
		print("ip: ", self.ip)
		# returns String
		return self.ip
		pass
	def getVar (self) :
		""" retourne la liste des variables """
		#print("var: ", self.var)
		# returns list
		return self.var
		pass
