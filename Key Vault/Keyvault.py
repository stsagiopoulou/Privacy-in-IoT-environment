from bluetooth import *
import sys
import time
import threading
import sys
import paillier
import os
import time
import pickle

#execute the file genkeys.py to generate the public and the private keys
picklefile = open('keys', 'rb')
keys = pickle.load(picklefile)
picklefile.close()
priv,pub= keys

while True:
    if sys.version < '3':
        input = raw_input


    addr = "B8:27:EB:94:D0:4A"

    if len(sys.argv) < 2:
        print("No device.")
        print("The sample Service")
    else:
        addr = sys.argv[1]
        print("Searching for SampleServer on %s" % addr)


    uuid= "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = find_service( uuid = uuid, address = addr )

    if len(service_matches) == 0:
        print("Couldn't find SampleServer service")
        #sys.exit(0)
        time.sleep(3)
        continue

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"%s\" on %s" % (name,host))

    sock=BluetoothSocket (RFCOMM)
    sock.connect((host, port))

    print("Connected")
	#send only the public key to storage
    keys=pickle.dumps(pub)
    sock.send(keys)
    try:
        while True:
            sums = sock.recv(1024)
            x= paillier.decrypt(priv,pub,int(sums))
            sock.send(str(x).encode('utf8'))
            print("received [%s]" % x)
   
    except IOError:
       pass
    sock.close()
