# Header file
# Austin Wise, Alan Bulavsky, Kelvin Amuma
import numpy as np
import os
import random
import pickle
import time


# combine the checksum and seqNum in one pkg
class AssembleDataPacket:
    def __init__(self, checksum, sequence, packet):
        self.cs = checksum
        self.sequence = sequence
        self.packet = packet


# combine the server ACK packet
class AssembleACKPacket:
    def __init__(self, serv_seq, verify):
        self.serv_seq = serv_seq
        self.verify = verify


# gets packet in correct orientation to send through UDP socket on client side
def package_data_packet(pkt, sequence, cs):
    packaged_packet = AssembleDataPacket(cs, sequence, pkt)
    packaged_packet = pickle.dumps(packaged_packet)
    return packaged_packet


# gets ack packet assembled in correct orientation on server side
def package_ack_packet(sequence, verify):
    packaged_packet = AssembleACKPacket(sequence, verify)
    packaged_packet = pickle.dumps(packaged_packet)
    return packaged_packet


# random error with ACK packer from server
def ack_error(data, loss):

    loss_pct = 100 - loss
    x = random.randint(0, 100)

    if x > loss_pct:
        data = flip_ack(data)
    return data


# random error with data packet from client
def data_error(msg, loss):
    loss_pct = 100 - loss
    x = random.randint(0, 100)

    print("x = ", x)

    if x > loss_pct:
        y = bytearray()
        print(msg)

        w = [j for j in msg]
        y += w

        print(y)
        return msg
    else:
        return msg


# fragment the image into smaller packets with size 1024 bytes
def fragment_image(img, packet_size):
    packets = []
    file_size = get_size(img)
    with open(img, 'rb') as file:
        total_packets = file_size // packet_size + 2
        for i in range(0, total_packets):
            packets.append(file.read(packet_size))
    return packets


# make_packet function splits file into packets of 1024 bytes to send to server
def make_packet(seq, packet_data, checksum):
    packet = bytearray()
    packet += bytearray(seq)
    packet += bytearray(packet_data)  # append bytes to the packet
    packet += bytearray(checksum)     # append checksum to packet

    return packet                     # returns packet_data, when empty this will be 0


# get_size obtains the size of the bitmap file so the server knows how much data to read
def get_size(file):
    temp = os.stat(file).st_size      # get file size and store it in temporary variable
    return temp                             # return temp as string


# binary math to add bits and checksum
def bin_math(x, y, sum_arr):
    carry = 0

    for k in range(len(sum_arr)):
        m = -1 - k
        sum_arr[m] = x[m] + y[m]
        sum_arr[m] = sum_arr[m] + carry

        match sum_arr[m]:
            case 0:
                carry = 0
            case 1:
                carry = 0
            case 2:
                sum_arr[m] = 0
                carry = 1
            case 3:
                sum_arr[m] = 1
                carry = 1

    if carry == 1:
        tmp = np.array([0, 0, 0, 0, 0, 0, 0, 1])
        bin_math(tmp, sum_arr, sum_arr)

    sum_list = sum_arr.tolist()
    return sum_list


# checksum algorithm
def check_sum(data):

    if not data:
        return

    x = [j for j in data]
    num1 = bin(x[0])[2:]
    if len(x) > 1:
        num2 = bin(x[1])[2:]
    else:
        num2 = bin(00000000)
        return

    num1 = num1.zfill(8)
    num2 = num2.zfill(8)

    arr1 = np.empty(8, dtype=int)
    arr2 = np.empty(8, dtype=int)
    sum_arr = np.empty(8, dtype=int)  # array of ints (NOT STRING ANYMORE)
    index = 7

    while index > -1:
        arr1[index] = (num1[index:(index + 1)])
        arr2[index] = (num2[index:(index + 1)])
        index -= 1

    return bin_math(arr1, arr2, sum_arr)


# flip ack or seq number bit
def flip_ack(ack):
    if ack == b'0':
        ack = b'1'

    elif ack == b'1':
        ack = b'0'

    return ack


# one's compliment
def one_comp(checksum):

    index = 0
    arr3 = np.empty(8, dtype=int)
    arr3 = arr3.tolist()

    if checksum == 0:
        return arr3

    while index < 8:
        if checksum[index] == 0:
            arr3[index] = 1
        elif checksum[index] == 1:
            arr3[index] = 0

        index += 1
    return arr3


# add checksums to verify correct bits in place
def add(flip, checksum, ack):
    index = 0
    arr4 = np.empty(8, dtype=int)

    while index < 8:
        arr4[index] = checksum[index] + flip[index]
        index += 1

    if arr4.tolist() == [1, 1, 1, 1, 1, 1, 1, 1]:
        # ack = flip_ack(ack)
        return 1
    else:
        # ack = flip_ack(ack)
        return 0
