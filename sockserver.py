import socket
import sys


def banner():
    print('███████  █████  ███    ██  ██████ ██████  ')
    print('██      ██   ██ ████   ██ ██           ██ ')
    print('███████ ███████ ██ ██  ██ ██       █████  ')
    print('     ██ ██   ██ ██  ██ ██ ██      ██      ')
    print('███████ ██   ██ ██   ████  ██████ ███████  by Sanchious')


def inbound_message(remote_target):
    print(f'[+] Awaiting response...')
    response = remote_target.recv(1024).decode()
    return response


def outbound_message(remote_target, message):
    remote_target.send(message.encode())


def listener_handler():
    sock.bind((host_ip, host_port))
    print('[+] Awaiting connection from clinet...')
    sock.listen()
    remote_target, remote_ip = sock.accept()
    message_handler(remote_target, remote_ip)


def message_handler(remote_target, remote_ip):
    print(f'[+] Connection received from {remote_ip[0]}, {remote_ip[1]}')
    while True:
        try:
            message = input('Message to send#> ')
            if message == 'exit':
                remote_target.send(message.encode())
                remote_target.close()
                print('[-] Closing the connection...')
                break
            elif not message:
                continue
            outbound_message(remote_target, message)
            print(inbound_message(remote_target))
        except KeyboardInterrupt:
            remote_target.close()
            print('[+] Keyboard interrupt issued')
            break
        except Exception:
            remote_target.close()
            break


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    banner()
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
        listener_handler()
    except IndexError:
        print('[-] Argument(s) missing.')
    except Exception as e:
        print(e)
