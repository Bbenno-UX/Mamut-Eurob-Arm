#include "funcs.h"
bool fertig(){
  return (z1==z1temp && z2==z2temp && z3==z3temp && schritte==0);
    
  
}

void leveln(){
  while(digitalRead(LEVEL)){
        myMotor->onestep(FORWARD,SINGLE);
        delayMicroseconds(usecs);
  }
  for(int i=0;i<100;i++){
    myMotor->onestep(BACKWARD,SINGLE);
  }
}
void turner(int z,int pin,long& t,bool& aktiv){
if(aktiv && micros()-t>20000-z){
  digitalWrite(pin,HIGH);
  aktiv=false;
  t=micros();
}
else if (!aktiv && micros()-t>z){
  t=micros();
  digitalWrite(pin,LOW);
  aktiv=true;
}
}
bool schritter(){//funktion für schrittmotoren adafruit benutzt dummerweise "delay" bei der step funktion, darum nur 1 schritt auf einmal
  if(abs(schritte)>0){
  if(micros()-stepkram>usecs){
    stepkram=micros();
    if(schritte>0){
    schritte--;
    myMotor->onestep(BACKWARD,SINGLE);
    }
       if(schritte<0){
    schritte++;
    myMotor->onestep(FORWARD,SINGLE);
    }
  }
  return true; 
  }
  return false;
}
bool servo_akt(int z,int& ztemp,int& del){
  if(abs(ztemp-z)>2){
    //Serial.println("was");
  ztemp=ztemp+(z-ztemp)*pow(sin(del*2*Pi/150),2);
  del++;
  //Serial.print(pin);Serial.print(":\t");Serial.print(ztemp);Serial.print("\t");Serial.println(z);
  return true;
}
del=0;
return false;
}
void abr(){
  schritte=50;
}
void ovf_kontrolle(){
  if(micros()<t1){
    for(int i=0;i<sizeof(tims)/sizeof(tims[0]);i++){
      *tims[i]=0;
    }
  }
}