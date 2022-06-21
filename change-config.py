#Note that before running this script, you need to create a folder called "output" in the same directory that you intend to run this from.
#Note2 please edit the "devices" file to match your devices.
#Note3 please edit the "vars.py" file and adjust your credentials etc

from netmiko import ConnectHandler
import io
import time
import getpass
import vars
import os

usern = vars.username
password = vars.password
secret = vars.secret
pt = vars.port
dev_type = vars.devicetype

localtime = time.localtime()
formattime = time.strftime("%d-%m-%Y %H:%M:%S" , localtime)
datetime = time.strftime("%d-%m-%Y" , localtime)

print("Starting tool...")

checkconfig = []
file = open("check-config.csv" , "r")
for line in file:
	checkconfig = line.split(",")
	showcmd = (checkconfig[0])
	verifycmd = (checkconfig[1])

resolveconfig = []
file = open("resolve-config.txt" , "r")
for line in file:
	resolveconfig.append(line)

devices = dict()
file = open("devices.csv" , "r")
for line in file:
	devices.update({line.split(",")[0]:line.split(",")[1]})

for dev_name, dev_address in devices.items():
	try:
		sw = {
		'device_type': dev_type,
		'ip':   dev_address.strip(),
		'username': usern,
		'password': password,
		'secret': secret,
		'port' : pt,
		'verbose': False
		}
		net_connect = ConnectHandler(**sw)
		net_connect.enable()
		output = net_connect.send_command('term len 0')
		output = net_connect.send_config_set(showcmd)

		if verifycmd in output:
			print(dev_name + ":\r\n" + verifycmd + " was found in configuration...")
			print("Sending resolution commands:" + "\r\n" + resolveconfig)
			output = net_connect.send_config_set(resolveconfig)
		else:
			print(dev_name + ":\r\n" + verifycmd + " was not found in configuration, no further action required")
		net_connect.disconnect()

	except:
		fi = open(os.path.join("output/FAILED DEVICES " + datetime + ".txt"), "a")
		fi.write("\r\n" + dev_name + " failed at " + formattime + "\r\nCheck ssh access to: " + dev_address + "\r\n")
		fi.close()
		print(dev_name + ":\r\nError detected, check manually...")
		continue

print("Tool finished...")
