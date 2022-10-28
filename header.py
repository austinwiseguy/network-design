# Header file
# Austin Wise, Alan Bulavsky, Kelvin Amuma
import numpy as np
import os
import random


# will implement this last
def error_path():
    error_type = input("Enter number for program path (1 - No errors | 2 - Data Error | 3 - ACK Error): ")
    return error_type


# this will also be at the end
def random_loss(file, loss_pct):
    return


# make_packet function splits file into packets of 1024 bytes to send to server
def make_packet(seq, packet_data, checksum):
    packet = bytearray()

    packet += bytearray(seq)
    packet += bytearray(packet_data)  # append bytes to the packet
    packet += bytearray(checksum)           # append checksum to packet
    return packet                     # returns packet_data, when empty this will be 0


# get_size obtains the size of the bitmap file so the server knows how much data to read
def get_size(file):
    temp = str(os.stat(file).st_size)       # get file size and store it in temporary variable
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


# check if data gets corrupted based on user input
def is_corrupt():
    return


# flip ack or seq number bit
def flip_ack(ack):
    if ack == b'0':
        ack = b'1'

    elif ack == b'1':
        ack = b'0'

    return ack


def one_comp(checksum):
    index = 0
    x = checksum[index]
    arr3 = np.empty(8, dtype=int)
    arr3 = arr3.tolist()

    while index < 8:
        if checksum[index] == 0:
            arr3[index] = 1
        elif checksum[index] == 1:
            arr3[index] = 0

        index += 1
    return arr3


def add(flip, checksum, ack):
    index = 0
    arr4 = np.empty(8, dtype=int)

    while index < 8:
        arr4[index] = server_check_sum[index] + flip[index]
        index += 1

    if arr4.tolist() == [1, 1, 1, 1, 1, 1, 1, 1]:
        ack = flip_ack(ack)
        return ack
    else:
        ack = flip_ack(ack)
        return ack

# don't think we need this
def has_seq_num():
    return

