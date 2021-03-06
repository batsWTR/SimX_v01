import serial
import time






class Arduino :
	'''Se connecte a un module et lui envoie les donnees qui changent'''
	def __init__(self, liste) :
		self.nom = liste[0] # String
		self.port = liste[1] # String
		self.listeVar = liste[2] # List
		self.dictVar = {}  # Dictionnaire des variables
		self.serie = 0  #port serie
		pass
	def connection (self) :
		''' double connection au module Arduino par le port serie et met a zero toutes le 
		variable, retourne -1 si pb'''

		# Connexion
		print("Connexion au module",self.nom)

		#try:
		#	self.serie = serial.Serial(self.port)
		#except:
		#	print("Erreur de connexion sur",self.nom)
		#	return -1
		#print("Connexion reussie sur", self.port)

		#self.serie.setDTR(False)
		#time.sleep(3)
		#self.serie.flushInput()
		#self.serie.setDTR(True)

		try:
			self.serie = serial.Serial(self.port,baudrate=57600, timeout=0)
		except:
			print("Erreur de connexion sur",self.nom)
			return -1
		print("Connexion reussie sur", self.port)

		time.sleep(2)



		# Mise a zero du dictionnaire Attention pas de tests de la liste
	
		
		for var in self.listeVar:
			self.dictVar[var] = '0'    # mise a zero par caractere 0
		return 0

	def updateData (self, dictUpdate) :
		'''  Prend en parametre les donnees qui ont changees, les envoient a 
		l arduino et met a jour self.dictVar'''

		# met a jour self.dictVar
		for cle, val in dictUpdate.items():
			if self.dictVar[cle] == val:
				dictUpdate.pop[cle]
			self.dictVar[cle] = val

		if len(dictUpdate) == 0:
			return



		# Envoie NOM:var=val:var=val:\r a l Arduino
		var = self.nom + ':' 
		for cle,val in dictUpdate.items():
			var += cle + '=' + val + ':'
		var += '\r'
	
		# Conversion str -> ASCII
		var = var.encode("ASCII")
		try:
			self.serie.write(var)
			print("To Arduino:",var)
		except:
			print("Impossible d envoyer les donnees sur",self.port)
			return -1
		# returns int
		return 0
		

	def getToUpdate (self) :
		''' Retourne le dictionnaire des valeurs actuelles'''
		# returns Dict
		return self.dictVar

	def calibrate(self,valeur):
		print("Envoie de ",valeur, " a ",self.nom)
		envoie = self.nom + ":cal=" + str(valeur) + ":"
		envoie += '\r'
		envoie = envoie.encode("ASCII")
		self.serie.write(envoie)
		pass

	def closeSerie (self) :
		print("Fermeture de la connexion sur",self.port)
		if self.serie != 0:
			self.serie.close()
	


def main():
	ard = Arduino(["VOR","/dev/ttyUSB0",["609"]])
	ard.connection()
	ard.closeSerie()


if __name__ == "__main__":
	main()