#ifndef FUNCS
#define FUNCS
#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_MotorShield.h>
#define START1 1900
#define START2 1600
#define START3 1500
#define PIN1 6
#define PIN2 7
#define PIN3 5
#define LEVEL 2
#define Pi 3.1415926



extern int z2;
extern char buffers[4][6];
extern int z1;
extern int z3;
extern int z1temp;
extern int z2temp;
extern int z3temp;
extern int schritte;
extern int speedd;
extern long stepkram;
extern long t1;
extern long t2;
extern long t3;
extern long t_akt;
extern long safetime;
extern long serles;
extern int spr;
extern long usecs;
extern long *tims[6];
extern Adafruit_MotorShield AFMS;
extern Adafruit_StepperMotor *myMotor;
void turner(int z,int pin,long& t,bool& aktiv);
bool servo_akt(int z,int& ztemp,int& del);
bool schritter();
void leveln();
bool fertig();
void abr();
#endif