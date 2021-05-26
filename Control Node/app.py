from bluetooth import *
import sys
import paillier
import requests
import threading
import multiprocessing
from multiprocessing import Process,Pipe
from flask import Flask, render_template, request, session,logging, url_for, redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from passlib.hash import sha256_crypt
import os
import time
import foperations
import fingerprint
import iptc
import pickle
import RPi.GPIO as GPIO

f = open("motions.txt", "a")

global sum1,sum2,sum3,sum4,sum5,sum6,sum7,sum8,sum9,sum10,sum11,sum12
engine = create_engine("mysql+pymysql://root:yourpassword@localhost/register")
db=scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
colors = [
    "rgba(10,20,30,0.3)","#008000","#0000FF","#800080"]
labels =['Εικόνα','Ήχος','Κίνηση','Περιβάλλον']
labels2 =['Εικόνα/χρήστες','Εικόνα/εσύ','Ήχος/χρήστες','Ήχος/εσύ','Κίνηση/χρήστες','Κίνηση/εσύ','Περιβάλλον/χρήστες','Περιβάλλον/εσύ']

def processmotion():
   PIR    = 23
   PIR2   = 24

   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(PIR, GPIO.IN)
   GPIO.setup(PIR2, GPIO.IN) 
   try:
        time.sleep(2)
        while True:
            if GPIO.input(PIR) == 1:
                f.write("Sensor=1\n")
            if GPIO.input(PIR2) == 1:
                f.write("Sensor=2\n")

   except KeyboardInterrupt:
        GPIO.cleanup()

def processident(): #identification, in and out process, creates iptables
  server_sock=BluetoothSocket( RFCOMM )
  server_sock.bind(("",PORT_ANY))
  server_sock.listen(1)

  port = server_sock.getsockname()[1]
  uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

  advertise_service( server_sock, "SampleServer",
                        service_id = uuid,
                        service_classes = [ uuid, SERIAL_PORT_CLASS ],
                        profiles = [ SERIAL_PORT_PROFILE ],
  #                protocols = [ OBEX_UUID ]
                     )
  print("Waiting for connection on RFCOMM channel %d" % port)

  client_sock, client_info = server_sock.accept()
  print("Accepted connection from ", client_info)
  keys=client_sock.recv(1024)
  pub=pickle.loads(keys)
  while True:
    time.sleep(4)
    os.system('sudo sh -c "iptables-legacy-save > /etc/iptables.ipv4.nat"')
    time.sleep(2)
    fingerprint.cmosled(1)
    foperations.capture(0)
    time.sleep(1)
    fingerprint.cmosled(0)
    time.sleep(1)
    y=fingerprint.identify()
    print(y)
    if y!=2 or y!=3:
         id=int(str(y),16)
         print(id)
         os.system('sudo iptables-legacy -F FORWARD')
         os.system('sudo iptables-legacy -F RATE-LIMIT')
         os.system('sudo iptables-legacy -X RATE-LIMIT')

         global sum1
         global sum2
         global sum3
         global sum4
         global sum5
         global sum6
         global sum7
         global sum8
         global sum9
         global sum10
         global sum11
         global sum12
         with open("motions.txt", "r") as file:
             first_line = file.readline()
             for last_line in file:
                   pass
         print (last_line)
         if last_line=="Sensor=1\n": #the user enters the IoT environment, add her preferences to the sum
                    
                    l=db.execute("select sum1,sum2,sum3,sum4,sum5,sum6,sum7,sum8,sum9,sum10,sum11,sum12 from sums")
                    db.commit()
                    for y in l:
                            
                            if y[0] is None:
                               
                               par=0
                               sum1=sum2=sum3=sum4=sum5=sum6=sum7=sum8=sum9=sum10=sum11=sum12=paillier.encrypt(pub,par)
                               db.execute("update sums set sum1=(:sum1),sum2=(:sum2),sum3=(:sum3),sum4=(:sum4),sum5=(:sum5),sum6=(:sum6),sum7=(:sum7),sum8=(:sum8),sum9=(:sum9),sum10=(:sum10),sum11=(:sum11),sum12=(:sum12) where id='1'",{"sum1":sum1,"sum2":sum2,"sum3":sum3,"sum4":sum4,"sum5":sum5,"sum6":sum6,"sum7":sum7,"sum8":sum8,"sum9":sum9,"sum10":sum10,"sum11":sum11,"sum12":sum12})
                               db.commit()

                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    k=db.execute("select sum1,sum2,sum3,sum4,sum5,sum6,sum7,sum8,sum9,sum10,sum11,sum12 from sums")
                    db.commit()
                    for x in r:
                        for y in k:
                                sum1=paillier.e_add(pub,int(y[0]),int(x[1]))
                                sum2=paillier.e_add(pub,int(y[1]),int(x[2]))
                                sum3=paillier.e_add(pub,int(y[2]),int(x[3]))
                                sum4=paillier.e_add(pub,int(y[3]),int(x[4]))
                                sum5=paillier.e_add(pub,int(y[4]),int(x[5]))
                                sum6=paillier.e_add(pub,int(y[5]),int(x[6]))
                                sum7=paillier.e_add(pub,int(y[6]),int(x[7]))
                                sum8=paillier.e_add(pub,int(y[7]),int(x[8]))
                                sum9=paillier.e_add(pub,int(y[8]),int(x[9]))
                                sum10=paillier.e_add(pub,int(y[9]),int(x[10]))
                                sum11=paillier.e_add(pub,int(y[10]),int(x[11]))
                                sum12=paillier.e_add(pub,int(y[11]),int(x[12]))
                                db.execute("update sums set sum1=(:sum1),sum2=(:sum2),sum3=(:sum3),sum4=(:sum4),sum5=(:sum5),sum6=(:sum6),sum7=(:sum7),sum8=(:sum8),sum9=(:sum9),sum10=(:sum10),sum11=(:sum11),sum12=(:sum12)  where id='1'",{"sum1":sum1,"sum2":sum2,"sum3":sum3,"sum4":sum4,"sum5":sum5,"sum6":sum6,"sum7":sum7,"sum8":sum8,"sum9":sum9,"sum10":sum10,"sum11":sum11,"sum12":sum12})
                                db.commit()
         else: #the user leaves the IoT environment
            sums = db.execute("select sum1,sum2,sum3,sum4,sum5,sum6,sum7,sum8,sum9,sum10,sum11,sum12 from sums")
            db.commit()
            #send to Key Vault to decrypt
            for i in sums:
                 client_sock.send(i[0])
                 data=client_sock.recv(1024)
                 string= data.decode('utf8')
                 num=int(string)

                 client_sock.send(i[1])
                 data1=client_sock.recv(1024)
                 string1= data1.decode('utf8')
                 num1=int(string1)

                 client_sock.send(i[2])
                 data2=client_sock.recv(1024)
                 string2= data2.decode('utf8')
                 num2=int(string2)

                 client_sock.send(i[3])
                 data3=client_sock.recv(1024)
                 string3= data3.decode('utf8')
                 num3=int(string3)

                 client_sock.send(i[4])
                 data4=client_sock.recv(1024)
                 string4= data4.decode('utf8')
                 num4=int(string4)


                 client_sock.send(i[5])
                 data5=client_sock.recv(1024)
                 string5= data5.decode('utf8')
                 num5=int(string5)

                 client_sock.send(i[6])
                 data6=client_sock.recv(1024)
                 string6= data6.decode('utf8')
                 num6=int(string6)

                 client_sock.send(i[7])
                 data7=client_sock.recv(1024)
                 string7= data7.decode('utf8')
                 num7=int(string7)

                 client_sock.send(i[8])
                 data8=client_sock.recv(1024)
                 string8= data8.decode('utf8')
                 num8=int(string8)

                 client_sock.send(i[9])
                 data9=client_sock.recv(1024)
                 string9= data9.decode('utf8')
                 num9=int(string9)

                 client_sock.send(i[10])
                 data10=client_sock.recv(1024)
                 string10= data10.decode('utf8')
                 num10=int(string10)

                 client_sock.send(i[11])
                 data11=client_sock.recv(1024)
                 string11= data11.decode('utf8')
                 num11=int(string11)
                 #substract the user's preferences from the summary
                 if num==0:
                       l=db.execute("select sum1 from sums")
                       db.commit()
                       for sum in l:
                          sum1=sum[0]
                       db.execute("update sums set sum1=(:sum1) where id='1'",{"sum1":sum1})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s1=db.execute("select sum1 from sums")
                    db.commit()
                    for x in r:
                        for y in s1:
                            x1=paillier.inv(int(x[1]),pub)
                            sum1=paillier.e_add(pub,int(y[0]),x1)
                    db.execute("update sums set sum1=(:sum1) where id='1'",{"sum1":sum1})
                    db.commit()

                 if num1==0:
                       l=db.execute("select sum2 from sums")
                       db.commit()
                       for sum in l:
                          sum2=sum[0]
                       db.execute("update sums set sum2=(:sum2) where id='1'",{"sum2":sum2})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s2=db.execute("select sum2 from sums")
                    db.commit()
                    for x in r:
                        for y in s2:
                            x2=paillier.inv(int(x[2]),pub)
                            sum2=paillier.e_add(pub,int(y[0]),x2)
                    db.execute("update sums set sum2=(:sum2) where id='1'",{"sum2":sum2})
                    db.commit()

                 if num2==0:
                       l=db.execute("select sum3 from sums")
                       db.commit()
                       for sum in l:
                          sum3=sum[0]
                       db.execute("update sums set sum3=(:sum3) where id='1'",{"sum3":sum3})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s3=db.execute("select sum3 from sums")
                    db.commit()
                    for x in r:
                        for y in s3:
                            x3=paillier.inv(int(x[3]),pub)
                            sum3=paillier.e_add(pub,int(y[0]),x3)
                    db.execute("update sums set sum3=(:sum3) where id='1'",{"sum3":sum3})
                    db.commit()
                  
                 if num3==0:
                       l=db.execute("select sum4 from sums")
                       db.commit()
                       for sum in l:
                          sum4=sum[0]
                       db.execute("update sums set sum4=(:sum4) where id='1'",{"sum4":sum4})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s4=db.execute("select sum4 from sums")
                    db.commit()
                    for x in r:
                        for y in s4:
                            x4=paillier.inv(int(x[4]),pub)
                            sum4=paillier.e_add(pub,int(y[0]),x4)
                    db.execute("update sums set sum4=(:sum4) where id='1'",{"sum4":sum4})
                    db.commit()
                 
                 if num4==0:
                       l=db.execute("select sum5 from sums")
                       db.commit()
                       for sum in l:
                          sum5=sum[0]
                       db.execute("update sums set sum5=(:sum5) where id='1'",{"sum5":sum5})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s5=db.execute("select sum5 from sums")
                    db.commit()
                    for x in r:
                        for y in s5:
                            x5=paillier.inv(int(x[5]),pub)
                            sum5=paillier.e_add(pub,int(y[0]),x5)
                    db.execute("update sums set sum5=(:sum5) where id='1'",{"sum5":sum5})
                    db.commit()

                 if num5==0:
                       l=db.execute("select sum6 from sums")
                       db.commit()
                       for sum in l:
                          sum6=sum[0]
                       db.execute("update sums set sum6=(:sum6) where id='1'",{"sum6":sum6})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s6=db.execute("select sum6 from sums")
                    db.commit()
                    for x in r:
                        for y in s6:
                            x6=paillier.inv(int(x[6]),pub)
                            sum6=paillier.e_add(pub,int(y[0]),x6)
                    db.execute("update sums set sum6=(:sum6) where id='1'",{"sum6":sum6})
                    db.commit()
                 
                 if num6==0:
                       l=db.execute("select sum7 from sums")
                       db.commit()
                       for sum in l:
                          sum7=sum[0]
                       db.execute("update sums set sum7=(:sum7) where id='1'",{"sum7":sum7})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s7=db.execute("select sum7 from sums")
                    db.commit()
                    for x in r:
                        for y in s7:
                            x7=paillier.inv(int(x[7]),pub)
                            sum7=paillier.e_add(pub,int(y[0]),x7)
                    db.execute("update sums set sum7=(:sum7) where id='1'",{"sum7":sum7})
                    db.commit()
                 
                 if num7==0:
                       l=db.execute("select sum8 from sums")
                       db.commit()
                       for sum in l:
                          sum8=sum[0]
                       db.execute("update sums set sum8=(:sum8) where id='1'",{"sum8":sum8})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s8=db.execute("select sum8 from sums")
                    db.commit()
                    for x in r:
                        for y in s8:
                            x8=paillier.inv(int(x[8]),pub)
                            sum8=paillier.e_add(pub,int(y[0]),x8)
                    db.execute("update sums set sum8=(:sum8) where id='1'",{"sum8":sum8})
                    db.commit()

                 if num8==0:
                       l=db.execute("select sum9 from sums")
                       db.commit()
                       for sum in l:
                          sum9=sum[0]
                       db.execute("update sums set sum9=(:sum9) where id='1'",{"sum9":sum9})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s9=db.execute("select sum9 from sums")
                    db.commit()
                    for x in r:
                        for y in s9:
                            x9=paillier.inv(int(x[9]),pub)
                            sum9=paillier.e_add(pub,int(y[0]),x9)
                    db.execute("update sums set sum9=(:sum9) where id='1'",{"sum9":sum9})
                    db.commit()

                 if num9==0:
                       l=db.execute("select sum10 from sums")
                       db.commit()
                       for sum in l:
                          sum10=sum[0]
                       db.execute("update sums set sum10=(:sum10) where id='1'",{"sum10":sum10})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s10=db.execute("select sum10 from sums")
                    db.commit()
                    for x in r:
                        for y in s10:
                            x10=paillier.inv(int(x[10]),pub)
                            sum10=paillier.e_add(pub,int(y[0]),x10)
                    db.execute("update sums set sum10=(:sum10) where id='1'",{"sum10":sum10})
                    db.commit()

                 if num10==0:
                       l=db.execute("select sum11 from sums")
                       db.commit()
                       for sum in l:
                          sum11=sum[0]
                       db.execute("update sums set sum11=(:sum11) where id='1'",{"sum11":sum11})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s11=db.execute("select sum11 from sums")
                    db.commit()
                    for x in r:
                        for y in s11:
                            x11=paillier.inv(int(x[11]),pub)
                            sum11=paillier.e_add(pub,int(y[0]),x11)
                    db.execute("update sums set sum11=(:sum11) where id='1'",{"sum11":sum11})
                    db.commit()

                 if num11==0:
                       l=db.execute("select sum12 from sums")
                       db.commit()
                       for sum in l:
                          sum12=sum[0]
                       db.execute("update sums set sum12=(:sum12) where id='1'",{"sum12":sum12})
                       db.commit()
                 else:
                    r=db.execute("select * from preferences where id in (select i from idfin where id=(:id))",{"id":id})
                    s12=db.execute("select sum12 from sums")
                    db.commit()
                    for x in r:
                        for y in s12:
                            x12=paillier.inv(int(x[12]),pub)
                            sum12=paillier.e_add(pub,int(y[0]),x12)
                    db.execute("update sums set sum12=(:sum12) where id='1'",{"sum12":sum12})
                    db.commit()
         #send to Key Vault to decrypt
         sums = db.execute("select sum1,sum2,sum3,sum4,sum5,sum6,sum7,sum8,sum9,sum10,sum11,sum12 from sums")
         db.commit()
         for i in sums:
                 client_sock.send(i[0])
                 data=client_sock.recv(1024)
                 string= data.decode('utf8')
                 num=int(string)

                 client_sock.send(i[1])
                 data1=client_sock.recv(1024)
                 string1= data1.decode('utf8')
                 num1=int(string1)

                 client_sock.send(i[2])
                 data2=client_sock.recv(1024)
                 string2= data2.decode('utf8')
                 num2=int(string2)

                 client_sock.send(i[3])
                 data3=client_sock.recv(1024)
                 string3= data3.decode('utf8')
                 num3=int(string3)

                 client_sock.send(i[4])
                 data4=client_sock.recv(1024)
                 string4= data4.decode('utf8')
                 num4=int(string4)


                 client_sock.send(i[5])
                 data5=client_sock.recv(1024)
                 string5= data5.decode('utf8')
                 num5=int(string5)

                 client_sock.send(i[6])
                 data6=client_sock.recv(1024)
                 string6= data6.decode('utf8')
                 num6=int(string6)

                 client_sock.send(i[7])
                 data7=client_sock.recv(1024)
                 string7= data7.decode('utf8')
                 num7=int(string7)

                 client_sock.send(i[8])
                 data8=client_sock.recv(1024)
                 string8= data8.decode('utf8')
                 num8=int(string8)

                 client_sock.send(i[9])
                 data9=client_sock.recv(1024)
                 string9= data9.decode('utf8')
                 num9=int(string9)

                 client_sock.send(i[10])
                 data10=client_sock.recv(1024)
                 string10= data10.decode('utf8')
                 num10=int(string10)

                 client_sock.send(i[11])
                 data11=client_sock.recv(1024)
                 string11= data11.decode('utf8')
                 num11=int(string11)
				 
         #create the iptables
         if num >= 1:
                 i=db.execute("select IP from devices where category='eikona'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
         if num3 >= 1:
                 i=db.execute("select IP from devices where category='ixos'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
         if num6 >= 1:
                 i=db.execute("select IP from devices where category='kinisi'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
         if num9 >= 1:
                 i=db.execute("select IP from devices where category='periballon'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
         if num1 >= 1:
                 i=db.execute("select IP,IPtrust from devices where category='eikona'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         rule.dst = w[1]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
         
         if num4 >= 1:
                 i=db.execute("select IP,IPtrust from devices where category='ixos'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         rule.dst = w[1]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
            
         if num7 >= 1:
                 i=db.execute("select IP,IPtrust from devices where category='kinisi'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         rule.dst = w[1]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
         
         if num10 >= 1:
                 i=db.execute("select IP,IPtrust from devices where category='periballon'")
                 db.commit()
                 for w in i:
                     if w[0]!=0:
                         rule = iptc.Rule()
                         rule.src = w[0]
                         rule.dst = w[1]
                         match = iptc.Match(rule, "physdev")
                         match.physdev_in = "wlan0"
                         match.physdev_out = "eth0"
                         rule.add_match(match)
                         rule.target = iptc.Target(rule, "DROP")
                         chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                         table = iptc.Table(iptc.Table.FILTER)
                         chain.insert_rule(rule)
            
         if num2 >= 1 or num5 >= 1 or num8 >=1 or num11 >= 1:

                     table = iptc.Table(iptc.Table.FILTER)
                     chain = table.create_chain("RATE-LIMIT")

                     rule = iptc.Rule()
                     rule.target = iptc.Target(rule, "ACCEPT")
                     match = iptc.Match(rule, "hashlimit")
                     chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "RATE-LIMIT")
                     table = iptc.Table(iptc.Table.FILTER)
                     match.hashlimit_name = 'droprate'
                     match.hashlimit_mode = 'srcip'
                     match.hashlimit_upto = '10/sec'
                     match.hashlimit_burst = '20'
                     match.hashlimit_htable_expire = '1100'
                     rule.add_match(match)
                     chain.insert_rule(rule)

                     rule.target = iptc.Target(rule, "DROP")
                     chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "RATE-LIMIT")
                     table = iptc.Table(iptc.Table.FILTER)
                     chain.insert_rule(rule)
                     if num2 >= 1:
                         i=db.execute("select IP from devices where category='eikona'")
                         db.commit()
                         for w in i:
                             if w[0]!=0:
                                rule = iptc.Rule()
                                rule.src = w[0]
                                match = iptc.Match(rule, "physdev")
                                match.physdev_in = "wlan0"
                                match.physdev_out = "eth0"
                                rule.add_match(match)
                                rule.target = iptc.Target(rule, "RATE-LIMIT")
                                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                                table = iptc.Table(iptc.Table.FILTER)
                                chain.insert_rule(rule)
                     if num5 >= 1:
                         i=db.execute("select IP from devices where category='ixos'")
                         db.commit()
                         for w in i:
                             if w[0]!=0:
                                rule = iptc.Rule()
                                rule.src = w[0]
                                match = iptc.Match(rule, "physdev")
                                match.physdev_in = "wlan0"
                                match.physdev_out = "eth0"
                                rule.add_match(match)
                                rule.target = iptc.Target(rule, "RATE-LIMIT")
                                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                                table = iptc.Table(iptc.Table.FILTER)
                                chain.insert_rule(rule)
                     if num8 >= 1:
                         i=db.execute("select IP from devices where category='kinisi'")
                         db.commit()
                         for w in i:
                             if w[0]!=0:
                                rule = iptc.Rule()
                                rule.src = w[0]
                                match = iptc.Match(rule, "physdev")
                                match.physdev_in = "wlan0"
                                match.physdev_out = "eth0"
                                rule.add_match(match)
                                rule.target = iptc.Target(rule, "RATE-LIMIT")
                                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                                table = iptc.Table(iptc.Table.FILTER)
                                chain.insert_rule(rule)
                     if num11 >= 1:
                         i=db.execute("select IP from devices where category='periballon'")
                         db.commit()
                         for w in i:
                             if w[0]!=0:
                                rule = iptc.Rule()
                                rule.src = w[0]
                                match = iptc.Match(rule, "physdev")
                                match.physdev_in = "wlan0"
                                match.physdev_out = "eth0"
                                rule.add_match(match)
                                rule.target = iptc.Target(rule, "RATE-LIMIT")
                                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
                                table = iptc.Table(iptc.Table.FILTER)
                                chain.insert_rule(rule)
         os.system('sudo sh -c "iptables-legacy-save > /etc/iptables.ipv4.nat"')

class MyClass2:
    p2 =  multiprocessing.Process(target=processmotion)
def start2():
    MyClass2.p2.start()
    time.sleep(5)
def stop2():
    MyClass2.p2.terminate()
    MyClass2.p2.join()
    fingerprint.cmosled(0)

class MyClass:
    p =  multiprocessing.Process(target=processident)

def start():
    MyClass.p.start()
    time.sleep(5)
def stop():
    MyClass.p.terminate()
    MyClass.p.join()
    fingerprint.cmosled(0)


@app.route('/sign', methods=["GET","POST"])
def sign():
    if MyClass.p.is_alive():
       stop()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        secpass= sha256_crypt.encrypt(str(password))
        countrows = db.execute("SELECT * from (select COUNT(*) from users where name=(:name)) AS T1",{"name":name})
        db.commit()
        for x in countrows:
             if x[0]==0:
                db.execute("INSERT INTO users(name,password) VALUES (:name,:password)", {"name":name, "password":secpass})
                db.commit()
                return redirect(url_for('q'))
             else:
                error = 'Δοκίμασε άλλο όνομα.'
             return render_template('sign.html',error = error)

    return render_template('sign.html')

@app.route('/q', methods=["GET","POST"])
def q():
    if request.method == "POST":
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service( server_sock, "SampleServer",
                        service_id = uuid,
                        service_classes = [ uuid, SERIAL_PORT_CLASS ],
                        profiles = [ SERIAL_PORT_PROFILE ],
  #                protocols = [ OBEX_UUID ]
                     )
        print("Waiting for connection on RFCOMM channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)
        keys=client_sock.recv(1024)
        pub=pickle.loads(keys)

        x = int(request.form.get("q1"))
        y= paillier.encrypt(pub,x)
        q1=str(y)

        x2 = int(request.form.get("q2"))
        y2= paillier.encrypt(pub,x2)
        q2=str(y2)

        x3 = int(request.form.get("q3"))
        y3= paillier.encrypt(pub,x3)
        q3=str(y3)

        x4 = int(request.form.get("q4"))
        y4= paillier.encrypt(pub,x4)
        q4=str(y4)

        x5 = int(request.form.get("q5"))
        y5= paillier.encrypt(pub,x5)
        q5=str(y5)

        x6 = int(request.form.get("q6"))
        y6= paillier.encrypt(pub,x6)
        q6=str(y6)

        x7 = int(request.form.get("q7"))
        y7= paillier.encrypt(pub,x7)
        q7=str(y7)

        x8 = int(request.form.get("q8"))
        y8= paillier.encrypt(pub,x8)
        q8=str(y8)

        x9 = int(request.form.get("q9"))
        y9= paillier.encrypt(pub,x9)
        q9=str(y9)

        x10 = int(request.form.get("q10"))
        y10= paillier.encrypt(pub,x10)
        q10=str(y10)

        x11 = int(request.form.get("q11"))
        y11= paillier.encrypt(pub,x11)
        q11=str(y11)

        x12 = int(request.form.get("q12"))
        y12= paillier.encrypt(pub,x12)
        q12=str(y12)

        db.execute("INSERT INTO preferences(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12) VALUES (:q1,:q2,:q3,:q4,:q5,:q6,:q7,:q8,:q9,:q10,:q11,:q12)", {"q1":q1,"q2":q2,"q3":q3,"q4":q4,"q5":q5,"q6":q6,"q7":q7,"q8":q8,"q9":q9,"q10":q10,"q11":q11,"q12":q12})
        db.commit()
   
        return render_template('instructions.html')
    else:
        return render_template('q.html')

    return render_template('q.html')

@app.route('/log',methods=["GET","POST"])
def log():
    if request.method == "POST":
        global name
        name = request.form.get("name")
        password = request.form.get("password")
        secpass= sha256_crypt.encrypt(str(password))
        if name=='admin':
            result2=db.execute("SELECT * FROM devices")
            return render_template('admin.html', value=result2)

        else:
            namedata = db.execute("SELECT name FROM users WHERE (:name)",{"name":name})
            passwordata = db.execute("SELECT * FROM users WHERE name=(:name)",{"name":name})
            db.commit()
            for pass_word in passwordata:
                if sha256_crypt.verify(password,pass_word[2]):
                    return render_template('bar.html')
                else:
                    error = 'Something went wrong,try again!'
                    return render_template('log.html',error=error)

    return render_template('log.html')

@app.route('/delete/<name>')
def delete(name):
    db.execute("DELETE FROM devices where name=(:name)",{"name":name})
    db.commit()
    return render_template('thanks3.html')

@app.route('/insert',methods=["GET","POST"])
def insert():
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        mac = request.form.get("mac")
        IP = request.form.get("IP")
        IPtrust = request.form.get("IPtrust")
        db.execute("INSERT INTO devices(name,category,mac,IP,IPtrust) VALUES (:name,:category,:mac,:IP,:IPtrust)", {"name":name, "category":category, "mac":mac, "IP":IP, "IPtrust":IPtrust})
        db.commit()
        return render_template('thanks3.html')

    return render_template('insert.html')

@app.route('/qupdate', methods=["GET","POST"])
def qupdate():
    if request.method == "POST":
        global name
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service( server_sock, "SampleServer",
                        service_id = uuid,
                        service_classes = [ uuid, SERIAL_PORT_CLASS ],
                        profiles = [ SERIAL_PORT_PROFILE ],
  #                protocols = [ OBEX_UUID ]
                     )
        print("Waiting for connection on RFCOMM channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)
        keys=client_sock.recv(1024)
        pub=pickle.loads(keys)

        x = int(request.form.get("q1"))
        y= paillier.encrypt(pub,x)
        q1=str(y)

        x2 = int(request.form.get("q2"))
        y2= paillier.encrypt(pub,x2)
        q2=str(y2)

        x3 = int(request.form.get("q3"))
        y3= paillier.encrypt(pub,x3)
        q3=str(y3)

        x4 = int(request.form.get("q4"))
        y4= paillier.encrypt(pub,x4)
        q4=str(y4)

        x5 = int(request.form.get("q5"))
        y5= paillier.encrypt(pub,x5)
        q5=str(y5)

        x6 = int(request.form.get("q6"))
        y6= paillier.encrypt(pub,x6)
        q6=str(y6)

        x7 = int(request.form.get("q7"))
        y7= paillier.encrypt(pub,x7)
        q7=str(y7)

        x8 = int(request.form.get("q8"))
        y8= paillier.encrypt(pub,x8)
        q8=str(y8)

        x9 = int(request.form.get("q9"))
        y9= paillier.encrypt(pub,x9)
        q9=str(y9)

        x10 = int(request.form.get("q10"))
        y10= paillier.encrypt(pub,x10)
        q10=str(y10)

        x11 = int(request.form.get("q11"))
        y11= paillier.encrypt(pub,x11)
        q11=str(y11)

        x12 = int(request.form.get("q12"))
        y12= paillier.encrypt(pub,x12)
        q12=str(y12)

        db.execute("UPDATE preferences SET q1=(:q1),q2=(:q2),q3=(:q3),q4=(:q4),q5=(:q5),q6=(:q6),q7=(:q7),q8=(:q8),q9=(:q9),q10=(:q10),q11=(:q11),q12=(:q12) where id in (select id from users where name=(:name))",{"q1":q1,"q2":q2,"q3":q3,"q4":q4,"q5":q5,"q6":q6,"q7":q7,"q8":q8,"q9":q9,"q10":q10,"q11":q11,"q12":q12,"id":id,"name":name})
        db.commit()

        return render_template('thanks2.html')
    else:
        return render_template('qupdate.html')

    return render_template('qupdate.html')

@app.route('/process2', methods=["GET","POST"])
def process2(): #enrolls the fingerprints, and starts the processmotion(enables the motion sensors) and the processident(identification)
    global id
    global name
    fingerprint.cmosled(1)
    foperations.capture(0x0)
    time.sleep(1)
    fingerprint.cmosled(0)
    time.sleep(3)
    if fingerprint.identify()==3:
        for id in range(18):
            if foperations.enroll(0,id)==0:
                fingerprint.cmosled(0)
                time.sleep(3)
                continue
                foperations.enroll(0,id)
                id=id
            break
        start2()
        start()
        db.execute("insert into idfin (id) values (:id)",{"id":id})
        db.commit()
        return render_template('thanks.html')
    elif fingerprint.identify()==2:
        for id in range(18):
            if foperations.enroll(0,id)==0:
                fingerprint.cmosled(0)
                time.sleep(3)
                continue
                foperations.enroll(0,id)
                id=id
            break
        start2()
        start()
        db.execute("insert into idfin (id) values (:id)",{"id":id})
        db.commit()
        return render_template('thanks.html')
    else:
         return render_template('instructions.html')

if __name__ == '__main__':
     app.secret_key= b'\x10\xcd\xa0\xf8\xd9\x19\xf1 >/\n\xda\xba\x8b\xb7\x85\xb5\x08q\x08\xca\t\xdc\xc7'
     app.run(debug=True,port=80, host='0.0.0.0')


