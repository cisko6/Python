#!/usr/bin/env python

import telnetlib
import getpass
import sys

user = raw_input("Meno uzivatela: ")
password = getpass.getpass()

f = open ("myswitches.txt")

for line in f:
    print ("Configuring switch: " + line + "\n")
    HOST = line.strip()
    tn = telnetlib.Telnet(HOST)

    tn.read_until("Username: ")
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")

    tn.write("conf t\n")
    for j in range(2, 23):
        tn.write("vlan " + str(j) + "\n")
        tn.write("name Moja_VLAN_" + str(j)  + "\n")
        tn.write("exit\n")

    tn.write("end\n")
    tn.write("wr\n")
    tn.write("exit\n")

    print (tn.read_all())

f.close()
