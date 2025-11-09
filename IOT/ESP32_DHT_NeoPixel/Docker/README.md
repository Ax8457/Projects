# Docker Network files

<p align="justify">For this project the cloud storage and remote server used are not cloud instances but local dockers with volumes:</p>

- 1 Docker for nodred application
- 1 Docker for mongodb storage
<p align="justify">Below is the schema of network architecture:</p>

<p align="center"><img src="S.png" style="width:45%"></p>

<p align="justify">To build the 2 dockers: </p>

````bash
sudo docker-compose build
sudo docker-compose up
````

<p align="justify">Once the image is build and containers are running mongodb can be accessed on the port 27017 of the localhost and the application Node-Red on the port 1880 (HTTP) </p>
