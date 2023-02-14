from modules.fileManagement import readConfig, writeLog
from modules.fileUploader import uploadLogToFtpServer
from modules.emailSender import sendDoneMsg
from modules.bashFlags import getFlagObj


class bcod:
    OKGREEN   = "\033[92m"
    WARNING   = "\033[93m"
    ERRORRED  = "\033[91m"
    BOLD      = "\033[1m"
    ENDC      = "\033[0m"
    RMLINE    = "\033[F"
    MVBACK    = "\033[K"


CONN_MODULES = {
    "ssh"    : "modules.sshTester",
    "serial" : "modules.serialTester"
}


if __name__ == "__main__":
    args = getFlagObj()
    testLog = []

    try:
        cfg = readConfig(args.configPath)

        if cfg == None:
            raise Exception(f"{args.configPath} file not found.")

        if args.model not in cfg["devices"]:
            raise Exception(f"{args.model} not present in config.json file.")

        if args.conn not in CONN_MODULES:
            raise Exception(f"{args.conn} connection type not supported.")
        
        if args.conn != cfg["devices"][args.model]["settings"]["conn"]:
            raise Exception(f"Device does not support {args.conn} connection.")
        

        device = __import__(CONN_MODULES[args.conn], fromlist=[None]).Device(args.host, cfg["devices"][args.model]["settings"])


        passedTests = 0
        failedTests = 0
        totalTests  = len(cfg["devices"][args.model]["commands"])

        print(bcod.BOLD + f"Begining testing of {args.model}:" + bcod.ENDC + "\n\n")
        for itr, (i, s, o, e) in enumerate(device.TestAT(cfg["devices"][args.model]["commands"]), 1):
            testLog.append(f"{i}, {s}, {o}, {e}\n")
            
            print((bcod.RMLINE+bcod.MVBACK)*2, end="")
            if s == "PASSED":
                print(f"[{itr:>3}/{totalTests:>3}] Testing: {i:<10} Output: {o:<4} Expected: {e:<4} Status: " + bcod.OKGREEN + s + bcod.ENDC)
                passedTests += 1
            else:
                print(f"[{itr:>3}/{totalTests:>3}] Testing: {i:<10} Output: {o:<4} Expected: {e:<4} Status: " + bcod.ERRORRED + s + bcod.ENDC)
                failedTests += 1
            print(bcod.BOLD     + "Total results: " + bcod.ENDC + 
                    bcod.OKGREEN  + str(passedTests)  + bcod.ENDC + "/" +
                    bcod.ERRORRED + str(failedTests)  + bcod.ENDC)


        filePath, fileName = writeLog(args.outputPath, args.model, device.manuf, device.model, testLog)
        print("Done. Output file location:", filePath)


        if "smtpConfig" in cfg:
            if cfg["smtpConfig"]["isEnabled"]:
                print("Sent a notification to", cfg["smtpConfig"]["receiver"])
                sendDoneMsg(cfg["smtpConfig"])
            else:
                print("Notifications are disable. Notification was not sent.")
        else:
            print("Config file is missing 'smtpConfig' for notification capabilities.")
        

        if "ftpConfig" in cfg:
            if cfg["ftpConfig"]["isEnabled"]:
                print("CSV file uploaded to", cfg["ftpConfig"]["server"])
                uploadLogToFtpServer(cfg["ftpConfig"], filePath, fileName)
            else:
                print("File uploading is disabled. File was not uploaded.")
        else:
            print("Config file is missing 'ftpConfig' for file uploading capabilities.")
    except Exception as e:
        print(bcod.WARNING + bcod.BOLD + f"Error: {e}" + bcod.ENDC)
    else:
        print(bcod.BOLD + f"\nTest's completed succesfully." + bcod.ENDC)
        testLog = []
    finally:
        if testLog:
            writeLog(args.outputPath, args.model, device.manuf, device.model, testLog)
        print("Exiting...")
