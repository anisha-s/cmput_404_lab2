# References: Bigyan Karki, CMPUT 404 LAB 2, 17 January 2022, https://drive.google.com/file/d/1TD8UR9o-GPaudPNsY9HrePzroRBsEBFe/view
# Python docs, https://docs.python.org/3.4/library/multiprocessing.html?highlight=process

#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

# define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        # QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # bind socket to address
        s.bind((HOST, PORT))
        # set to listening mode
        s.listen(2)
        
        # continuously listen for connections
        while True:
            conn, addr = s.accept()

            p = Process(target=handle_echo, args=(conn, addr))
            p.daemon = True
            p.start()
            print("started process ", p)


def handle_echo(conn, addr):
    print("Connected by", addr)

    # recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    conn.sendall(full_data)
    conn.close()


if __name__ == "__main__":
    main()
