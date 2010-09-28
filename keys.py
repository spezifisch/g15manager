import struct
import subprocess


keys=[("G1", 1), ("G2", 2), ("G3", 4), ("G4", 8), ("G5", 16), ("G6", 32),
        ("M1", 262144), ("M2", 524288), ("M3", 1048576), ("MR", 2097152),
        ("L1", 8388608), ("L2", 16777216), ("L3", 33554432), ("L4", 67108864)]

def catch_keys(g15socket,commands):
    try:
        recv = g15socket.recv(1024)
        key = struct.unpack("i", recv)[0]
    except:
        return True


    if 1 <= key <= 32:
        print key
        for i in range(6):
            if key == keys[i][1]:
                command = commands[i].get_text().split(" ")
                command_list = []
                for arg in command:
                    command_list.append(arg)

                try:
                    subprocess.Popen(command_list)
                except:
                    pass


    return True