# Austin Wise, Alan Bulavsky, Kelvin Amuma
# UDP Client

from socket import *
import numpy as np
import header
import time
import timeit
import datetime

# serverName = ""
serverName = input("Enter IP Address of client: ")      # get ip address of server from user
serverPort = 12000  # server port

clientSocket = socket(AF_INET, SOCK_DGRAM)  # underlying network uses ipv4 address, creates UDP socket

# img = r"C:\Users\awwis\Desktop\new_jpeg_image.jpeg"
img = input("Enter location of image to send to server: ")  # get location and name of image

msg = 1
x = 0
seq = b'0'
timeout = 40 * 10**3
end = 0
flag = 0

# error_type = input("Enter number for program path (1 - No errors | 2 - ACK bit-error | 3 - DATA bit-error) |
# 4 - ACK packet loss | 5 - DATA packet loss: ")
error_type = 0
# loss_pct = input("Enter loss pct: ")
loss_pct = 0

packets = []

start = datetime.datetime.now()                         # track execution time

try:
    packets = header.fragment_image(img, 1024)         # opens user image for reading binary
    size = header.get_size(img) // 1024

    # while the packet is not empty, the packet gets sent to the server to write to the new image
    for i in range(len(packets)):
        msg = packets[i]
        if not msg:
            continue

        checksum = header.check_sum(msg)                                # compute checksum

        send_packet = header.make_packet(seq, msg, checksum)            # make packet
        clientSocket.sendto(send_packet, (serverName, serverPort))      # send data over UDP socket

        start_timer = time.perf_counter_ns() / 10**7

        # now wait for ACK from server
        x = clientSocket.recv(1024)

        stop = time.perf_counter_ns() / 10**7

        if float(stop - start_timer) > 40:
            the_timeout = stop - start_timer
            clientSocket.sendto(send_packet, (serverName, serverPort))
            x = clientSocket.recv(1024)
            ack = x[:1]
            print("TIMEOUT")

        else:
            ack = x[:1]

            if error_type == 2:
                ack = header.ack_error(ack, loss_pct)

            # if seq and ack are not equal, resend packet over UDP socket
            if seq != ack:
                print("ACK doesn't match, resending packet")

                clientSocket.sendto(send_packet, (serverName, serverPort))
                x = clientSocket.recv(1024)
                ack = x[:1]
            else:
                seq = header.flip_ack(seq)                                  # flip seq number bit to reflect next packet
                flag = 1
                x = 0
                continue

    clientSocket.sendto(b"done", (serverName, serverPort))

# error handling
except FileNotFoundError:
    print("File not found")

clientSocket.close()                                            # close the socket

end = datetime.datetime.now()
exec_time = (end - start).total_seconds()

# print("Successfully copied image to server!")                 # prints completion statement
print("Execution time: ", float(exec_time * 10**3), "ms")              # prints completion time
