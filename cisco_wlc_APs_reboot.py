import getpass
import netmiko
import re


# Заполняем IP, username, port
cisco_wlc = {
    'device_type': 'cisco_wlc',
    'ip':   '192.168.1.1',
    'username': 'adminlogin',
    'password': getpass.getpass(),
    'port' : 22,          # optional, defaults to 22
    'secret': '',     # optional, defaults to ''
    'verbose': False,       # optional, defaults to False
}

net_connect = netmiko.ConnectHandler(**cisco_wlc)
output = net_connect.send_command('show ap summary')
print(output)
# Ищем точки доступа по маске, wifipoint123, wifipoint456
all_ap_lists = re.findall('wifipoint...', output)
answer = input('Input AP names to reboot them or enter \"ALL\" to reboot all points:\nExample: point1 point2 point3\n').split()
if 'all' in [_.lower() for _ in answer]:
    for ap in all_ap_lists:
        net_connect.send_config_set(['config ap reset {}'.format(ap), 'y'])
        print('ALL points will be rebooted now')
else:
    for ap in answer:
        net_connect.send_config_set(['config ap reset {}'.format(ap), 'y'])
    print(*answer, 'points will be rebooted now')
net_connect.disconnect()
