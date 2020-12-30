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

