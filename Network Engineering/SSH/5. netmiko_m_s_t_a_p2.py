#!/usr/bin/env python3

from netmiko import ConnectHandler

devices = []

for i in reversed(range(1, 6)):
    name = "iosv_l2_" + str(i)
    ip = '192.168.122.5' + str(i)
    name = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'ciso',
        'password': 'cisco',
    }
    devices.append(name)

with open("iosv_l2_core.txt") as f:
    lines_core = f.read().splitlines()
print(lines_core)

with open("iosv_l2_access.txt") as f:
    lines_access = f.read().splitlines()
print(lines_access)

index = 0
for device in devices:
    print(f"Snazim sa pripojit na switch k zariadeniu: {device['ip']}")
    net_connect = ConnectHandler(**device)
    print(f"\n\nÚspešné pripojenie k {device['ip']}")
    if index < 3:
        output = net_connect.send_config_set(lines_access)
        print(output)
    else:
        output = net_connect.send_config_set(lines_core)
        print(output)
    index += 1
    net_connect.disconnect()

