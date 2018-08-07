import getpass
import paramiko
import sys
import time


tftp_server = '192.168.1.1'

with open('hardware.txt', 'r') as hardware_file:
    for line in hardware_file:
        if not line.strip() or line[0] == '#':
            continue
        hardware = line.strip('\n').split(' ')
        device, port, username, password = hardware[0], hardware[1], hardware[2], hardware[3]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('*** Connecting to {}...'.format(device))

        try:
            ssh.connect(device, port, username, password)
        except paramiko.AuthenticationException as exception:
            print('*** Connect failed:', str(exception))
            password = getpass.getpass('Please enter valid password for {} device:'.format(device))
            ssh.connect(device, port, username, password)

        with ssh.invoke_shell() as channel:
            time.sleep(5)
            channel.send('\n')
            time.sleep(2)
            channel.send('copy running-config tftp {} {}\n'.format(tftp_server, device + '_' + time.strftime("%Y%m%d-%H%M%S") + '.xml'))
            time.sleep(10)
            result = channel.recv(2000).decode('utf-8')
            print(result)
        print('All backups is done')
        ssh.close()
