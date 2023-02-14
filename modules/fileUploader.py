import paramiko


def uploadLogToFtpServer(cfg, filePath, fileName):
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(cfg["server"], cfg["port"], cfg["user"], cfg["pass"])

        with ssh.open_sftp() as sftp:
            try:
                sftp.mkdir(cfg["dest"])
            except IOError:
                pass
            finally:
                sftp.chdir(cfg["dest"])

            sftp.put(filePath, fileName)