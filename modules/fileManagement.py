import os
import json
import ftplib
from datetime import datetime


def readConfig(fileName):
    if os.path.exists(fileName):
        with open(fileName, "r") as fRead:
            return json.load(fRead)
    else:
        return None


def getCurDate(format="%y%m%d%H%M"):
    return datetime.now().strftime(format)


def writeLog(path, deviceName, manuf, model, log):
    if path == "":
        path = os.path.join(os.path.abspath(''), "output")

    if not os.path.exists(path):
        os.makedirs(path)

    fileName = f"{deviceName}-{getCurDate()}.csv"
    filePath = os.path.join(path, fileName)

    with open(filePath, "w") as f:
        f.write("Modem information\n")
        f.write(f"Manafacturer, {manuf}\n")
        f.write(f"Model, {model}\n\n")
        f.write(f"Command, Status, Response, Expected \n")
        f.writelines(log)
    
    return (filePath, fileName)