#include <SPI.h>  
#include "RF24.h"
#include <Otto.h>
Otto Otto;
RF24 myRadio (9, 10);
byte addresses[][6] = {"0"};
#define PIN_YL 2 // left leg, servo[0]
#define PIN_YR 3 // right leg, servo[1]
#define PIN_RL 4 // left foot, servo[2]
#define PIN_RR 5 // right foot, servo[3]
#define Trigger 7 // ultrasonic sensor trigger
#define Echo 6 // ultrasonic sensor echo
#define PIN_Buzzer 8 //buzzer

#define DIN_PIN A3
#define CS_PIN A2
#define CLK_PIN A1
#define LED_DIRECTION 1
int mov=0;
struct package {
  int id = 5; // id
  char  text = '1';
};


typedef struct package Package;
Package dataReceive;
Package dataTransmit;
long ultrasound() {
   long duration, distance;
   digitalWrite(Trigger,LOW);
   delayMicroseconds(2);
   digitalWrite(Trigger, HIGH);
   delayMicroseconds(10);
   digitalWrite(Trigger, LOW);
   duration = pulseIn(Echo, HIGH);
   distance = duration/58;
   return distance;
}

void setup() {
  Otto.init(PIN_YL, PIN_YR, PIN_RL, PIN_RR, true, PIN_Buzzer);
    pinMode(Trigger, OUTPUT); 
  pinMode(Echo, INPUT); 

  Otto.initMATRIX( DIN_PIN, CS_PIN, CLK_PIN, LED_DIRECTION); 
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
      myRadio.read( &dataReceive, sizeof(dataReceive) );
    }
    Serial.println("Recieve: ");
    Serial.println(dataReceive.text);
    int mov = dataReceive.text - '0';
    if ( dataReceive.id == 5 ) {
      if(mov== 1){Otto.walk(1,1500,1);}
      if(mov== 2){Otto.walk(1,1500,-1);}
    }
  }
 delay(100);
 myRadio.stopListening();
 
  dataTransmit.id = dataTransmit.id + 1;
  Serial.println("Transmit: ");
  Serial.println(dataTransmit.text);
  char inData[300];
  int index = 0;
      if (ultrasound() <= 15) {
      dataTransmit.text = '1';

    }else{
 
      dataTransmit.text = '0';}


  myRadio.openWritingPipe(addresses[0]);
  myRadio.write(&dataTransmit, sizeof(dataTransmit));
  myRadio.openReadingPipe(1, addresses[0]);
  myRadio.startListening();
}
