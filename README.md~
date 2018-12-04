### Introduction
This is Merchant Cart demo of Music Festival for Inventory Management

### Pre-requisites
Create EC2 instance and enable port 8655 in security group to run your application in EC2.

### Setup in EC2
To install NodeJS :
```
	$ curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash –
	$ sudo apt-get install nodejs
```
To install Postgres :
```
    $ sudo apt-get update
    $ sudo apt-get install postgresql postgresql-contrib
```
Install NodeJS process Manager
```
$ npm install pm2 -g
```
### Adding application to EC2 instance:
Copy **webapp** folder to your EC2 instance.
```
 $ scp -i <pem file> -r webapp <EC2-instance-url>
```
## Run the application
Run the server in EC2 instance with : pm2 start

### Setup in Dragonboard 410c :
For serial communication you run the following command in Dragonboard 410c :
```
    $ pip install pyserial 
```
## Modify Configuration file as per your environment
Please, change the required highlighted configuration
```
{
    "usb_setting" : "/dev/ttyUSB0",
    "sensor_count": "5",
    "url_connect" : "http://<EC2-instance-IP>:8655/api/updateItem",
    "response_time": "60",
    "apn": "airtelgprs.com",
    "username": " ",
    "password": " ",
    "auth_id":"0"
}
```

### Run the application :
Run the following command in Dragonboard 410C 
```
 $ python main.py
 ``` 
