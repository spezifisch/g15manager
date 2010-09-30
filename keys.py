import struct
import subprocess


keys_list={1:0, 2:1, 4:2, 8:3, 16:4, 32:5, 262144:"M1",
            524288:"M2", 1048576:"M3", 2097152:"MR", 8388608:"L1", 16777216:"L2",
            33554432:"L3", 67108864:"L4"}


def catch_keys(g15socket, bindings, keys_m1, keys_m2, keys_m3, m1, m2, m3 ):
    try:
        recv = g15socket.recv(1024)
        key = struct.unpack("i", recv)[0]
    except:
        return True


    if 1 <= key <= 32 and bindings.get_active():

        if m1:
            iter = keys_m1.get_iter(keys_list[key])
            command = keys_m1.get_value(iter, 1).split(" ")
        elif m2:
            iter = keys_m2.get_iter(keys_list[key])        
            command = keys_m2.get_value(iter, 1).split(" ")
        elif m3:
            iter = keys_m3.get_iter(keys_list[key])
            command = keys_m3.get_value(iter, 1).split(" ")


        try:
            subprocess.Popen(command)
        except:
            pass


    return True