# References: Bigyan Karki, CMPUT 404 LAB 2, 17 January 2022, https://drive.google.com/file/d/1TD8UR9o-GPaudPNsY9HrePzroRBsEBFe/view
# Python docs, https://docs.python.org/3.4/library/multiprocessing.html?highlight=process

import socket
from multiprocessing import Pool

# define address & buffer size
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'


def connect(addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)
        full_data = s.recv(BUFFER_SIZE)
        print(full_data)

    except Exception as e:
        print(e)
    finally:
        s.close()


def main():
    with Pool() as pool:
        pool.map(connect, [('127.0.0.1', 8001)]*4)


if __name__ == "__main__":
    main()
