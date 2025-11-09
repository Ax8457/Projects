/*
    IOT Application
    Personal Project 

*/

/*
  LIBRARIES AND VARS; STRUCT ....
*/
//include
#include "DHT.h"
#include <ArduinoJson.h>
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WebServer.h>
#include <LittleFS.h>
#include <FFat.h>
#include "esp_system.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
//LED
#define LED_GREEN 18
#define LED_RED 19
#define LED_YELLOW 33
//NeoPixel
#define LED_PIN 26
#define LED_COUNT 1
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_RGBW + NEO_KHZ800); // 1 LED on pin 2
//DHT 
#define DHTPIN 17 
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE); 
// MQTT connection details
#define MQTT_HOST "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_DEVICEID "id"
#define MQTT_USER "" // no need for authentication, for now
#define MQTT_TOKEN "" // no need for authentication, for now
#define MQTT_TOPIC "id/evt/status/fmt/json"
#define MQTT_TOPIC_DISPLAY "id/cmd/display/fmt/json" 
//https://www.hivemq.com/demos/websocket-client/
//user: redacted , password:redacted
//clientID clientId-v3g7u5bJoK
//MQTT object
void callback(char* topic, byte* payload, unsigned int length);
WiFiClient wifiClient;
PubSubClient mqtt(MQTT_HOST, MQTT_PORT, callback, wifiClient);
//Time
const char* ntpServer = "pool.ntp.org"; //ntp server
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 3600;
//struct for DHT metrics
  //create struct
struct DHTMetrics {
  float h;
  float t;
  float f;
};
//json objects
StaticJsonDocument<512> jsonDoc;//allocate memory
StaticJsonDocument<256> jsonDoc2;
//overall system status
int isOk = 0;
bool jsonExport = true;
int delay_time = 1000;
//Commands
enum CommandType {
  SUSPEND_JSON_EXPORT,
  CHANGE_POLLING_INTERVAL,
  CHANGE_NEOPIXEL_COLOR,
  UNKNOWN_COMMAND
};
//color for neopixel control
enum Color{
  BLUE,
  RED,
  GREEN,
  YELLOW,
  ORANGE,
  PURPLE,
  WHITE,
  PINK,
  UNKNOWN_COLOR
};
//API server
WebServer server(80);
fs::FS* fsys = nullptr;// file system no intialized yet => null ptr


/*
    FUNCTIONS
*/
//color
Color getColor(JsonObject o) {
  for (JsonPair key_value : o) {
    const char* key = key_value.key().c_str();
    bool val = key_value.value().as<bool>();
    if (val) {
      if (strcmp(key, "red") == 0) return RED;
      if (strcmp(key, "blue") == 0) return BLUE;
      if (strcmp(key, "green") == 0) return GREEN;
      if (strcmp(key, "yellow") == 0) return YELLOW;
      if (strcmp(key, "orange") == 0) return ORANGE;
      if (strcmp(key, "purple") == 0) return PURPLE;
      if (strcmp(key, "white") == 0) return WHITE;
      if (strcmp(key, "pink") == 0) return PINK;
    }
  }
  return UNKNOWN_COLOR;
}

//update color 
void NeoPixel_setColor(Color c) {
  switch(c){
    case BLUE:
      strip.setPixelColor(0, strip.Color(0, 0, 50));
      strip.show();
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    case RED:
      strip.setPixelColor(0, strip.Color(0, 50, 0));
      strip.show(); 
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    case GREEN:
      strip.setPixelColor(0, strip.Color(50, 0, 0));
      strip.show();
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    case YELLOW:
      strip.setPixelColor(0, strip.Color(50, 50, 0));
      strip.show();
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    case ORANGE:
      strip.setPixelColor(0, strip.Color(25, 50, 0));
      strip.show();
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    case PURPLE:
      strip.setPixelColor(0, strip.Color(50, 0, 50));
      strip.show();
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    case WHITE:
      strip.setPixelColor(0, strip.Color(50, 50, 50));
      strip.show();
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    case PINK:
      strip.setPixelColor(0, strip.Color(25, 50, 25));
      strip.show();
      Serial.println("[<=] NeoPixel Color changed.");
      break;
    default:
      strip.setPixelColor(0, strip.Color(255, 255, 255));
      strip.show(); 
      Serial.println("[<=] NeoPixel Color Unknown.");
      break;
  }
}




//Wifi setup
void setup_wifi(){
  WiFi.mode(WIFI_STA); //Set the ESP to station mode (client)
  char* ssid = "redacted";
  char* password = "redacted";
  WiFi.begin(ssid, password);
  delay(3000);
  if (WiFi.status() == WL_CONNECTED){
    Serial.println("[+] Connected to Wifi,Ip :");
    Serial.println(WiFi.localIP());
    flash_LED(LED_YELLOW,1);
    //NeoPixel_setColor(0);
  }
}

/*
DEBUG
//print local time
void printLocalTime(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
}
*/

//update neopixel led if connection 
void check_wifi_state(){
    while(WiFi.status() != WL_CONNECTED){
      flash_LED(LED_YELLOW,0);
      delay(1000);
      Serial.println("=> Reconnecting to Wifi ...");
    } 
    flash_LED(LED_YELLOW,1);
}

//read DHT metrics
DHTMetrics get_DHT_metrics()
{
  //float metrics 
  DHTMetrics m; //dedicated struct created
  m.h = dht.readHumidity();
  m.t = dht.readTemperature();
  m.f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(m.h) || isnan(m.t) || isnan(m.f)) {
    Serial.println(F("[x] Failed to read from DHT sensor!"));
    isOk = +1;
    m.t = 0;
    m.h = 0;
    m.f = 0;
    return m;
  }
  //return metrics
  return m;
}

//create metrics in JSON format
JsonObject craft_metrics_json(DHTMetrics m){
  //get time
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("[x] Failed to obtain time");
    isOk += 1;
    JsonObject err = jsonDoc.to<JsonObject>();
    err["error"] = "<[x] Failed to obtain time";
    return err;
  }
  char timeStr[50];  
  strftime(timeStr, sizeof(timeStr), "%A, %B %d %Y %H:%M:%S", &timeinfo);
  //create payload
  JsonObject payload = jsonDoc.to<JsonObject>();
  JsonObject metrics = payload.createNestedObject("Metrics");
  //metrics
  metrics["Temperature_C"] = m.t;
  metrics["Temperature_F"] = m.f;
  metrics["Humidity"] = m.h;
  JsonObject time = payload.createNestedObject("Time");
  time["Time"] = timeStr;

  //return payload
  return payload;
}

//connect MQTT broker
void connect_MQTT_broker(){
  if (mqtt.connect(MQTT_DEVICEID, MQTT_USER, MQTT_TOKEN)) {
    Serial.println("[+] MQTT Connected");
    mqtt.subscribe(MQTT_TOPIC_DISPLAY);
    
  } else {
    Serial.println("[x] MQTT Failed to connect!");
    isOk += 1;
    ESP.restart();
  }
}

//
CommandType getCommandType(const char* key) {
  if (strcmp(key, "suspend_json_export") == 0) return SUSPEND_JSON_EXPORT;
  if (strcmp(key, "Interval") == 0 ) return CHANGE_POLLING_INTERVAL;
  if (strcmp(key, "Color") == 0 ) return CHANGE_NEOPIXEL_COLOR;
}
//check command and apply commmand based on json object received from the broker (display topic cmd)
void apply_remote_command(JsonObject p){
  for (JsonPair key_value : p){
    const char* key = key_value.key().c_str();
    JsonVariant value = key_value.value();

    switch(getCommandType(key)){
      case SUSPEND_JSON_EXPORT:
        if (value.as<bool>()){
          jsonExport = false;
          Serial.println("[<=] JSON export logs suspended");
        }
        else{
          jsonExport = true;
          Serial.println("[<=] JSON export logs restarted");
        }
        break;

      case CHANGE_POLLING_INTERVAL:
        delay_time = value.as<int>();
        delay_time = delay_time * 1000;
        Serial.print("[<=] Polling Interval changed to:");
        Serial.print(delay_time);
        Serial.print("ms");
        break;
      
      case CHANGE_NEOPIXEL_COLOR: {
        if (p.containsKey("color")) {
          JsonObject colorObj = p["color"].as<JsonObject>();
          Color c = getColor(colorObj);
          NeoPixel_setColor(c);
        }else {
          Serial.println("[X] No 'color' object found in JSON!");
        } 
        break;
      }

      case UNKNOWN_COMMAND:
        Serial.println("Unknown command.");
      default:
        Serial.println("No Valid command found.");
        break;
    }

  }
}

//check log export
void check_json_log_export(bool j_e){
  if (!j_e){
      isOk += 1; //if true => exprot suspended
  }
}

//callback function
void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] : ");
  
  payload[length] = 0; // ensure valid content is zero terminated so can treat as c-string
  Serial.println((char *)payload);

  //create json object
  DeserializationError error = deserializeJson(jsonDoc2, (char *)payload);
  if (error) {
    Serial.print("[x] deserializeJson() failed: ");
    Serial.println(error.c_str());
    return;
  } 
  JsonObject p = jsonDoc2.as<JsonObject>();
  //manage receive commands
  apply_remote_command(p);
}

//check MQTT connection state
void check_MQTT_connectionState(){
  while (!mqtt.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqtt.connect(MQTT_DEVICEID, MQTT_USER, MQTT_TOKEN)) {
      Serial.println("MQTT Connected");
      mqtt.subscribe(MQTT_TOPIC_DISPLAY);
      
      mqtt.loop();
    } else {
      Serial.println("MQTT Failed to connect!");
      isOk += 1;
      delay(5000);
    }
  }
}

//send JSON message to MQTT broker
void send_JSON_MQTT(JsonObject p ){
  char jsonBuffer[512];
  serializeJson(p,jsonBuffer,sizeof(jsonBuffer));
  Serial.println("[=>] Sending msg to Broker"); 
  if (!mqtt.publish(MQTT_TOPIC, jsonBuffer)) {
    Serial.println("[x] MQTT Publish failed");
    isOk += 1;
  }
  else{
    Serial.println("[OK] Message Sent");
  }
}

//Led Green
void flash_LED(int led_pin,int ledMode){
  switch(ledMode){
    case 0:
      digitalWrite(led_pin, LOW);  // LED off
      break;
    case 1:
      digitalWrite(led_pin, HIGH); // LED on
      break;
    case 2:
      digitalWrite(led_pin, HIGH);
      delay(500);
      digitalWrite(led_pin, LOW);
      delay(500);                   // LED flashing
      break;
    default:
      break;
  }
}

//check system status
void check_system(){
  if (isOk == 0){
    flash_LED(LED_RED,0);
    flash_LED(LED_GREEN, 1);
  }
  else{
    Serial.println("[!] System in error state");
    flash_LED(LED_GREEN, 0);
    flash_LED(LED_RED,1); 
  }
}

/*
  API
*/
void handleMetrics() {
  //compute/get metrics values
  
  // CPU load approximation (FreeRTOS) 
  UBaseType_t numTasks = uxTaskGetNumberOfTasks();
  TaskStatus_t *taskStatus = (TaskStatus_t*)malloc(numTasks * sizeof(TaskStatus_t));
  String cpuLoad;
  if (taskStatus) {
    uxTaskGetSystemState(taskStatus, numTasks, NULL);
    unsigned long totalRunTime = 0;
    for (UBaseType_t i = 0; i < numTasks; i++){
      totalRunTime += taskStatus[i].ulRunTimeCounter;
    }
    cpuLoad = String(totalRunTime);
    free(taskStatus);
  } else {
    cpuLoad = "0";
  }
  // filesystem storage
  uint64_t totalBytes = 0, usedBytes = 0;
  if (fsys == (fs::FS*)&FFat) {
    totalBytes = FFat.totalBytes();
    usedBytes = FFat.usedBytes();
  } else if (fsys == (fs::FS*)&LittleFS) {
    totalBytes = LittleFS.totalBytes();
    usedBytes = LittleFS.usedBytes();
  }

  //Craft JSON to render
  //CPU load
  String json = "{";
  json += "\"cpuLoad\":" + cpuLoad + ",";
  // Heap RAM libre
  json += "\"heapFree\":" + String(ESP.getFreeHeap()) + ",";
  //Storage
  json += "\"storageTotal\":" + String(totalBytes) + ",";
  json += "\"storageUsed\":" + String(usedBytes);
  json += "}";

  //Headers
  server.sendHeader("Cache-Control", "no-cache");
  server.send(200, "application/json", json);
}

/*
      SETUP & LOOP
*/
//setup
void setup() {
  //LED Green & Red & Yellow
  pinMode(LED_GREEN, OUTPUT); //SYSTEM STATUS
  pinMode(LED_RED, OUTPUT); //SYSTEM STATUS
  pinMode(LED_YELLOW, OUTPUT); //WIFI STATE

  Serial.begin(115200);
  //init & start devices connected
  setup_wifi();
  dht.begin();
  strip.begin(); 
  //time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  //conect mqtt
  connect_MQTT_broker();

  //API setup
  //file system choice 
  if (FFat.begin(true)) fsys = &FFat;
  else if (LittleFS.begin(true)) fsys = &LittleFS;
  //JSON endpoint
  server.on("/metrics", HTTP_GET, handleMetrics);
  server.begin();
}

void loop() {
  server.handleClient();
  mqtt.loop();
  isOk = 0; // reset error counter 
  check_wifi_state(); 
  check_MQTT_connectionState();
  check_json_log_export(jsonExport);
  if (jsonExport){
    DHTMetrics m = get_DHT_metrics();
    JsonObject p = craft_metrics_json(m);
    send_JSON_MQTT(p);
    delay(delay_time);
  }
  //check system status and ajust LED GREEN & RED
  check_system();
  delay(1000);
}
