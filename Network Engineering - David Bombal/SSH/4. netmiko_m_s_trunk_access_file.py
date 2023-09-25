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

with open("iosv_l2_config.txt") as f:
    lines = f.read().splitlines()
print(lines)

for device in devices:
    print(f"Snazim sa pripojit na switch k zariadeniu: {device['ip']}")
    net_connect = ConnectHandler(**device)
    print(f"\n\nÚspešné pripojenie k {device['ip']}")

    output = net_connect.send_config_set(lines)
    print(output)

    net_connect.disconnect()
