
#include <SoftwareSerial.h> 

#include <SPI.h>
#include <Wire.h>



SoftwareSerial MyBlue(0, 1);

int Relay = 8;
int Relay2 = 7;
 
void setup() {
 
// Locker initialization
pinMode(Relay, OUTPUT);
pinMode(Relay2, OUTPUT);
digitalWrite(Relay, HIGH);
digitalWrite(Relay2, HIGH);
Serial.begin(9600);
MyBlue.begin(38400);  //Baud Rate for AT-command Mode.  
Serial.println("***AT commands mode***"); 
 
 
}

 void loop() 
{ 
 //from bluetooth to Terminal. 
 if (MyBlue.available()) 
   Serial.write(MyBlue.read()); 
 //from termial to bluetooth 
 if (Serial.available()) 
   MyBlue.write(Serial.read());

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if(data == "1")
    {
      digitalWrite(Relay, LOW);
      delay(2000);
      digitalWrite(Relay, HIGH);
    }
    else if(data == "2")
    {
      digitalWrite(Relay2, LOW);
      delay(2000);
      digitalWrite(Relay2, HIGH);
    }
    else 
    {
      digitalWrite(Relay, HIGH);
      digitalWrite(Relay2, HIGH);
    }
  }
}
 
 
 
