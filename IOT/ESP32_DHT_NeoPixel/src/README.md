# Source files of the project

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
````
````c
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
````
