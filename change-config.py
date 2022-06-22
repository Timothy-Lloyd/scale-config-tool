#Note that before running this script, you need to create a folder called "output" in the same directory that you intend to run this from.
#Note2 please edit the "devices.csv" file to match your devices.
#Note3 please edit the "vars.py" file and adjust your credentials etc
#Note4 please edit the "checkconfig.py" file with the show command and expected output
#Note5 please edit the "resolveconfig" file with configurations to resolve if show command output matches above

from netmiko import ConnectHandler
import time
import vars
import os
import checkconfig

red = "\033[0;31m"
green = "\033[0;32m"
white = "\033[00m"
    
usern = vars.username
password = vars.password
secret = vars.secret
pt = vars.port
dev_type = vars.devicetype
showcmd = checkconfig.show
verifycmd = checkconfig.verify

localtime = time.localtime()
formattime = time.strftime("%d-%m-%Y %H:%M:%S" , localtime)
datetime = time.strftime("%d-%m-%Y" , localtime)

print("Starting tool...\r\n")

devices = dict()
file = open("devices.csv" , "r")
for line in file:
    devices.update({line.split(",")[0]:line.split(",")[1]})

for dev_name, dev_address in devices.items():
    try:
        sw = {
            'device_type': dev_type,
            'ip': dev_address.strip(),
            'username': usern,
            'password': password,
            'secret': secret,
            'port' : pt,
            'verbose': False
        }
        net_connect = ConnectHandler(**sw)
        net_connect.enable()
        output = net_connect.send_command('term len 0')
        output = net_connect.send_command(showcmd)

        if verifycmd in output:
            print(red + dev_name + white + ":\r\nThe following string to change" + red + " WAS FOUND" + white + " in configuration:\r\n" + verifycmd + "\r\nResolving...")
            output = net_connect.send_config_from_file(config_file='resolveconfig')
            print("Following configuration sent to device:\r\n" + output + "\r\nConfiguration changed as above...\r\n")
        else:
            print(green + dev_name + white + ":\r\nThe following string to change was not found in configuration:\r\n" + verifycmd + "\r\nNo further action required...\r\n")
        net_connect.disconnect()

    except:
        print(dev_name + ":\r\nError detected, check manually...")
        fi = open(os.path.join("output/FAILED DEVICES " + datetime + ".txt"), "a")
        fi.write("\r\n" + dev_name + " failed at " + formattime + "\r\nCheck ssh access to: " + dev_address + "\r\n")
        fi.close()
    continue

print("Tool finished...")
input()
