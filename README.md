# cisco-cli-apply-config

Summary:

Purpose of this script is to apply certain bulk configurations to multiple pieces of equipment. For example: configure
new vlan on multiple switches, update SNMP community string on all pieces of equipment, update password across all
network devices. Supports both SSH and Telnet. Only SSH is enabled by default. Always writes memory after applying. 
This was tested primarily in virtual Cisco environment and might have different effect on specific physical Cisco models.


Requirements:

1) Interpreter: Python 3.8.0+
2) Python Packages: telnetlib, netmiko, paramiko, re

How to run:

1) Open apply_config.py file with a text editor of your choice. Replace example configurations in the PARAMETERS
   section. Lines 11-13. By default, ip addresses must be added to switches.txt file, one per line in the same directory
   with the script.
   

2) By default, script will use SSH to establish connection. Telnet is supported.
    1) To disable SSH, comment out Line 148.
    2) To enable Telnet, uncomment Line 149.
   

3) Run python3 apply_config.py in the terminal.