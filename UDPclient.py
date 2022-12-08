# Austin Wise, Alan Bulavsky, Kelvin Amuma
# UDP Client

from socket import *
import header
import time
import pickle
from timer import Timer

# timeout of 50ms
TIMEOUT_INT = 0.05

serverName = "10.250.1.66"  # input("Enter IP Address of server: ")  # get ip address of server from user
serverPort = 12000  # server port

clientSocket = socket(AF_INET, SOCK_DGRAM)  # underlying network uses ipv4 address, creates UDP socket

img = r"C:\Users\awise\Desktop\jpeg_image.jpeg"

# input("Enter location of image to send to server: ")  # get location and name of image
# img = r"C:\Users\awwis\Desktop\diode.bmp"

type_error = 0

count = 0
i = 0

# phase 5 variables
next_seq = 0
base = 0
window_size = 10

send_timer = Timer(TIMEOUT_INT)
# error_type = input("Enter number for program path (1 - No errors | 2 - Data Error | 3 - ACK Error): ")

packets = []

start = time.time()

try:
    packets = header.fragment_image(img, 1024)         # opens user image for reading binary
    num_packets = len(packets)                         # get number of packets in buffer

    # while the packet is not empty, the packet gets sent to the server to write to the new image
    # for i in range(num_packets):
    while base is not num_packets:
        if not packets:
            continue

        # compute checksum
        checksum = header.check_sum(packets[next_seq])

        if next_seq <= base + window_size and next_seq < num_packets:
            send_packet = header.package_data_packet(packets[next_seq], next_seq, checksum)     # make packet
            clientSocket.sendto(send_packet, (serverName, serverPort))          # send data over UDP socket
            count += 1
            # if base of window equals the previous highest seq num, start the timer
            if base == next_seq:
                send_timer.start()

            next_seq += 1

        else:
            # receive ACK packet from server
            serv_pkg, serverAddress = clientSocket.recvfrom(1024)
            serv_pkg = pickle.loads(serv_pkg)

            seq = serv_pkg.serv_seq             # get server sequence number
            ack = serv_pkg.verify               # get ack (1 or 0)

            # if ACK is 1 (not NACK), update base of the window
            if ack:
                base = seq + 1

            # if the base equals the next sequence number, stop the timer, else start the timer
            if base == next_seq:
                send_timer.stop()

            else:
                send_timer.start()

        # count += 1
        i += 1

    end = time.time()

    clientSocket.sendto(b"done", (serverName, serverPort))

# error handling
except FileNotFoundError:
    print("File not found")

clientSocket.close()                                        # close the socket

total = end - start
print("Count: ", count)
print("Total time: ", total, "s")
print("Successfully copied image to server!")               # prints completion statement
