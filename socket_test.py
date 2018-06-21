import socket
import struct
import re
import errno
import time
class MasterEtherCAT:
    def __init__(self):
        self.send_mac = "0x00 0x01 0x05 0x35 0x7f 0xe2"
        self.receive_mac = "0x01 0x01 0x05 0x01 0x00 0x00"
        self.interface = "enp0s8"
        poat = 0x88a4
        self.cat_send = socket.socket(socket.PF_PACKET, socket.SOCK_RAW) #创服务器套接字

        # struct.pack() and struct.unpack()
        # 用于C语言数据与Python数据类型间转换。
        timeval = struct.pack('ll', 0, 1)
        # s.setsockopt(level,optname,value)设置给定套接字选项的值。
        #  在send(),recv()过程中有时由于网络状况等原因，发收不能预期进行,而设置收发时限：
        # self.cat_send.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        # SO_DONTROUTE  bool 禁止选径；直接传送。
        self.cat_send.setsockopt(socket.SOL_SOCKET, socket.SO_DONTROUTE, 1)
        # 发送时限
        self.cat_send.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
        # self.cat_send.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)

        # self.cat_recv = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
        # 接收时限
        # self.cat_recv.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        # self.cat_recv.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
        # self.cat_recv.setsockopt(socket.SOL_SOCKET, socket.SO_DONTROUTE, 1)

        # 套接字与地址绑定
        self.cat_send.bind((self.interface, poat))
        # self.cat_send.listen(5)  # 监听连接,传入连接请求的最大数
        # self.cat = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
        # timeval = struct.pack('ll', 0, 1)
        # # s.setsockopt(level,optname,value)设置给定套接字选项的值。
        # self.cat.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        # self.cat.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
        # self.cat.setsockopt(socket.SOL_SOCKET, socket.SO_DONTROUTE, 1)

        # ----------------------------------------------------#
        self.cat_head = "0x88 0xa4"
        # self.cat_head[0] = 0x88
        # self.cat_head[1] = 0xA4
        # ----------------------------------------------------#

    # 根据ethercat的结构
    def socket_send(self, data_str):
        # 将报文str转为 array
        data_list = data_str.split()
        data_10_array = [0] * len(data_list)
        for num in range(len(data_list)):
            data_10_array[num] = int(data_list[num], 16)
        cat_scoket = []   #[0] * len(data_list)
        # 目的地址+源地址 各六字节
        cat_scoket.extend(data_10_array)
        self.cat_send.send(bytes(cat_scoket))
        # self.cat_send.send(cat_scoket.encode())

    def socket_recv(self, csvlinenum):
        try:
            print("recving")
            packet = self.cat_send.recv(4096)
            print("packet:", packet)
        except IOError as e:  # and here it is handeled
            if e.errno == errno.EWOULDBLOCK:
                print(csvlinenum, ": e.errno == errno.EWOULDBLOCK")
                pass
        # data = None
        # while data == None:
        #     print("recveving")
        #     packet = self.cat_recv.recv(4096)
        #     print("packet:", packet)


        # try:
        #     recv = self.cat.recv(2048)
        #     receive_data = [0] * len(recv)
        #     print("recv: ", recv)
        #     for i in range(len(recv)):
        #         if (i >= 16):
        #             # print ('[{:d}]: 0x{:02x}'.format(i-16,recv[i]))
        #             # 只保留报文部分
        #             receive_data[i - 16] = recv[i]
        #
        #     CMD = receive_data[0]  # CMD (1 byte)
        #     IDX = receive_data[1]  # IDX (1 byte)
        #     ADP = receive_data[2] | (receive_data[3] << 8)  # ADP (2 byte)
        #     ADO = receive_data[4] | (receive_data[5] << 8)  # ADO (2 byte)
        #     LEN = receive_data[6] | (receive_data[7] << 8)  # LEN (2 byte)
        #     IRQ = receive_data[8] | (receive_data[9] << 8)  # IRQ (2 byte)
        #     DATA = [0] * LEN
        #     for i in range(LEN):
        #         # print ('[{:d}]: 0x{:02x}'.format(i,receive_data[10+i]))
        #         DATA[i] = receive_data[10 + i]
        #     WKC = receive_data[9 + LEN + 1] | (receive_data[9 + LEN + 2] << 8)  # WKC (2 byte)
        #     cat_frame = [0] * 2
        #     cat_frame[0] = len(receive_data)
        #     cat_frame[1] = 0x10 | ((0x700 & len(receive_data)) >> 8)
        #     print("CMD= 0x{:02x}".format(CMD))
        #     print("IDX= 0x{:02x}".format(IDX))
        #     print("ADP= 0x{:04x}".format(ADP))
        #     print("ADO= 0x{:04x}".format(ADO))
        #     print("LEN= 0x{:04x}".format(LEN))
        #     print("IRQ= 0x{:04x}".format(IRQ))
        #     for i in range(LEN):
        #         print('DATA[%d]: 0x{:02X}'.format(DATA[i]) % (i))
        #     print("WKC= 0x{:04x}".format(WKC))
        #
        #
        # except IOError as e:  # and here it is handeled
        #     if e.errno == errno.EWOULDBLOCK:
        #         print(csvlinenum, ": e.errno == errno.EWOULDBLOCK")
        #         pass

    # Close sockets
    def close(self):
        self.cat_recv.close()
        self.cat_send.close()
        return

if __name__ == '__main__':

    ether = MasterEtherCAT()

    # 原版的16进制数据
    name_str = "true_16_data"
    # name_str = "true_16_data_010105_to_02017fe2_171577len"
    # name_str = "true_16_data_00017fe2_to_010105_171578len"
    filename = "data/" + name_str + ".csv"

    csvlinenum = 0
    with open(filename, 'r') as csvfile:
        for line in csvfile:
            if line == "" and len(line) == 0:
                raise ValueError("line is untrue: %d", line)
            csvlinenum += 1
            # print(csvlinenum,": ", line)
            ether.socket_send(line)
            time.sleep(2)
            ether.socket_recv(csvlinenum)

    ether.close()