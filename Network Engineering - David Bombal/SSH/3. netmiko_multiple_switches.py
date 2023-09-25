#!/usr/bin/env python3

from netmiko import ConnectHandler

devices = []

for i in range(1, 4):
    name = "iosv_l2_" + str(i)
    ip = '192.168.122.5' + str(i)
    name = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'ciso',
        'password': 'cisco',
    }
    devices.append(name)

for device in devices:
    net_connect = ConnectHandler(**device)
    print(f"\n\nÚspešné pripojenie k {device['ip']}")
    for j in range(2, 21):
        print("Working on vlan " + str(j))
        config_commands = ['vlan ' + str(j), 'name 3netmiko_VLAN_' + str(j), 'exit']
        #config_commands = ['no vlan ' + str(j), 'exit']
        net_connect.send_config_set(config_commands)
    output = net_connect.send_command('sh vlan brief')
    print(output)

    output = net_connect.send_command('wr')
    print(output)

    net_connect.disconnect()
