# Scale-Config-Tool
Scale-Config-Tool is a lightweight tool which will allow rapid configuration changes across a wide range of networking devices. In this example the tool is used to adjust the TACACS authentication server used to authenticate access to the switch management console. It can however be used for other purposes.  

**To do list:**
1. Integrate with Nornir for multi-threading  
2. Create functions to tidy up busy code  

## Requirements:
python3  
python3-netmiko  

## Prerequisites:
Create folder in the scale-config-tool folder called "output" - this is where the tools store output.  

## Description:
Further to the overview above, the tool follows this logic flow:  
1. Load device from "devices.csv"  
2. SSH to device, send a show command defined as "show" within "checkconfig.py". In this example, we're trying to see if the device has the old authentication server and therefore needs to be updated with the new IP  
3. Check if the output from the show command matches a string defined as "verify" within "checkconfig.py". In our example, the string is set as part of a configuration line associated with the old authentication server   
    1. If the output does not match, it is assumed that the configuration does not need to be changed as the device does not have the configuration of the old authentication server  
    2. If the output matches the verification command, it is assumed that the configuration needs to be updated. The configuration within the "resolveconfig" file is sent to the device, this configuration is designed to both add the new authentication server and remove the old server in our example. The configuration is then tested using the "test" and "testsuccess" criteria within the "checkconfig.py" file. It is expected that the "testsuccess" field should be found within the "test" command output. Please see below for the pass or fail scenarios:  
        1. If the device passes the test the system configuration is saved and the tool moves onto the next device  
        2. If the device fails the test, it is assumed that the configuration failed and needs to be rolled back. The configuration within the "revertconfig" file is sent to the device, this configuration is designed to both re-add the old authentication server and remove the new server in our example. The configuration is then tested using the "test" and "testsuccess" criteria within the "checkconfig.py" file. It is expected that the "testsuccess" field should be found within the "test" command output. Either a pass or fail will be logged for the administrator to manually check the device.  
4. Should there be any errors the tool will continue to the next device after logging the device with the error within a file location in the folder "./output"  

## How To Use:
1. First, add folder "output" to ./  
2. Add devices to file "devices.csv"  
3. Add any details to update to file "vars.py"  
4. Add show and verify commands to file "checkconfig.py"  
5. Add resolution commands should the above commands match to file "resolveconfig"  
6. Add rollback commands that can revert the configuration changes made in the previous step should configuration testing fail to file "revertconfig"  
7. Run the tool "scale-config-tool.py" and observe output  
8. Manually check the devices recorded in a file within the output folder  
