
//#include <array>
#include "funcs.h"
#define Pi 3.1415926

//#include "heder.h"
// Create the motor shield object with the default I2C address
// Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// int spr=200;

// Adafruit_StepperMotor *myMotor = AFMS.getStepper(spr, 1);
float switchsm=600;
float switchprev;
float sw;
//platformio device monitor --echo --eol CRLF --filter send_on_enter
int z2=START2;
char buffers[4][6];
int z1=START1;
int z3=START3;
int z1temp=START1;
int z2temp=START2;
int z3temp=START3;
int schritte;
int speedd=20;
long stepkram=0;
long t1;
long t2=0;
long t3=0;
long t_akt=0;
long safetime=0;
long serles=0;
int spr=200;
long usecs=60000000/(spr*speedd);
long *tims[6]={&t1,&t2,&t3,&t_akt,&serles,&stepkram};
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *myMotor = AFMS.getStepper(spr, 1);
bool serbool;
//int speedd=20;
// int schritte;
bool availprev=false;
char inp[5];
int ind=0;

int del1;
int del2;
int del3;
char akt;
int j=0;
int k=0;
bool aktiv1;
bool aktiv2;
bool aktiv3;
// long *tims[6]={&t1,&t2,&t3,&t_akt,&serles,&stepkram};
int *steller[4]={&schritte,&z1,&z2,&z3};
#define Pi 3.1415926
//#include <Adafruit_MotorShield.h>
//Adafruit_MotorShield AFMS = Adafruit_MotorShield();
//Adafruit_DCMotor *myMotor = AFMS.getMotor(3);
void setup() {
    //myMotor->setSpeed(255);
  //myMotor->run(FORWARD);
  // put your setup code here, to run once:
  //towas();
  pinMode(LEVEL,INPUT);
  pinMode(PIN1,OUTPUT);
  pinMode(PIN2,OUTPUT);
  pinMode(PIN3,OUTPUT);
  pinMode(8,OUTPUT);
  // Optimal 0,1600,1300,1500
  //servo auf 1430 runter für magnet
  digitalWrite(8,HIGH);
Serial.begin(9600);
AFMS.begin();
  Serial.println("Motor Shield found.");

  myMotor->setSpeed(speedd); 
  leveln();
  attachInterrupt(digitalPinToInterrupt(LEVEL),abr,CHANGE);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() && micros()-serles>4000){//Serial-buffer braucht 3 ms, um sich zu füllen, hab ich gehört
  availprev=true;
  
  serles=micros();
    akt=Serial.read();
            if(akt==','){
            j++;
            k=0;
        }
        else{
          buffers[j][k]=akt;
          k++;
        }
  }
      else if(Serial.available()==0 && availprev && micros()-serles>4000){
      serbool=false;
      k=0;
      j=0;
      serles=micros();
  availprev=false;
  for(int i=0;i<4;i++){
    if(buffers[i][0]!=0){
      *steller[i]=atof(buffers[i]);
    }
  }
  
  del1=0;
  del2=0;
  del3=0;
  for(int i=0;i<4;i++){
  memset(buffers[i],0,6);
  }
  //Serial.print(z1);Serial.print("\t");Serial.print(z2);Serial.print("\t");Serial.println(schritte);
  ind=0;
  }

  
turner(z1temp,PIN1,t1,aktiv1);
turner(z2temp,PIN2,t2,aktiv2);
turner(z3temp,PIN3,t3,aktiv3);
 if(!schritter()){
  //Serial.print(schritte);Serial.print(":\t");Serial.print(z1temp);Serial.print("\t");Serial.println(z2temp);
  if (micros()-t_akt>20000){
    t_akt=micros();
  if(!servo_akt(z1,z1temp,del1)){
    if(!servo_akt(z2,z2temp,del2)){
      if(!servo_akt(z3,z3temp,del3) && !serbool){
        serbool=true;
        Serial.println(1);
      }
    }

  }
 }
 }
}

