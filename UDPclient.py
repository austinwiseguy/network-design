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
img = r"C:\Users\awise\Desktop\jpeg_image.jpeg"

# type_error = header.error_path()
type_error = 0
msg = 1
i = 0

try:
    transfer_file = open(img, 'rb')         # opens user image for reading binary
    msg = transfer_file.read(2)

    # while the packet is not empty, the packet gets sent to the server to write to the new image
    while msg:
        checksum = header.check_sum(msg)
        send_packet = header.make_packet(msg, checksum)
        # sndpkt = header.make_packet(ack, packet, checksum)
        i += 1
        clientSocket.sendto(send_packet, (serverName, serverPort))  # send data over UDP socket
        msg = transfer_file.read(2)

        # now wait for ACK from server
        # while clientSocket.recv(2048) != 'ack':
        #     print("waiting...")

        # print("Sending next packet!")

# error handling
except FileNotFoundError:
    print("File not found")

finally:
    transfer_file.close()


return_msg, serverAddress = clientSocket.recvfrom(2048)     # receives confirmation message from server
clientSocket.close()                                        # close the socket

# bmp_size = int(int(bmp_size) / 1024)                        # calculation to convert size of file to kb

print("File of size " + str(bmp_size) + "kb written to new image")    # prints completion statement


