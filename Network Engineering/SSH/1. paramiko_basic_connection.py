import time
import paramiko

ip_address = "192.168.122.51"
username = "ciso"
password = "cisco"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address,username=username,password=password)

print("Successful connection " + ip_address)

remote_connection = ssh_client.invoke_shell()

remote_connection.send("conf t\n")
remote_connection.send("int loop 0\n")
remote_connection.send("ip add 1.1.1.1 255.255.255.255\n")
remote_connection.send("exit\n")

for i in range(2, 21):
    remote_connection.send("no vlan " + str(i) + "\n")
    time.sleep(0.5)
remote_connection.send("end\n")


time.sleep(1)
output = remote_connection.recv(65535)
print(output)

ssh_client.close()
