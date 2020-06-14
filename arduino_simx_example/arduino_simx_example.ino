// module Instru_servo


// Sketch template pour les instruments a base d'un moteur pas a pas.
// Pour la configuration, reiseigner la variable nomModule et numIOCP suivant l instrument.
// Activez ou desactivez la fonction testEncofeur si l instru dispose d un encodeur rotarif
// Modifiez la fonction calculDeplacement suivant l instrument

// Les trames de receptions reconnues par le module sont:

// servo1:cal=val:\r    -> trame de calibration val = valeur + / -, nomModule est facultatif
// servo1:numIOCP=val:\r  -> valeur de la variable IOCP, nomModule est facultatif
// nomHasard:name=?:\r  -> demande le nom du module, renvoie nomModule, nomHazard = on ne connait pas le nom du module
// servo1:504=10500:505=905:506=905:507=25:508=25:
// servo1 fuel:EGT g:EGT d:N1 g:N1 d:

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVOMIN  60 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  440 // This is the 'maximum' pulse length count (out of 4096)

#define SERVO_FREQ 52 // Analog servos run at ~60 Hz updates

// NOM du module

String nomModule = "servo1";    // Nom du module
int lastFuel = 0;
int lastN1 = 0;
int lastEgt = 0;



void setup()
{
  
  // Lancement de la connexion serie
  Serial.begin(57600);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);  // The int.osc. is closer to 27MHz  
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~60 Hz updates
  delay(10);
  
  fuel("0");
  egtd("0");
  n1d("0");
}

void loop()
{

  String ligne = "";
  
  // Fonction de recuperation de la variable envoyee sur le port serie, met a jour la var varIOCP
  ligne = receptionData();
  
  // si une ligne est recu
  if (ligne != 0){
    //Serial.println("[DEBUG] ligne reception: " + ligne);
    decoupeLigne(ligne);
  }
  


    
}


//---------------------------------------------------------------------------------------






//--------------------------------------------------------------------------------------




  // Fonction de recuperation de la variable envoyee sur le port serie, met a jour la var varIOCP
String receptionData()
{
  char inByte = 0;
  String ligneRecep = "";
  
  
  // En attente de qqch a recevoir
  while (Serial.available() > 0) {
    //Serial.println("DEBUG: arrivee port serie");
 // Lit sur le port serie jusqu a '\r'et met la ligne lue dans ligneRecep sans le '\r'
  while (inByte != '\r') {
    if (Serial.available() > 0) {
      inByte = Serial.read();
      if (inByte != '\r') {
         ligneRecep += inByte;
      }
      
    }
  }
 
 // Fonction de decoupe de la ligne recu 
 return (ligneRecep);
  
  
  }

}

//******************************************************
// recoit une ligne et la decoupe selon le separateur ':'puis appelle decoupemot(mot) sinon se tremine
void decoupeLigne(String ligne)
{
  int next = 0;
  int sep = 0;
  String mot = "";
  
  while (next < ligne.length()) {
    sep = ligne.indexOf(':', next);
    if (sep != -1) {
      mot = ligne.substring(next, sep);
      next = sep + 1;
      // decoupeMot
      //Serial.println("DEBUG separation: " + mot);
      decoupeMot(mot);
    }
    else {
      next = ligne.length();
    }
  }
      
  
}
//***********************************************************************


// Recois les donneees decoupees par ':' -> Nom  var=val 
            // commandes possibles:
            // name:?     -> renvoie de nomModule sur le port serie
            // numIOCP:val   -> val est convertie en int puis divise par 10 000 et rangee dans varIOCP
            // cal:val        -> calibration du moteur, avance ou recule de val
            
void decoupeMot(String mot) {
  
  int sep = 0;
  int intVal = 0;
  String var = "";
  String val = "";
  String name = "name";
  String cal = "cal";
  float temp = 0;
  

  
  
  // Index du separateur ==
  sep = mot.indexOf('=');
  
  // Si pas de '=', alors abandons du mot, en general, nomModule
  if (sep == -1) {
    return;
  }
  
  // cote gauche du mot, soit nomModule,numIOCP ou 0
  var = mot.substring(0, sep);
  //Serial.println("[DEBUG] var: " + var);

  // cote droit du mot, converie en int
  val = mot.substring(sep + 1);

  // parfois, val est vide !
  if (val == "")
  {
    return;
  }
  //Serial.println("[DEBUG] val: " + val);
  

  // Test si var = name, si oui, renvoi le nom du module
 if (var == name)
 {
   Serial.println(nomModule);
   return;
 }

 
 
 // Test si var = numIOCP, si oui, / par 100 et met a jour varIOCP
 // fuel
 if ( var == "504")
 {
  //Serial.println("DEBUG: envoi a servo 0");
  fuel(val);
   return;
 }
 else if (var == "505")
 {
  egtg(val);
  return;  
 }
 else if (var == "506")
 {
  egtd(val);
  return;
 }
 else if (var == "507")
 {
  n1g(val);
  return;
 }
 else if (var =="508")
 {
  n1d(val);
  return;
 }
 else
 {
  return;
 }
}


//-----------------------------------------------------------------------------------------
// met à jour le servo n°0
void fuel(String val)
{
   long  intVal = 0;
   String str;
   
   intVal = val.toInt();
   intVal = intVal / 10000;
   //Serial.println("DEBUG: intVal: " + intVal);
   

   // map la valeur : 0 -> 70 et 1000 -> 275
   intVal = map(intVal,0,1000,70,275);
   if (intVal > SERVOMAX)
   {
    intVal = SERVOMAX;
   }
   // envoi la valeur au servo 0
   pwm.setPWM(0,0,intVal);
   
  // str = "[DEBUG] var IOCP: " ;
   //str += intVal;
   //Serial.println(str);
  
}
void egtg(String val)
{
  long  intVal = 0;
  intVal = val.toInt();
  intVal = intVal / 10000;
   //Serial.println("DEBUG: intVal: " + intVal); 

   // map la valeur : 0 -> 70 et 1000 -> 275
   intVal = map(intVal,0,1000,70,275);
   if (intVal > SERVOMAX)
   {
    intVal = SERVOMAX;
   }
  
  pwm.setPWM(1,0,70);
  delay(5);
}
void egtd(String val)
{
  long  intVal = 0;
  intVal = val.toInt();
  intVal = intVal / 10000;
  // Serial.println("DEBUG egtd: intVal: " + String(intVal));

   // map la valeur : 0 -> 70 et 1000 -> 275
   intVal = map(intVal,0,1000,84,380);
   if (intVal > SERVOMAX)
   {
    intVal = SERVOMAX;
   }
  
  pwm.setPWM(2,0,intVal);

  
}
void n1g(String val)
{
  long  intVal = 0;
  intVal = val.toInt();
  intVal = intVal / 10000;
   //Serial.println("DEBUG n1g: intVal: " + intVal);

   // map la valeur : 0 -> 70 et 1000 -> 275
   intVal = map(intVal,0,1000,70,275);
   if (intVal > SERVOMAX)
   {
    intVal = SERVOMAX;
   }
  
  pwm.setPWM(3,0,70);

}
void n1d(String val)
{
  long  intVal = 0;
  long secval = 0;
  intVal = val.toInt();
  intVal = intVal / 1000;
  



if (lastN1 < intVal)
{
  for(lastN1;lastN1 <= intVal; lastN1 ++)
  {
    secval = map(lastN1,0,1000,440,1920);
    pwm.writeMicroseconds(4,secval);
    //delay(2);
  }
  lastN1 = intVal;
  return;
}
else if (lastN1 > intVal)
{
  for(lastN1;lastN1 >= intVal; lastN1 --)
  {
    secval = map(lastN1,0,1000,440,1920);
    pwm.writeMicroseconds(4,secval);
    //delay(2);
  }  
  lastN1 = intVal;
  return;
}
else if (intVal == 0)
{
  pwm.writeMicroseconds(4,450);
  lastN1 = 0;
  return;
}

  
       // map la valeur : 0 -> 70 et 1000 -> 275
     
     //Serial.println("DEBUG n1d: intVal: " + String(intVal));
     //lastN1 = intVal;


}
