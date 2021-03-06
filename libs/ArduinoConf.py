# Classe ArduinoConf
# lit le fichier de description des modules arduino
# Constructeur avec le nom du fichier de conf
# fn get() -> lit le fichier, remplie liste module [NAME,PORT,[VAR]], referme le fichier 
# fn getModule() -> renvoie la liste des module contenu dans le fichier de conf
# fn getConModule() -> renvoie la liste des modules connectes

from glob import glob
import serial
import time


# initialise la classe avec le chemin du fichier de conf
class ArduinoConf :
	'''Ouvre le fichier arduino.conf et extrait le nom du module, son port et les variables necessaire.'''
	def __init__(self, confFile) :
		self.confFile = confFile # String
		self.listeModule = [] # list
		self.fichier = 0  # file descriptor
		

	def get (self) :
		""" recuperation des donnees, renvoie -1 si pb """
		try:
			self.fichier = open(self.confFile,"r")
			print("Ouverture du fichier ",self.confFile)
		except:
			print("Erreur, le fichier n existe pas")
			return -1


		lire = True
		while lire:
			ligne = self.fichier.readline()
			if ligne == "":
				lire = False
				print("Fin du fichier", self.confFile)
			elif ligne[0] == '[':
				print("Lecture module...")
				self.litModule()
			elif ligne[0] == " ":
				pass


		

		self.fichier.close()
		print("Fermeture du fichier conf")
		print()
		# returns int
		return 0
		pass

#---------------------------------------------------------------------
# fonction integree a get()

	def litModule (self) :  #   aaaaaaaaaaaaaaaaa
		""" lit les ligne de def module et ajoute a listeModule """
		tmpliste = []
		ligne = " "

		while ligne == "" or ligne[0] != ']':
			ligne = self.fichier.readline()
			tmp = ligne[0:4]
			if tmp == "NAME":
				index = ligne.index('=')
				tmp = ligne[index + 1:-1]
				tmp = tmp.strip()
				tmpliste.append(tmp) 
				
			
				ligne = self.fichier.readline()
				tmp = ligne[0:4]
				if tmp == "PORT":
					index = ligne.index('=')
					tmp = ligne[index + 1: -1]
					tmp = tmp.strip()
					tmpliste.append(tmp)   
			
					ligne = self.fichier.readline()
					tmp = ligne[0:3]
					if tmp == "VAR":
						index = ligne.index('=')
						tmp = ligne[index + 1: -1]
						tmp = tmp.strip()
						tmp = tmp.split(',')
						tmpliste.append(tmp)
						self.listeModule.append(tmpliste)
						ligne = self.fichier.readline()    

				


		


#---------------------Retourne tous les modules-----------------------------------


	def getModule (self) :
		""" retourne la liste listeModule """
		# returns list
		return self.listeModule
		


#------------Retourne les modules connectes
	def getConModule(self) :
		""" retourne la liste des modules connectes au systeme"""
		# vars
		serie = 0	# descripteur connexion serie
		recv = 0	# var reception du nom
		listeMod = list()	# liste des module ok


		# liste les port usb connectes
		listeTty = glob("/dev/ttyUSB*")
		

		# Connexion de chaque port serie trouve, double connexion serie du au reset de l arduino
		for port in listeTty:

			try:
				serie = serial.Serial(port,baudrate=57600, timeout=0)
				print("connexion sur " , port)
			except:
				print("Erreur de connexion sur " , port)
				break
		# Ligne de demande du nom du module
			var = "xx:name=?:\r"
			var = var.encode("ASCII")
			time.sleep(2)


		# Envoie de la ligne au module
			try:
				serie.write(var)
				
			except:
				print("Impossible d'envoyer a " , port)
				serie.close()
				break
			
		# Lecture du nom renvoye
			time.sleep(5)
			try:
				recv = serie.readline()
			except:
				print("Erreur de lecture sur " , port)
				serie.close()
				return

		

		# test du nom et effacement de \r\n
			recv = recv.decode()

			if recv != " ":
				recv = recv[:-2]
			print("Detection de ", recv)

		# recherche le nom dans la liste des modules
			tmp = [0,0,0]
			for liste in self.listeModule:
				if liste[0] == recv:
					tmp[0] = liste[0]
					tmp[1] = port
					tmp[2] = liste[2]
					listeMod.append(tmp)

			
			serie.close()
					
		return listeMod










