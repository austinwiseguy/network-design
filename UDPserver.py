# Austin Wise, Alan Bulavsky, Kelvin Amuma
# UDP Server

from socket import *
import random
import header
import pickle

serverIP = "192.168.1.163"
serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)                  # sets up server socket
serverSocket.bind((serverIP, serverPort))                         # assigns port number to the server's socket

image = r"C:\Users\awwis\Desktop\image.jpeg"
# input("Enter location and image to write data to: ")  # prompt user to enter image location
random.seed()

print("ready to receive...")    # waiting
file = open(image, "wb")        # open new image to write
i = 0
ack = 0


# while connection is open
while True:
    # receive data from client
    segAndAddr = serverSocket.recvfrom(2048)
    packet_data, clientAddress = segAndAddr

    # if there is no data left to transmit, close the file
    if packet_data == b"done":
        file.close()
        break

    else:
        i += 1

        packet_data = pickle.loads(packet_data)     # load class data into bytes

        seq = packet_data.sequence    # first byte of packet is sequence num

        if ack == seq:
            checksum = packet_data.cs  # get checksum
            msg = packet_data.packet      # img data

            server_checksum = header.check_sum(msg)
            flip = header.one_comp(server_checksum)
            verify = header.add(flip, server_checksum, ack)            # adds checksum to verify (returns 1 if good)

            file.write(msg)                                         # write to file
            print(i)
            send_packet = header.package_ack_packet(ack, verify)    # assemble ack packet
            # send_packet = pickle.dumps(send_packet)

            # ack = add
            ack += 1                                                # sets ack to next packet

            serverSocket.sendto(send_packet, clientAddress)         # send to client

        else:
            print("ERROR")
            # serverSocket.sendto(send_packet, clientAddress)         # resend ack packet to client

serverSocket.close()                                        # close server socket
print("Image written successfully!")
