import datetime
from ShutdownScript import *

def read_devices_from_file(filename):
    devices_list = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    os = None
    host = None
    username = None
    password = None
    for line in lines:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            if os is not None:
                devices_list.append({'device_type': os, 'host': host, 'username': username, 'use_keys':True,'key_file':privatekey_path})
            os = line[1:-1]
            host = None
            username = None
            password = None
        else:
            key, value = line.split("=")
            if key == "host":
                host = value
            elif key == "username":
                username = value
            elif key == "password":
                password = value
    if os is not None:
        devices_list.append({'device_type': os, 'host': host, 'username': username, 'use_keys':True,'key_file':privatekey_path})
    return devices_list

class FileError(Exception):
    def __init__(self, messsage):
        self.message = messsage
        super().__init__(self.message)

def checkFile(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        non_empty_lines = [line for line in lines if line.strip()]
        with open(file_path, 'w') as file:
            file.writelines(non_empty_lines)

def make_logging(log_string):
        current_datetime = datetime.datetime.now()
        return f"[{current_datetime}] {log_string}\n"

def write_loggging(logging_list):
    current_datetime = datetime.datetime.now()
    with open(f"logs/{current_datetime.day}-{current_datetime.month}-{current_datetime.year} {current_datetime.hour}-{current_datetime.minute}-{current_datetime.second}.log","w") as log_file:
        for logs in logging_list:
            log_file.write(logs)

def addDevice():
    while True:
        os=input("Enter the os from the new device (fortinet,paloalto_panos):")
        if os.lower() == "fortinet" or os.lower() == "paloalto_panos":
            break
    host=input("Enter the Ip address:")
    username=input("Enter the username:")
    with open("config.conf","a") as config_file:
        config_file.write(f"\n[{os}]")
        config_file.write("\n"+host)
        config_file.write("\n"+username)