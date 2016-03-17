# Class ArduinoConf
# read description file of arduino modules
# 
# fn get() -> read file, fill module list [NAME,PORT,[VAR]], close file 
# fn getModule() -> return module list
# fn getConModule() -> return list of connected modules

from glob import glob
import serial
import time


class ArduinoConf :	
	def __init__(self, confFile) :
		'''Open file arduino.conf and extract module name and module vars'''
		self.confFile = confFile # String
		self.listeModule = [] # list
		self.fichier = None

	def get (self) :
		"""read file and get datas, return None if problem or 1 if ok """
		try:
			self.fichier = open(self.confFile,"r")
			print("Open ",self.confFile)
		except:
			print("Error, file does not exist")
			return None
		lire = True
		while lire:
			ligne = self.fichier.readline()
			# if end of file
			if ligne == "":
				lire = False
			# if module begin
			elif ligne[0] == '[':
				print("Reading module...", end='.')
				self.litModule()
			# if empty line
			elif ligne[0] == " ":
				pass

		self.fichier.close()
		print("Close conf file")
		# returns int
		return 1



#---------------------------------------------------------------------
# fonction integree a get()

	def litModule (self) :  #   aaaaaaaaaaaaaaaaa
		""" read def module and add to listeModule """
		tmpliste = []
		ligne = " "

		while ligne == "" or ligne[0] != ']':
			ligne = self.fichier.readline()
			tmp = ligne[0:4]
			if tmp == "NAME":
				index = ligne.index('=')
				tmp = ligne[index + 1:-1]
				tmp = tmp.strip()
				print(tmp)
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
		""" return module list of list with name,port vars """
		# returns list
		return self.listeModule

#------------Retourne les modules connectes
	def getConModule(self) :
		""" return module list actually connected"""
		# vars
		serie = 0	# descripteur connexion serie
		recv = 0	# var reception du nom
		listeMod = list()	# liste des module ok
		# liste les port usb connectes
		listeTty = glob("/dev/ttyUSB*")
		if len(listeTty) == 0:
			print('No arduino module connected')
			return None
		# Connexion de chaque port serie trouve, double connexion serie du au reset de l arduino
		for port in listeTty:
			try:
				serie = serial.Serial(port)
			except:
				print("Error on %s" , port)
				break

			serie.setDTR(False)
			time.sleep(3)
			serie.flushInput()
			serie.setDTR(True)

			try:
				serie = serial.Serial(port,baudrate=57600, timeout=0)
				print("connexion on " , port)
			except:

				print("Error on %s" , port)
				break
		# Ligne de demande du nom du module
			var = "xx:name=?:\r"
			var = var.encode("ASCII")

			time.sleep(2)
		# Envoie de la ligne au module
			try:
				serie.write(var)				
			except:
				print("Unable to send datas to " , port)
				serie.close()
				break			
		# Lecture du nom renvoye
			time.sleep(1)
			try:
				recv = serie.readline()
			except:
				print("Reading error on " , port)
				serie.close()
				break

		# test du nom et effacement de \r\n
			recv = recv.decode()
			if recv != " ":
				recv = recv[:-2]
			print("Detection of ", recv)
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










