Seulement pour Linux mais bientot sur windows
Only for Linux but soon with windows




SimX permet d'interfacer X-plane et des modules Arduino
Il s'utilise avec le plugin uipcx coté simulateur
Por cela, il faut renseigner le fichier "Simx.conf" avec l'IP et le PORT du serveur ainsi que les variables du fichier uipcxdatos du repertoire plugin de X-plane
ajouter les modules arduino dans le fichier arduino.conf -> NAME et VAR
Lancer SimX_v01.py, une fois connecté, les variables seront envoyés directement au module concerné

Pour utiliser SimX, il faut:
Installer python3
Installer python3-serial


Simx is a script that connect Arduino modules to X-plane
It uses uipcx plugin on simulator side
You have to add IP an PORT of server in "Sinx.conf" file and var from uipcxdatos file in X-plane plugin directory
Add arduino modules in arduino.conf file -> NAME and VAR
Launch SimX_v01.py, once connected, vars will be automaticly updated on the right module

To use SimX, you need:
install python3
install python3-serial

