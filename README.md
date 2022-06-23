# Scale-Config-Tool
Scale-Config-Tool is a lightweight tool which will allow rapid configuration changes across a wide range of networking devices. In this example the tool is used to adjust the TACACS authentication server used to authenticate access to the switch management console. It can however be used for other purposes.  

## Requirements:
python3  
python3-netmiko  

## Prerequisites:
Create folder in the scale-config-tool folder called "output" - this is where the tools store output.  

## Description:
Further to the overview above, the tool follows this logic flow:  
- Load device from "devices.csv"  
- SSH to device, send a show command defined as "show" within "checkconfig.py". In this example, we're trying to see if the device has the old authentication server and therefore needs to be updated with the new IP  
- Check if the output from the show command matches a string defined as "verify" within "checkconfig.py". In our example, the string is set as part of a configuration line associated with the old authentication server   
  - If the output does not match, it is assumed that the configuration does not need to be changed as the device does not have the configuration of the old authentication server  
  - If the output matches the verification command, it is assumed that the configuration needs to be updated  
    - The configuration within the "resolveconfig" file is sent to the device, this configuration is designed to both add the new authentication server and remove the old server  
- Should there be any errors the tool will continue to the next device after logging the device with the error within a file location in the folder "./output"  

## How To Use:
- First, add folder "output" to ./  
- Add devices to file "devices.csv"  
- Add credentials to file "vars.py"  
- Add show and verify commands to file "checkconfig.py"  
- Add resolution commands should the above commands match to file "resolveconfig"  
- Run the tool "change-config.py" and observe output  
- Manually check the devices recorded in a file within the output folder  
