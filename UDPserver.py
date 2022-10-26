# Austin Wise, Alan Bulavsky, Kelvin Amuma
# UDP Server

from socket import *
import random
import header

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)                  # sets up server socket
serverSocket.bind(('', serverPort))                         # assigns port number to the server's socket

# image = input("Enter location and image to write data to: ")             # prompt user to enter image location
image = r"C:\Users\awise\Desktop\image.jpeg"
random.seed()

print("ready to receive...")    # waiting
file = open(image, "wb")        # open new image to write
i = 0


# while connection is open
while True:
    segAndAddr = serverSocket.recvfrom(10)
    packet_data = segAndAddr[0]
    clientAddress = segAndAddr[1]

    if packet_data:
        while packet_data:
            checksum = list(packet_data[-8:])               # eventually use to compute checksum
            msg = packet_data[:2]
            print(packet_data)

            file.write(msg)                                 # write to file
            packet_data = serverSocket.recv(10)
            print(i)
            i += 1
    else:
        break

    break

serverSocket.sendto(str(i).encode(), clientAddress)

serverSocket.close()                                        # close server socket
print("file written successfully")








