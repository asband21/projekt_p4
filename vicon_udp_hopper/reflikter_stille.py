import socket

UDP_IP = "192.168.1.34"
UDP_PORT = 51001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

UDP_IP_2 = "100.102.101.103"
UDP_PORT_2 = 51001

sock_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
tal = 1
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    sock_2.sendto(data, (UDP_IP_2, UDP_PORT_2))
    tal = tal*-1
    if tal > 0:
        print("\r ----", end='')
    else:
        print("\r ||||", end='')

