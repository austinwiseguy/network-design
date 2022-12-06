# Austin Wise, Alan Bulavsky, Kelvin Amuma
# UDP Server

from socket import *
import random
import header

# serverIP = ""
serverIP = input("Enter IP address of server: ")
serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)                  # sets up server socket
serverSocket.bind((serverIP, serverPort))                   # assigns port number to the server's socket

# image = r"C:\Users\awwis\Desktop\image.jpeg"
image = input("Enter location and image to write data to: ")       # prompt user to enter image location
error_type = 0

# loss_pct = input("Enter loss percentage: ")
loss_pct = 5

random.seed()

print("ready to receive...")    # waiting
file = open(image, "wb")        # open new image to write
i = 0
ack = b'0'


# while connection is open
while True:
    segAndAddr = serverSocket.recvfrom(2048)
    packet_data = segAndAddr[0]
    clientAddress = segAndAddr[1]

    if packet_data == b"done":
        file.close()
        break

    else:
        seq = packet_data[:1]    # first byte of packet is sequence num

        if ack == seq:
            checksum = list(packet_data[-8:])                       # last eight bytes are checksum
            msg = packet_data[1:len(packet_data)-8]                 # bytes 2-3 are image data

            if error_type == 2:
                msg = header.data_error(msg, loss_pct)

            # print("msg = ", msg)
            server_checksum = header.check_sum(msg)
            flip = header.one_comp(server_checksum)
            add = header.add(flip, server_checksum, ack)            # adds checksum to verify

            file.write(msg)                                         # write to file
            send_packet = header.make_packet(ack, seq, checksum)    # assemble ack packet
            serverSocket.sendto(send_packet, clientAddress)

            ack = add                                               # sets ack to next packet

        else:
            serverSocket.sendto(send_packet, clientAddress)         # resend ack packet to client

serverSocket.close()                                        # close server socket
print("file written successfully")
