import getpass
import paramiko
import time
import re
import os
from ftplib import FTP


ironport = '192.168.1.1' # Cisco IronPort IP or FQDN 
ironport_username = 'admin'
ironport_password = getpass.getpass('Enter \"{}\" password for Cisco IronPort {}:'.format(ironport_username, ironport))
backupserver = '192.168.1.2'
backup_path = '\\backup\\'


try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ironport, username=ironport_username, password=ironport_password,
                   look_for_keys=False, allow_agent=False)
    with ssh.invoke_shell() as ssh:
        time.sleep(5)
        ssh.send('saveconfig\n')
        time.sleep(2)
        ssh.send('2\n') # Options:
                        # 1. Mask passphrases
                        # 2. Encrypt passphrases
                        # 3. Plain passphrases
        time.sleep(5)
        result = ssh.recv(2000).decode('utf-8')
        backup_filename = re.findall('configuration/(.*?\.xml)', result)[0]
    ssh.close()
    
except Exception as e:
    print("*** Caught exception: {}: {}".format(e.__class__, e))
    traceback.print_exc()
    try:
        ssh.close()
    except:
        pass
    sys.exit(1)

if not os.path.exists('\\\\' + backupserver + backup_path):
    os.makedirs('\\\\' + backupserver + backup_path)

with FTP(ironport, ironport_username, ironport_password) as ftp:
    ftp.cwd('configuration')
    with open('\\\\' + backupserver + backup_path + backup_filename, 'wb') as local_file:
        ftp.retrbinary('RETR ' + backup_filename, local_file.write)
        ftp.delete(backup_filename)
        print('Backup Complete')



