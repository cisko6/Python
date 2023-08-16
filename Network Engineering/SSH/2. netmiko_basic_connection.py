#!/usr/bin/env python3

from netmiko import ConnectHandler

# DEVICE, IP, USERNAME, PASSWORD
iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.122.51',
    'username': 'ciso',
    'password': 'cisco',
}

# CONNECT
net_connect = ConnectHandler(**iosv_l2)
output = net_connect.send_command('show vlan\n')
print(output)

print("Ak chceš vytvoriť 2-20 VLAN - press 1\n"
      "Ak chceš vymazať 2-20 VLAN - press 2")
while True:
    try:
        vysl = int(input())
        if vysl < 1 or vysl > 2:
            print("Musíš zadať len 1 alebo 2!")
            continue
        else:
            break
    except ValueError as e:
        print("Chyba: " + str(e))


if vysl == 1:
    for i in range(2, 21):
        print("Creating VLAN" + str(i) + "\n")
        config_commands = ['vlan ' + str(i) + ' ', 'name NETMIKO_VLAN_' + str(i), 'exit']
        net_connect.send_config_set(config_commands)
else:
    for i in range(2, 21):
        print("Deleting VLAN" + str(i) + "\n")
        config_commands = ['no vlan ' + str(i) + ' ', 'exit']
        net_connect.send_config_set(config_commands)

output = net_connect.send_command('show vlan\n')
print(output)

net_connect.disconnect()
print("\nSuccessfully disconnected\n")
