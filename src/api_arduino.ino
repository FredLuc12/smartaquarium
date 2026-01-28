#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <RTClib.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

const String API_URL_MESURE      = "http://host.wokwi.internal:8000/api/mesures/";
const String API_URL_COMMAND     = "http://host.wokwi.internal:8000/api/commandes/";
const String API_URL_ACTIONNEURS = "http://host.wokwi.internal:8000/api/actionneurs/";
const String API_URL_CAPTEURS    = "http://host.wokwi.internal:8000/api/capteurs/";

bool LUM_ACTIVATE = false;

int last_temp = LOW;     
int last_distance = LOW;
int last_pH = LOW;
int last_light = LOW;

const float GAMMA = 0.7;
const float RL10 = 50;

// Pins ESP8266 compatibles
const int RELAY_HEAT = 5;   // D1
const int RELAY_PUMP = 4;   // D2
const int RELAY_LUM = 0;    // D3

// Seuils 
float TEMP_THRESHOLD = 25.0;
float WATER_THRESHOLD = 200;
float LUM_THRESHOLD = 1000;

// DS18B20
#define ONE_WIRE_BUS 13  // D7
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// RTC
#define SDA_PIN 4   // D2
#define SCL_PIN 5   // D1
RTC_DS1307 rtc;

// HC-SR04
#define TRIG_PIN 14  // D5
#define ECHO_PIN 12  // D6

// Potentiometer (ESP8266 n'a qu'un seul ADC)
#define POTENTIOMETER_PIN A0

// PHOTO-RESISTOR - Commenté car même pin que potentiomètre
// #define LDR_PIN A0

struct Capteur {
  int id;
  const char* nom;
  const char* type;
  const char* unite;
  const char* localisation;
  float seuil_min;
  float seuil_max;
  bool actif;
};

struct Actionneur {
  int id;
  const char* nom;
  const char* type;
  bool etat;
};

Capteur capteurs[] = {
  {1,"TempEau", "DS18B20", "°C", "Bassin", 0, 35, true},
  {2,"NiveauEau", "HC-SR04", "cm", "Cuve", 0, 300, true},
  {3,"Luminosite", "LDR", "lux", "Serre", 200, 2000, true},
  {4,"pH", "Potentiometre", "", "Bassin", 0, 14, true}
};

Actionneur actionneurs[] = {
  {10,"Chauffage", "relay_motor", false},
  {11,"Pompe", "relay_motor", false},
  {12,"Eclairage", "relay_motor", false}
};

void Register_Capteurs() {
  for (auto &c : capteurs) {
    String json =
      "{"
      "\"id\":" + String(c.id) + ","
      "\"nom\":\"" + String(c.nom) + "\","
      "\"type\":\"" + String(c.type) + "\","
      "\"unite\":\"" + String(c.unite) + "\","
      "\"localisation\":\"" + String(c.localisation) + "\","
      "\"seuil_min\":" + String(c.seuil_min) + ","
      "\"seuil_max\":" + String(c.seuil_max) + ","
      "\"actif\":" + String(c.actif ? "true" : "false") +
      "}";

    Send_JSON(json,API_URL_CAPTEURS);
  }
}

void Register_Actionneurs() {
  for (auto &a : actionneurs) {
    String json =
      "{"
      "\"id\":" + String(a.id) + ","
      "\"nom\":\"" + String(a.nom) + "\","
      "\"type\":\"" + String(a.type) + "\","
      "\"etat\":" + String(a.etat ? "true" : "false") +
      "}";

    Send_JSON(json,API_URL_ACTIONNEURS);
  }
}

void Setup_Hour(){

  Wire.begin(SDA_PIN, SCL_PIN);

  if (!rtc.begin()) {
    Serial.println("RTC DS1307 non detecte !");
    while (1);
  }

  if (!rtc.isrunning()) {
    Serial.println("RTC arrete, mise a l'heure...");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

}

void Setup_Wifi() {

  Serial.begin(115200);
  Serial.println("Hello, ESP8266!");

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
}

void setup() {
  
  Setup_Wifi();
  // Setup_Hour();

  sensors.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(POTENTIOMETER_PIN, INPUT);

  pinMode(RELAY_HEAT, OUTPUT);
  pinMode(RELAY_PUMP, OUTPUT);
  pinMode(RELAY_LUM, OUTPUT);

  Register_Capteurs();
  Register_Actionneurs();

}

float HC_SR04() {

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;

  return distance;
}

// Photoresistor commenté - même pin que potentiomètre sur ESP8266
// int Photoresistor(){
//   int lux = analogRead(A0);
//   return lux;
// }

float DS18B20() {

  sensors.requestTemperatures(); 
  float temps = sensors.getTempCByIndex(0);

  return temps;
}

float Potentiometer() {

  float phRaw = analogRead(POTENTIOMETER_PIN);
  float phValue = map(phRaw, 0, 1023, 0, 14);  // ESP8266 ADC = 0-1023

  return phValue;
}

void Relay_Lum(float light){

  DateTime now = rtc.now();
  if (light < LUM_THRESHOLD){

      Serial.println("not enought luminosity");

    if (now.hour() < 22 && now.hour() > 17){
      Serial.println("Light ON");
      digitalWrite(RELAY_LUM, HIGH);
    }
    else{
      Serial.println("Light in ECO MODE");
    }
  }

  Trigger_Call_API(RELAY_LUM, last_light,12,3,light);

}

void Trigger_Call_API(int RELAY, int &last_value, int actionneur_id, int capteur_id, float mesure){

  int current_state = digitalRead(RELAY);
  if (current_state != last_value){
    Serial.println("send data to bdd");
    last_value = current_state;
    String payload_mesure = "{"
      "\"capteur_id\":" + String(capteur_id) + ","
      "\"mesure\":" + String(mesure) +
      "}";
    Send_JSON(payload_mesure, API_URL_MESURE);

    String payload_commande = "{"
      "\"actionneur_id\":" + String(actionneur_id) + ","
      "\"commande\":\"" + String(current_state) + "\","
      "\"source\":" + " automatique" +
      "}";

    Send_JSON(payload_commande, API_URL_COMMAND);
  }
  else{
   Serial.println("value unsend no changes"); 
  }
}

void Display_Hour(){
  
  DateTime now = rtc.now();
  Serial.print(now.hour());
  Serial.print(":");
  Serial.print(now.minute());
  Serial.print(":");
  Serial.println(now.second());
}

void Relay_Heat(float temperature) {
  digitalWrite(RELAY_HEAT, temperature < TEMP_THRESHOLD ? HIGH : LOW);
  Trigger_Call_API(RELAY_HEAT, last_temp,10,1,temperature);

}

void Relay_Pump(float distance) {
  digitalWrite(RELAY_PUMP, distance > WATER_THRESHOLD ? HIGH : LOW);
  Trigger_Call_API(RELAY_PUMP, last_light,11,2, distance);
}

void Display(String component, String label, float value, String unity) {

  Serial.print(component);
  Serial.print(" / ");
  Serial.print(label);
  Serial.print(" = ");
  Serial.print(value);
  Serial.println(unity);
}

String Build_JSON(String key, float value) {
  String json = "{";
  json += "\"" + key + "\":" + String(value);
  json += "}";
  return json;
}

void Send_JSON(String payload, String endpoint){

  if(WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    http.begin(client, endpoint);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload);

    if(httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Erreur HTTP: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi déconnecté !");
  }

}

void loop() {

  Display_Hour();

  float distance_result = HC_SR04();
  float temperature_result = DS18B20();
  float pH_result = Potentiometer();
  float light_result = 500;  // Valeur fixe temporaire (LDR commenté)

  Display("DS18B20", "Temperature eau", temperature_result, " °C");
  Display("HC-SR04", "Distance", distance_result, " cm");
  Display("Potentiometer", "pH", pH_result, "");
  Display("Photosensor", "Luminosité", light_result, "");

  Relay_Pump(distance_result);
  Relay_Heat(temperature_result);
  Relay_Lum(light_result);

  delay(2000); 
}
