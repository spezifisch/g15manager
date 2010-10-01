import struct
import subprocess


keys_list={1:0, 2:1, 4:2, 8:3, 16:4, 32:5, 262144:"M1",
            524288:"M2", 1048576:"M3", 2097152:"MR", 8388608:"L1", 16777216:"L2",
            33554432:"L3", 67108864:"L4"}


def catch_keys(g15socket, bindings, m1_commands, m2_commands, m3_commands, m1, m2, m3 ):

    try:
        recv = g15socket.recv(1024)
        key = struct.unpack("i", recv)[0]
    except:
        return True


    if 1 <= key <= 32 and bindings.get_active():

        def run_command(commands):
            iter = commands.get_iter(keys_list[key])
            if commands.get_value(iter, 1):
                if commands.get_value(iter, 2):
                    command = ["xte", "str " + commands.get_value(iter, 1)]
                else:
                    command = commands.get_value(iter, 1).split(" ")

            try:
                subprocess.Popen(command)
            except:
                pass


        if m1.get_active():
            run_command(m1_commands)
        elif m2.get_active():
            run_command(m2_commands)
        elif m3.get_active():
            run_command(m3_commands)

    return True



def command_edited(item, text, commands, mem, config):
    iter = commands.get_iter(int(item))
    commands.set_value(iter, 1, text)
    config.set_string("/apps/g15manager/commands/M%i/G%i" % (mem, (int(item)+1)), commands.get_value(iter, 1))



def toggle_text_input(item, commands, mem, config):
        iter = commands.get_iter(int(item))
        if commands.get_value(iter, 2):
            commands.set_value(iter, 2, False)
        else:
            commands.set_value(iter, 2, True)

        config.set_bool("/apps/g15manager/commands/M%i/G%i_text_input" % (mem,(int(item)+1)), commands.get_value(iter, 2))
