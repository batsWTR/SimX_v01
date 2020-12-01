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
listeVarRegister = [] # liste des variables à enregistrer sur le serveur IOCP

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


#  on fait la liste complete des variables à enregistrer, on affiche

print("**** Fichier de conf ****")
for j,k in simxConf.getVar().items():
		print(j,k)
		listeVarRegister.append(j)


print("**** Fichier Arduino ++++")
for i in  arduinoConf.getModule():
		find = 0
		print(i)
		for j in i[2]:
			j = int(j)
			for l in listeVarRegister:
				if j == l:
					find = 1
			if find == 0:
				listeVarRegister.append(j)

print("liste var")
print(listeVarRegister)




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
nb_module = len(liste)

if len(liste) > 0:
	for mod in liste:
		moduleArduino.append(Arduino(mod))
	for i in range(len(moduleArduino)):
		moduleArduino[i].connection()
else:
	print("Aucun module Arduino connectes")


# Connexion au serveur IOCP et enregistrement

iocp = Iocp2()
ip = simxConf.getIp()
port = simxConf.getPort()


# boucle principale du programme
while( True):
	#essai de connexion au serveur
	while iocp.connect(ip,port) == -1:
		time.sleep(2)


	#enregistrements sur le serveur
	dictVarArduino = iocp.register(listeVarRegister)
	print("REGISTERED: ",dictVarArduino)
	# test si iocp est toujours connecte
	while (iocp.isConnected):
		dictRecv = iocp.recvData()
		# test si des datas ont ete recues
		if(dictRecv != -1):
			for cle in dictRecv.keys():
				dictVarArduino[cle] = dictRecv[cle]
		if nb_module != 0:
			majModule()
	# coupure du serveur = mise a zero de toutes les vars
	for cle in dictVarArduino.keys():
		dictVarArduino[cle] = '0'
	if nb_module != 0:
		majModule()
	







# Fermeture des module Arduino
for i in range(len(moduleArduino)):
	moduleArduino[i].closeSerie()

#Fermeture serveur
iocp.close()



	

















