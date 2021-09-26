# Privacy-in-IoT-environment

## Manual

### Introduction
The proposed system is related to the privacy of users in a smart environment. It allows users to control (i) when the devices collect data, (ii) where they send them and (iii) their flow. This functionality is applied when the users enter the smart environment as their physical presence is recognized through their fingerprint and motion sensors. User preferences are encrypted with the Paillier cryptosystem to enhance privacy.   
In this project, we:  
* Implemented code to use a Raspberry Pi 3, model B+, as an access point for multiple IoT devices and to connect, in Python, a GT-511C1R fingerprint sensor and two PIR motion sensors to the Raspberry Pi.
* Created a database with MySQL to store and manipulate user data, preferences, fingerprints, and the security rules for each IoT device.
* Developed a firewall with iptables on the access point so that the IoT devices are calibrated according to the users’ collective security rules.
* Used Python’s Flask microframe, HTML and CSS, to create a web application that brings every component together.
* Used the Paillier cryptosystem to homomorphically encrypt user preferences.
* Used two PIR motion sensors to detect motion. This way, the system protects the information if a user is in the IoT environment
* Used two Raspberry Pi (hereby referred to as X and Y, respectively) which represent two communicating nodes with separate functions. Their role is to keep the private and public keys safe. Raspberry Y contains the private and public keys and decrypts the data. Raspberry X, (i) contains the database, (ii) is the access point, and (iii) connects with the sensors. The required information is passed from one Raspberry to the other via bluetooth communication
<img src="https://user-images.githubusercontent.com/76787087/103372743-85eb0f80-4adb-11eb-90f7-76f89a272588.png" width="500">

* *Raspberry Image from: "https://commons.wikimedia.org/wiki/File:Raspberry_Pi_3_illustration.svg"


### Establish communication between two Raspberry Pi 3 without internet
On both Raspberry:    
1. The Bluetooth chips must be unblocked using:  **`sudo rfkill unblock all`**
2. For coding in Python:  **`sudo apt-get install bluez pi-bluetooth python-bluez`**     

On Raspberry Y:
1. Enter bluetoothctl to open bluetooth control.
2. At the prompt enter the following commands:   
**`power on`**   
**`discoverable on`**   
**`pairable on`**   
**`agent on`**   
**`default-agent`**   

On Raspberry X:   
1. Enter bluetoothctl to open bluetooth control.     
2. At the prompt enter the following commands:      
**`power on`**    
**`discoverable on`**    
**`pairable on`**    
**`agent on`**    
**`default-agent`**    
**`scan on`**    
When the address of Raspberry Y pops up:     
**`pair <theaddressY>`**   
The devices need to be paired and trusted. Check this with the command:       
**`info <theaddressY>`**   
If they are not trusted enter:   
**`trust <theaddressY>`**   
To connect them some changes are required.   
1. Edit the file /etc/systemd/system/dbus-org.bluez.service   
**`sudo nano /etc/systemd/system/dbus-org.bluez.service`**   
**`Add –C to the line “xecStart=/usr/lib/bluetooth/bluetoothd”`**   
**`Add the line “ExecStartPost=/usr/bin/sdptool add SP”`**  
2. Reboot both of them and check if the SPP is running.    
	**`sudo sdptool browse local`**   
3. Create client and server.   
	On the first Pi: **`sudo rfcomm watch hci0`**    
	On the second Pi: **`sudo rfcomm watch hci0 <theaddress>`**       
  _Note: If there is an error “no advertisable device” when you run your python Script, run the command “sudo hciconfig hci0 piscan”._   
  
### How to connect the Raspberry Pi with the sensors
#### PIR Motion sensors
We use two motion sensors, one for inside movement detection and the other for outside movement. Three cables are needed to connect a PIR to Raspberry X:    
1. **one is used for ground (GND);**    
2. **the second is used for output pin (GPIO23); and,**    
3. **the last one is used for power (Vcc).**   

The sensor works for VCC 5-12V, so the green cable is plugged in the 5V pin on Raspberry X.    
<img src="https://user-images.githubusercontent.com/76787087/103378431-f3eb0300-4aea-11eb-978b-640de27cbbf8.png" width="350">     
We connect the other motion sensor following the same steps. However, we use a different output pin, the GPIO24.  

#### GT-511C1R Fingerprint sensor
The sensor works with serial communication and uses the UART protocol. To activate the communication between the fingerprint sensor and Raspberry X, we enable the serial port of X as follows:   
**`sudo raspi-config`**   
**`select option – Interface Options`**   
**`select option- Serial`**   
**`enable`**   
The UART needs two pins: one to read and the other to write. The UART pins of the Raspberry are GPIO14 (Tx) and GPIO15 (Rx). To connect the fingerprint sensor with Raspberry X we use four cables:   
1. connects the sensor’s Tx pin with the Rapsberry’s Rx;   
2. connects the sensor’s Rx pin with the Rapsberry’s Tx;   
3. for ground (GND); and,   
4. for power (Vcc).     

The sensor works for VCC 3.3-6V, so the red cable is plugged in the 3V pin of Raspberry X.     
<img src="https://user-images.githubusercontent.com/76787087/103378613-8c818300-4aeb-11eb-9009-7380c95aec73.png" width="350">     

### Using Raspberry Pi as access point
To control the traffic of IoT devices we use Raspberry X as access point. We connect Raspberry X with a router through an ethernet cable. A bridge must be created between the wireless device and the Ethernet device at Raspberry X access point. This bridge will pass all traffic between the two interfaces.    
1. Update and upgrade Raspberry X:   
**`sudo apt-get update`**    
**`sudo apt-get upgrade`**   
2. Install hostapd and bridge-utils:   
**`sudo apt-get install hostapd`**   
**`sudo apt-get install bridge-utils`**   
3. Unmask and activate hostapd to work properly:     
**`sudo systemctl unmask hostapd`**   
**`sudo systemctl enable hostapd`**      
**`sudo systemctl start hostapd`**    
4. Edit file /etc/hostapd/hostapd.conf to seem like the following:       
<img src="https://user-images.githubusercontent.com/76787087/103377236-7d003b00-4ae7-11eb-9833-6fccbb06391a.jpg" width="500">       
5. Edit file /etc/network/interfaces to seem like the following:       
<img src="https://user-images.githubusercontent.com/76787087/103377282-a7ea8f00-4ae7-11eb-9050-4a0e4e8be97d.png" width="500">      
6. Edit the file /etc/default/hostapd as follows: 

**`DAEMON_CONF=” /etc/hostapd/hostapd.conf”`**        
**`RUN_DAEMON=yes`**          
7. Reboot  

### Other libraries you need
**`sudo apt install mariadb-servers`**      
**`sudo apt-get install iptables`**    
**`sudo apt-get install python3 flask`**    
