# Austin Wise, Alan Bulavsky, Kelvin Amuma
# UDP Client

from socket import *
import os   # used for reading size of file
import numpy as np
import header

# serverName = input("Enter IP Address of server: ")  # get ip address of server from user
serverName = "10.250.1.66"
serverPort = 12000  # server port

clientSocket = socket(AF_INET, SOCK_DGRAM)  # underlying network uses ipv4 address, creates UDP socket

# img = input("Enter location of image to send to server: ")  # get location and name of image
img = r"C:\Users\awise\Desktop\diode.bmp"

# type_error = header.error_path()
type_error = 0
msg = 1
x = 1
i = 0
seq = b'0'


try:
    transfer_file = open(img, 'rb')         # opens user image for reading binary
    msg = transfer_file.read(2)

    # while the packet is not empty, the packet gets sent to the server to write to the new image
    while msg:
        checksum = header.check_sum(msg)                                # compute checksum

        send_packet = header.make_packet(seq, msg, checksum)            # make packet
        clientSocket.sendto(send_packet, (serverName, serverPort))      # send data over UDP socket

        # now wait for ACK from server
        x = clientSocket.recv(12)
        ack = x[:1]

        # if seq and ack are not equal, resend packet over UDP socket
        if seq != ack:
            clientSocket.sendto(send_packet, (serverName, serverPort))
        else:
            seq = header.flip_ack(seq)                                  # flip seq number bit to reflect next packet

        i += 1

        # read next bytes from image
        msg = transfer_file.read(2)

# error handling
except FileNotFoundError:
    print("File not found")

finally:
    transfer_file.close()


return_msg, serverAddress = clientSocket.recvfrom(2048)     # receives confirmation message from server
clientSocket.close()                                        # close the socket

print("Successfully copied image to server!")               # prints completion statement


