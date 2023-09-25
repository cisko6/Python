#!/usr/bin/env python

import telnetlib
import getpass
import sys

user = raw_input("Meno uzivatela: ")
password = getpass.getpass()

f = open ("myswitches.txt")

for line in f:
    HOST = line.strip()
    tn = telnetlib.Telnet(HOST)

    tn.read_until("Username: ")
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ")
        tn.write(password + "\n")

    print ("Configuring switch: " + line + "\n")

    tn.write("terminal length 0\n")
    tn.write("show run\n")
    tn.write("exit\n")

    data = tn.read_all()
    output_file = open("/home/debian/switches/switch_" + HOST, "w")
    output_file.write(data)
    output_file.close()

f.close()
