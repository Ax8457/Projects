# Nodered source files

### Setup

<p align="justify">This project lies on Node-Red appliation (Javascript) to build dashboards and remotely control and monitor IOT device. Once Node-Red docker is running and reachable <a href="../Docker/">(Docker config)</a> Following palettes must be installed:</p>

- node-red-dashboard
- node-red
- node-red-mongodb

### Node-Red flows
<p align="justify">Each of the JSON files attached in this subfolder corresponds to a dedicated flow under Node-Red:</p>
  
- _Receive ESP32 data from Broker_ : This flow binds the broker and subscribes to the dedicated topic in order to receive metrics.
- _Store sensor Data_ : This flow binds the mongodb data and stores metrics received.
- _Plot DHT sensor Data_ : This flow creates a monitoring dashboard and plots DHT sensor live metrics.
- _Management Dashboard_ : This flow allows user to remotely send commands to ESP32 through dashboard connected to command topic of the broker.
- _Temperature Alerting via LEDs_ : This flow automatically tickers LED/NeoPixel color based on temperature thresholds.
- _Historical chart_ : This flow retreives data from database and plots longtime chart.

### JSON metrics
<p align="justify">The metric payloads are sent JSON formated and are processed and reshaped mutliple times going through different flows of Node-Red.</p>

#### step1 : Payload sent by ESP32 
````json
{
  "Metrics": {
    "Temperature_C": 23.8,
    "Temperature_F": 74.84,
    "Humidity": 38
  },
  "Time": {
    "Time": "Sunday, November 09 2025 23:14:06"
  }
}
````
<p align="justify"></p>
````json
{
  "_id": "6910f4be5b95620007ebf05c",
  "topic": "hwu-e6046365-0f8e-49c5-a33c-6638f5ae539f/evt/status/fmt/json",
  "payload": {
    "time": 1762718910035,
    "temp": 24.1,
    "humidity": 40,
    "location": "NUC"
  },
  "qos": 0,
  "retain": false,
  "_msgid": "dbf00595223e4520"
}
````
