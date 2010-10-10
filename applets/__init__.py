import os

applets = []


for file in os.listdir("./applets"):
    if file.split(".")[1] == "py":
        applet = file.split(".")[0]

        if applet != "__init__":
            module = __import__(applet, globals(), locals(), [], -1)
            applets.append([module.name, module, 0])


applets.sort()
