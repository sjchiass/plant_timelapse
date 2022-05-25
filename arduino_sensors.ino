#include "DHT.h"
#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22

#define Probes A0 

DHT dht(DHTPIN, DHTTYPE);

float s = 0;
 
void setup() { 
 Serial.begin(9600); 
 dht.begin();
 pinMode(5, OUTPUT);
} 
void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    // Let it rest
    delay(1000);
    return;
  }

  // Only power sensor when necessary
  digitalWrite(5, HIGH);
  // Let it rest
  delay(10);
  // Divide by 1024 to normalize reading between 0 and 1
  // Then subtract it from one so that 1 becomes moist
  // Multiply by 100 to get a %
  s = 100.0*(1-(analogRead(Probes)/1024.0));
  digitalWrite(5, LOW);

  // Print the data through serial
  Serial.print(s);
  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.println(t);

  // Wait 5 minutes
  delay(300000); 
} 
