# References: Bigyan Karki, CMPUT 404 LAB 2, 17 January 2022, https://drive.google.com/file/d/1TD8UR9o-GPaudPNsY9HrePzroRBsEBFe/view
# Python docs, https://docs.python.org/3.4/library/multiprocessing.html?highlight=process

import socket, time, sys
from multiprocessing import Process

# define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


def get_remote_ip(host):
    print(f'Getting IP for host:')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f'Host name not resolved. Exiting')
        sys.exit()

    print("IP of " + host + " is " + remote_ip)
    return remote_ip


def main():
    host = "www.google.com"
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server')
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind socket to address
        proxy_start.bind((HOST, PORT))
        # set to listening mode
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print('connected by ', addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print('Connecting to Google')
                r_ip = get_remote_ip(host)
                proxy_end.connect((r_ip, port))
                p = Process(target=handle_echo, args=(conn, addr, proxy_end))
                p.daemon = True
                p.start()
                print("started process ", p)

            conn.close()


def handle_echo(conn, addr, proxy_end):
    print("Connected by", addr)
    send_full_data = conn.recv(BUFFER_SIZE)
    print('sending received data ', send_full_data, ' to Google')
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)

    data = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending received data {data} to client')
    conn.send(data)


if __name__ == "__main__":
    main()


