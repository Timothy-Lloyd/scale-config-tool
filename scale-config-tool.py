#Note that before running this script, you need to create a folder called "output" in the same directory that you intend to run this from.
#Note2 please edit the "devices.csv" file to match your devices.
#Note3 please edit the "vars.py" file and adjust your credentials etc
#Note4 please edit the "checkconfig.py" file with the show command and expected output
#Note5 please edit the "resolveconfig" file with configurations to resolve if show command output matches above
#Note6 please edit the "revertconfig" file with configurations to roll back the resolution should the configuration tests fail

from netmiko import ConnectHandler
import time
import getpass
import vars
import os
import checkconfig

red = "\033[0;31m"
green = "\033[0;32m"
white = "\033[00m"
    
pt = vars.port
dev_type = vars.devicetype

showcmd = checkconfig.show
verifycmd = checkconfig.verify
testcmd = checkconfig.test
testresult = checkconfig.testsuccess

localtime = time.localtime()
formattime = time.strftime("%d-%m-%Y %H:%M:%S" , localtime)
datetime = time.strftime("%d-%m-%Y" , localtime)

print("Starting tool...\r\n")
print("Please enter the credentials to perform the tasks required:\r\n")
print("Username: ", end="")
usern = str(input())
password = getpass.getpass()
secret = getpass.getpass(prompt='Secret: ')

print("\r\nTool is ready, please check the " + red + "configuration files" + white + " you wish to send are correct!\r\nIf you wish to continue hit enter, otherwise use a break sequence...")
input()

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
            print("Following configuration sent to device:\r\n!\r\n" + output + "\r\n!\r\nConfiguration changed as above...")
            print("...testing configuration...")
            output = net_connect.send_command(testcmd)
            if testresult in output:
                net_connect.send_command("wr")
                print("Configuration successful, please see output below:\r\n!\r\n" + green + output + white + "\r\n!\r\nDevice reconfiguration completed and config saved...\r\n\r\n")
                fi = open(os.path.join("output/Config Changed " + datetime + ".txt"), "a")
                fi.write("\r\n" + dev_name + " " + dev_address + "Time: " + formattime + "\r\nReconfigured and passed test as follows: " + output + "\r\n")
                fi.close()
            else:
                print("Configuration failed test, please see output below:\r\n!\r\n" + red + output + white + "\r\n!\r\nReverting configuration...")
                output = net_connect.send_config_from_file(config_file='revertconfig')
                print("Following configuration sent to device:\r\n!\r\n" + output + "\r\n!\r\nConfiguration changed as above...")
                print("...testing configuration...")
                output = net_connect.send_command(testcmd)
                if testresult in output:
                    print("Reverting configuration successful, please see output below:\r\n!\r\n" + green + output + white + "\r\n!\r\nManually check device!!!")
                    fi = open(os.path.join("output/TEST FAILED " + datetime + ".txt"), "a")
                    fi.write("\r\n" + dev_name + " failed at " + formattime + "\r\nTesting configuration failed but configuration was successfully reverted. Manually check the configuration on device: " + dev_address + "\r\n\r\n")
                    fi.close()
                else:
                    print("Reverting configuration failed test, please see output below:\r\n!\r\n" + red + output + white + "\r\n!\r\nManually check device!!!\r\n\r\n")
                    fi = open(os.path.join("output/TEST FAILED " + datetime + ".txt"), "a")
                    fi.write("\r\n" + dev_name + " failed at " + formattime + "\r\nTesting configuration failed and configuration revertion failed! Manually check the configuration on device: " + dev_address + "\r\n")
                    fi.close()
             
        else:
            print(green + dev_name + white + ":\r\nThe following string to change was not found in configuration:\r\n" + verifycmd + "\r\nNo further action required...\r\n\r\n")
            fi = open(os.path.join("output/Not configured " + datetime + ".txt"), "a")
            fi.write("\r\n" + dev_name + " " + dev_address + "Time: " + formattime + "\r\nDevice was not configured as peer tool.\r\n")
            fi.close()
        net_connect.disconnect()

    except:
        print(red + dev_name + ":\r\nError detected, check manually...\r\n\r\n" + white)
        fi = open(os.path.join("output/FAILED DEVICES " + datetime + ".txt"), "a")
        fi.write("\r\n" + dev_name + " failed at " + formattime + "\r\nCheck ssh access to: " + dev_address + "\r\n")
        fi.close()
    continue

print("Tool finished...")
input()
