# ############################################     PARAMETERS    #######################################################
# Fill in variables below. Username, password, and enable password.
# Use text file switches.txt and paste in ip addresses of the devices. One per line.
# Alternatively, comment out lines 13-15 and uncomment line 16 instead, if number of devices is relatively small.
# Use command_file variable for config lines. Line 17.
# Alternatively, comment out line 17 and uncomment lines 18-20 to specify configs.txt file with lots of configurations.
# One config line per text line inside configs.txt file.
# By default, only cisco platform is supported.
# ######################################################################################################################
user = 'cisco'
password = 'cisco'
enable_password = 'cisco'
# ######################################################################################################################
switchhosts = 'switches.txt'
with open(switchhosts) as f:
    switchhosts = f.read().splitlines()
# switchhosts = ['192.168.56.40', '192.168.56.48']
command_file = ['vlan 400', 'name VOICE2', 'vlan 444', 'name DMZ1']
# command_file = 'configs.txt'
# with open(command_file) as g:
#     command_file = g.read().splitlines()
# ######################################################################################################################
platform = 'cisco_ios'
errors = []


def netmiko_write_commands(usr, passw, en_passw, swh, plat, comm):
    from netmiko import ConnectHandler
    incr = 0
    for host in swh:
        print("ESTABLISHING SSH SESSION TO SWITCH " + str(host))
        try:
            net_connect = ConnectHandler(device_type=plat,
                                         ip=host,
                                         username=usr,
                                         password=passw,
                                         secret=en_passw
                                         )
            net_connect.enable()
            output = net_connect.send_config_set(comm)
            print(output)
            output = net_connect.send_command('write memory')
            print(output)
            print("Switch " + str(host) + " is COMPLETE")
            incr = incr + 1
        except:
            print(host)
            errors.append(host)


def tellib_write_commands(usr, passw, en_passw, swh, comm):
    import telnetlib
    incr = 0
    for host in swh:
        try:
            tn = telnetlib.Telnet(host)
            tn.read_until(b"Username: ")
            tn.write(usr.encode('ascii') + b"\n")
            if password:
                tn.read_until(b"Password: ")
                tn.write(passw.encode('ascii') + b"\n")
                tn.write(b"enable\n")
                tn.write(en_passw.encode('ascii') + b"\n")
                tn.write(b"terminal length 0\n")
                tn.write(b"conf t\n")
                print("Applying configs to " + host)
                for x in comm:
                    x = x.strip()
                    print(x)
                    output = tn.write(x.encode('ascii') + b"\n")
            tn.write(b"end\n")
            print("Writing Memory")
            tn.write(b"terminal no length\n")
            tn.write(b"wr mem\n")
            tn.write(b"exit\n")
            incr = incr + 1
            print(tn.read_all().decode('ascii'))
        except:
            errors.append(host)


netmiko_write_commands(user, password, enable_password, switchhosts, platform, command_file)
# tellib_write_commands(user, password, enable_password, switchhosts, command_file)

for e in errors:
    print("##############################################")
    print("ERRORS WERE FOUND ON THIS HOST: " + e)
