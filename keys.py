import struct
import subprocess


keys_list={1:0, 2:1, 4:2, 8:3, 16:4, 32:5, 262144:"M1",
            524288:"M2", 1048576:"M3", 2097152:"MR", 8388608:"L1", 16777216:"L2",
            33554432:"L3", 67108864:"L4"}


def catch_keys(g15socket,keys, toggle_bindings):
    try:
        recv = g15socket.recv(1024)
        key = struct.unpack("i", recv)[0]
    except:
        return True


    if 1 <= key <= 32 and toggle_bindings.get_active():

        iter = keys.get_iter(keys_list[key])
        
        command = keys.get_value(iter, 1).split(" ")

        try:
            subprocess.Popen(command)
        except:
            pass


    return True