import argparse
import os

from netmiko import ConnectHandler
from FileClass import *

def check_devices():
    checkFile(config_file)
    devices = read_devices_from_file(config_file)
    output_logging = []
    for device in devices:
        try:
            if device['device_type'] == 'fortinet' or device['device_type'] == 'paloalto_panos' or device['device_type'] == 'f5_linux':
                netconnect = ConnectHandler(**device)
                output_logging.append(make_logging(f"The Device with the Ip Address {device['host']} is online!"))
        except Exception as e:
            output_logging.append(make_logging(f"The Device with the Ip Address {device['host']} is offline!"))
    write_loggging(output_logging)

def shutdown_all():
    checkFile(config_file)
    devices = read_devices_from_file(config_file)
    output_logging = []
    for device in devices:
        try:
            if device['device_type'] == 'fortinet':
                netconnect = ConnectHandler(**device)
                netconnect.send_command("execute shutdown\ny")
            elif device['device_type'] == 'paloalto_panos':
                netconnect = ConnectHandler(**device)
                netconnect.send_command("request shutdown system\ny")
            elif device['device_type'] == 'f5_linux':
                netconnect = ConnectHandler(**device)
                netconnect.send_command("tmsh modify sys db ui.system.preferences.offline_mode value enable")
        except Exception as e:
            output_logging.append(make_logging(f"The Device with the Ip Address {device['host']} has now been shudown or is already offline!"))
    write_loggging(output_logging)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("private_ssh_key_path")
    parser.add_argument("logs_path")
    parser.add_argument("--test", help="Check devices", action='store_true')
    parser.add_argument("--shutdown", help="Shutdown devices", action='store_true')
    args = parser.parse_args()
    privatekey_path = args.private_ssh_key_path
    logs_path = args.logs_path
    if not os.path.exists(logs_path):
        os.mkdir(logs_path)
    config_file = args.filename
    if args.test:
        check_devices()
    if args.shutdown:
        shutdown_all()