# Austin Wise, Alan Bulavsky, Kelvin Amuma
# UDP Server

from socket import *
import random
import header

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)                  # sets up server socket
serverSocket.bind(('', serverPort))                         # assigns port number to the server's socket

# image = input("Enter location and image to write data to: ")             # prompt user to enter image location
image = r"C:\Users\awise\Desktop\image.bmp"
random.seed()

print("ready to receive...")    # waiting
file = open(image, "wb")        # open new image to write
i = 0
ack = b'0'


# while connection is open
while True:
    segAndAddr = serverSocket.recvfrom(12)
    packet_data = segAndAddr[0]
    clientAddress = segAndAddr[1]

    if packet_data:
        while packet_data:
            seq = packet_data[:1]                                       # first byte of packet is sequence num
            if ack == seq:
                checksum = list(packet_data[-8:])                       # last eight bytes are checksum
                msg = packet_data[0:4]                                  # bytes 2-3 are image data
                server_checksum = header.check_sum(msg)
                flip = header.one_comp(server_checksum)
                add = header.add(flip, server_checksum, ack)            # adds checksum to verify, flips ack if correct
                # will compute checksum here
                # --------------------------
                # read 2 bytes of image data
                file.write(msg)                                         # write to file
                send_packet = header.make_packet(ack, seq, checksum)    # assemble ack packet
                serverSocket.sendto(send_packet, clientAddress)         # send ack to client
            else:
                serverSocket.sendto(send_packet, clientAddress)         # resend ack to client

            packet_data = serverSocket.recv(12)                         # receive next packet from client
            i += 1
    else:
        break

    break

# serverSocket.sendto(str(i).encode(), clientAddress)         # arbitrary

serverSocket.close()                                        # close server socket
print("file written successfully")

















