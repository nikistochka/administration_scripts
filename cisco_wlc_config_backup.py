import netmiko
import re
import time


cisco_wlc = {
    'device_type': 'cisco_wlc',
    'ip': '192.168.1.1',
    'username': 'ADMINLOGIN',
    'password': 'PASSWORD',
    'port': 22,  # optional, defaults to 22
    'secret': '',  # optional, defaults to ''
    'verbose': False,  # optional, defaults to False
}

tftp_backup_server_ip = '192.168.1.2'


def config_backup_cisco_wlc(wlc_device, backup_server_ip, upload_path='./', transfer_upload_mode='tftp'):
    net_connect = netmiko.ConnectHandler(**wlc_device)
    output = net_connect.send_command('show sysinfo')
    device_name = re.findall('System Name.*?\s(.*?)\n', output)[0]
    net_connect.send_config_set([
        'transfer upload mode {}'.format(transfer_upload_mode),
        'transfer upload datatype config',
        'transfer upload serverip {}'.format(backup_server_ip),
        'transfer upload path {}'.format(upload_path),
        'transfer upload filename {}'.format(device_name + '_' + time.strftime("%Y%m%d-%H%M%S") + '.xml')
    ])
    net_connect.send_config_set(['transfer upload start', 'y'])
    net_connect.disconnect()


if __name__ == '__main__':
    config_backup_cisco_wlc(cisco_wlc, tftp_backup_server_ip)
