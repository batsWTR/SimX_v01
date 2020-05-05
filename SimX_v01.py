#  Programme permettant la recuperation de variables IOCP et de les transmattre a un
#  Arduino.
# 2 fichiers de configurations sont necessaires,
# simx.conf:
# 1 er ligne, PORT=xxxx , port IOCP
# 2 eme ligne IP=xx.xx, adresse ip du serveur
# lignes suivantes:
# variable a surveiller, venant du fichier uipcxdatos.txt
# 500	sim/cockpit2/gauges/indicators/airspeed_kts_pilot	float	n
#
# arduino.conf
# decrit les modules Arduino qui recevront les variables
# [
# NAME= nom_module  
# PORT = /dev/xx
# VAR= 500,332,55
# ]
# cree par B.Wentzler janvier 2015




from libs.SimxConf import *
from libs.ArduinoConf import *
from libs.Arduino import *
from libs.Iocp import *
import time
import os



dictVarArduino = {}  #contient toutes les cles st variables des modules arduino
moduleArduino = [] # Liste des modules Arduino

dirName = os.path.dirname(__file__)
fileSimxConf = os.path.join(dirName, "simx.conf")
fileArduinoConf = os.path.join(dirName,"arduino.conf")


simxConf = SimxConf(fileSimxConf)
arduinoConf = ArduinoConf(fileArduinoConf)

# Lecture des fichiers de configuration

if simxConf.get() == -1:
	print("Probleme avec le fichier",fileSimxConf)
	exit(-1)

if arduinoConf.get() == -1:
	print("Probleme avec le fichier",fileArduinoConf)
	exit(-1)

#------------------------------------------------


# Mise a jour de tous les modules
def majModule():
	for i in range(len(moduleArduino)):
		dictTemp = {}
		dictTemp2 ={}
		# dicttemp contiens les cles a mettre a jour
		dictTemp = moduleArduino[i].getToUpdate()
		print(moduleArduino[i].nom," MAJ: ",dictTemp)
		print("DICTARD: ", dictVarArduino)
		for cle in dictTemp.keys():
			if dictTemp[cle] != dictVarArduino[cle]:
				print("NO ERROR")
				dictTemp2[cle] = dictVarArduino[cle]
		moduleArduino[i].updateData(dictTemp2)






# Creation et init des classes pour chaque module Arduino

liste = arduinoConf.getConModule()
for mod in liste:
	moduleArduino.append(Arduino(mod))

if len(moduleArduino) == 0:
	print("Aucun module Arduino connectes")
	exit(-1)
	
#---------------------------------------

# Connexions de chaque module   ATTENTION si connection nok

for i in range(len(moduleArduino)):
	moduleArduino[i].connection()



#---------------------------------

# Recuperation des variable pour le serveur IOCP

for i in range(len(moduleArduino)):
	dico = moduleArduino[i].getToUpdate()
	for cle,val in dico.items():
		dictVarArduino[cle] = val

print(dictVarArduino)
#----------------------------------------------

# Connexion au serveur IOCP et enregistrement

iocp = Iocp2()
ip = simxConf.getIp()
port = simxConf.getPort()
listeVar = []

#prend ttes les variables des Arduinos et les mets dans la liste
for cle in dictVarArduino.keys():
	listeVar.append(cle)

# boucle principale du programme
while( True):
	#essai de connexion au serveur
	while iocp.connect(ip,port) == -1:
		time.sleep(2)


	#enregistrements sur le serveur
	dictVarArduino = iocp.register(listeVar)
	print("REGISTERED: ",dictVarArduino)
	# test si iocp est toujours connecte
	while (iocp.isConnected):
		dictRecv = iocp.recvData()
		# test si des datas ont ete recues
		if(dictRecv != -1):
			for cle in dictRecv.keys():
				dictVarArduino[cle] = dictRecv[cle]
			majModule()
	# coupure du serveur = mise a zero de toutes les vars
	for cle in dictVarArduino.keys():
		dictVarArduino[cle] = '0'
	majModule()
	







# Fermeture des module Arduino
for i in range(len(moduleArduino)):
	moduleArduino[i].closeSerie()

#Fermeture serveur
iocp.close()



	

















