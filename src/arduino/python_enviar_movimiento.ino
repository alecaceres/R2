#include <SPI.h>  
#include "RF24.h"
#include <Otto.h>
Otto Otto;
RF24 myRadio (9, 10);
byte addresses[][6] = {"0"};
#define LeftLeg 2 
#define RightLeg 3
#define LeftFoot 4 
#define RightFoot 5 
#define Buzzer  8 
#define Trigger 6 // ultrasonic sensor trigger pin
#define Echo 7 // ultrasonic sensor echo pin
int mov=0;
  String index;
struct package {
  int id = 1;
  char  text = '0';
};


typedef struct package Package;
Package dataRecieve;
Package dataTransmit;

void setup() {
     Otto.init(LeftLeg, RightLeg, LeftFoot, RightFoot, true, Buzzer); //Set the servo pins and Buzzer pin
  pinMode(Trigger, OUTPUT); 
  pinMode(Echo, INPUT); 
  Serial.begin(115200);
  delay(1000);
  
  myRadio.begin();  
  myRadio.setChannel(115); 
  myRadio.setPALevel(RF24_PA_MAX);
  myRadio.setDataRate( RF24_250KBPS );
  
  myRadio.openReadingPipe(1, addresses[0]);
  myRadio.startListening();
}

void loop() {
  if ( myRadio.available()) {
    while (myRadio.available()){
      myRadio.read( &dataRecieve, sizeof(dataRecieve) );
    }
    int mov = dataRecieve.text - '0';
   Serial.println(mov);
  }
  

 delay(200);
 myRadio.stopListening();
 
  dataTransmit.id = dataTransmit.id + 1;
 
  char flag=0;

  while (Serial.available() >= 1) {
index=Serial.readStringUntil('\n');}
dataTransmit.text=index[0];
  myRadio.openWritingPipe(addresses[0]);
  myRadio.write(&dataTransmit, sizeof(dataTransmit));
  myRadio.openReadingPipe(1, addresses[0]);
  myRadio.startListening();
}
