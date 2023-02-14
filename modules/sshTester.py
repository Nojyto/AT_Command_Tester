import paramiko
import select
import time


class Device:
    REQ_TIMEOUT = 1
    
    def __init__(self, _host, cfg):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname = _host,
                         port     = cfg["port"],
                         username = cfg["user"],
                         password = cfg["pasw"])
        self.ssh.exec_command("service gsmd stop")
        self.stdin, self.stdout, self.stderr = self.ssh.exec_command("socat /dev/tty,raw,echo=0,escape=0x03 /dev/ttyUSB3,raw,setsid,sane,echo=0,nonblock ; stty sane\r", get_pty=True)

        self.manuf = self.__send("AT+GMI").split('\n')[0]
        self.model = self.__send("AT+GMM").split('\n')[0]

    def __del__(self):
        #self.stdin.channel.send('\x03')
        #self.stdout.channel.close()
        self.ssh.close()

    
    def __send(self, cmnd):
        s = time.time()
        self.stdin.channel.send(cmnd + '\n')
        while not self.stdout.channel.exit_status_ready():
            time.sleep(0.5)

            if time.time() - s > self.REQ_TIMEOUT:
                return "FAILED"

            if self.stdout.channel.recv_ready():
                rl, wl, xl = select.select([self.stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    return self.stdout.channel.recv(4096).decode().strip()


    def TestAT(self, commands):
        for cmnd in commands:
            # try:
            #     transport = self.ssh.get_transport()
            #     transport.send_ignore()
            # except EOFError as e:
            #     print(e)

            nncmnd = cmnd + "\n".join(commands[cmnd]["flags"])
            if len(commands[cmnd]["flags"]) == 2:
                nncmnd += '\u001A'
            output = self.__send(nncmnd).split('\n')[-1]
            expected = commands[cmnd]["rsp"]
            status = "PASSED" if output == expected else "FAILED"
            yield (cmnd, status, output, expected)
