#include <PubSubClient.h>
#include <SPI.h>
#include <Wire.h>
#include <ESP8266WiFi.h>

// Connect to the WiFi
const char* ssid = "NETGEAR68";
const char* password = "vU7$N5i0v%";
const char* mqtt_server = "192.168.1.41";

WiFiClient espClient;
PubSubClient client(espClient);

//ports for relays to power solenoid locks
int Relay = 5;
int Relay2 = 16;

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for(int i=0; i<length; i++) {
    char receivedChar = (char)payload[i];
    Serial.print(receivedChar);
    if(receivedChar == '1'){
      digitalWrite(Relay, LOW);
      delay(2000);
      digitalWrite(Relay, HIGH);
    }
    if(receivedChar == '2'){
      digitalWrite(Relay2, LOW);
      delay(2000);
      digitalWrite(Relay2, HIGH);
    }    
  }
  Serial.println();
}

void reconnect() {
  while(!client.connected()) {
    Serial.print("Attempting MQTT connection...");

    if(client.connect("ESP8266 Client")) {
      Serial.println("connected");
      client.subscribe("unlockNUM");
    }
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");

      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  //pin initializations
  pinMode(Relay, OUTPUT);
  pinMode(Relay2, OUTPUT);
  digitalWrite(Relay2, HIGH);
  digitalWrite(Relay, HIGH);
  

}

void loop() {
  if(!client.connected()) {
    reconnect();
  }
  client.loop();
}
