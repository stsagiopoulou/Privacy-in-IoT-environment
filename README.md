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

<img src="" width="500">
