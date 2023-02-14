import serial


class Device:
    def __init__(self, _host, cfg):
        self.serialShell = serial.Serial(port     = _host,
                                         baudrate = cfg["baudrate"],
                                         bytesize = cfg["bytesize"],
                                         timeout  = cfg["timeout"],
                                         stopbits = cfg["stopbits"])
        self.serialShell.write(b"systemctl stop ModemManager\r\n")

        self.manuf = self.__send("AT+GMI").split('\n')[1]
        self.model = self.__send("AT+GMM").split('\n')[1]


    def __del__(self):
        self.serialShell.close()
    

    def __send(self, cmnd):
        self.serialShell.write(cmnd.encode() + b"\r\n")
        return self.serialShell.readall().decode().strip()


    def TestAT(self, commands):
        for cmnd in commands:
            nncmnd = cmnd + "\n".join(commands[cmnd]["flags"])
            if len(commands[cmnd]["flags"]) == 2:
                nncmnd += '\u001A'
            output = self.__send(nncmnd).split('\n')[-1]
            expected = commands[cmnd]["rsp"]
            status = "PASSED" if output == expected else "FAILED"
            yield (cmnd, status, output, expected)

#sudo chmod 777 /dev/ttyUSB3