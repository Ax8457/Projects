# Source files of the project

## Features implemented
**[Hardware]**

- The Red LED is lighting if the system enters a critical state, for instance if the metrics export fails, if the JSON export is suspended, if the sensor is unplugged ...
- The Green LED remains lighting if no problem is encountered
- The Yellow LED indicates if the connection to Wi-Fi is OK. If the yellow led is off, it means the connection to the network has been lost.
- The NeoPixel follows temperature thresholds and auto updates the color of the pixel (from green to red). It raises alerts as well, displayed directly on the dashboard
- The device exports metrics and data in JSON format


**[Commands]**
- Possibility to suspend JSON export: it means the sensor no longer sends metrics to broker  
- Possibility to change NeoPixel color when the JSON export is suspended (otherwise the color is auto adjusted by thresholds and color immediately switch with respect to temperature). If multiple colors are selected, this is the first one in the JSON which is selected to update NeoPixel Color
- Possibility to increase polling interval: the payload sent is used to ticker delay between metrics sending on the ESP32

## Application source : application.c
<p align="justify"> This file contains the code uploaded on the ESP32. The IDE used is Arduino IDE and for this project following librabries are mandatory: </p>

- ESP-Wroom-32: _ESP32 dev module_
- JSON log export: _Arduino JSON_
- NeoPixel: _Adafruit NeoPixel_ 
- DHT sensor: _DHT sensor Library_ 

#### Details of functions

- Wifi : 
````c
void setup_wifi(){
  /*
    This function connects the esp32 to Wi-FI network using SSID and password. If the ESP32
    is successfuly connected to Wi-Fi, the yellow LED switches on.
  */
}

void void check_wifi_state(){
  /*
    This function checks the wifi state, while the connection is lost, the esp32 tries to reconnect.
  */
}
````

- DHT sensor
````c
DHTMetrics gets_DHT_metrics(){
  /*
    This function use DHT sensor library to get metrics measured by the sensor namely humidity
    and return a custom DHT structure variable containing metrics.
  */
}

JsonObject craft_metrics_json(DHTMetrics m){
  /*
    This function handles DHTMetrics object returned by the previous function to return a
    JSON object containing well formated payload with metrics.
  */
}
````

- NeoPixel and LEDs
````c
void NeoPixel_setColor(Color c){
  /*
    This function takes an ENUM type color argument (custom) and set the corresponding color of the NeoPixel.
  */
}

void flash_LED(int led_pin,int ledMode){
  /*
    This function takes LED pin on the ESP32 and LED Mod (3 mods possibles swicth on, off and lighting) as arguments
    and updates right LED state.
  */
}

Color getColor(JsonObject o){
  /*
    This function takes JSON Object received and handled by callback() function and extract the key (here a color) set
    to true. Then the right Color type ENUM is returned (to be passed to NeoPixel_setColor function).
  */
}
````

- MQTT comunication
````c
void connect_MQTT_broker(){
  /*
    This function establishes connection with public hiveMQ MQTT broker. 
  */
}

void check_MQTT_connectionState(){
  /*
    This function checks connection state with the broker. While the connection is
    lost, it tries to reconnect.
  */
}

void send_JSON_MQTT(JsonObject p ){
  /*
    This function takes the JSON formated object returned by craft_metrics_json()
    and sends the JSON paylaod to MQTT Broker (on the right topic).
  */
}

void callback(char* topic, byte* payload, unsigned int length) {
  /*
    This function listens on command topic on the broker and is used to interpret and execute
    remote commands received by the management server.
  */
}
````
- Commands processing
````c
CommandType getCommandType(const char* key) {
  /*
    This function takes extracted keys from JSON object received and handled by callback() function,
    and maps the right ENUM CommandType type.
  */
}

void apply_remote_command(JsonObject p){
  /*
    This function takes JSON object received and handled by callback() function, extracts the keys from JSON and
    calls getCommandType() to get the CommandType associated. Then the right section of code is executed.
  */
}
````
- System health
````c
void check_system(){
  /*
    This function is called at each loop and checks system's health. A boolean is incremented if an issue is encountered
    by different check functions . The score is set to 0 at each loop start and at the if the score is different from zero,
    RED LED switches on.
  */
}
````
