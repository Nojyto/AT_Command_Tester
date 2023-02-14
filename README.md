# AT command tester

## Additional Dependencies

### [Program CLI](main.py)
- json
- datetime
- argparse

### [Serial tester module](modules/serialTester.py)
- serial

### [SSH tester module](modules/sshTester.py)
- paramiko
- select

Full list in [requirements.txt](requirements.txt).


## Configuration file example
Configuration file is in json format. Example bellow is a truncated version of [config](config.json) file. Default file path is {executing dir}/output.
```json
{
    "smtpConfig": {
        "isEnabled": false,
        "server": "smtp.gmail.com",
        "port": 465,
        "sender": "<...>",
        "pass": "<...>",
        "subject": "AT command tester",
        "message": "Script has finished running.",
        "receiver": "<...>"
    },
    "ftpConfig": {
        "isEnabled": false,
        "server": "<...>",
        "port": 22,
        "user": "<...>",
        "pass": "<...>",
        "dest": "../practicalTest"
    },
    "RUTX11": {
        "settings" :{
            "conn": "ssh",
            "port": 22,
            "user": "root",
            "pasw": "Admin123"
        },
        "commands": {
            "ATI": {
                "flags":"",
                "rsp": "OK"
            },
            "AT+GMI": {
                "flags":"",
                "rsp": "OK"
            },
            "AT+GMM": {
                "flags":"",
                "rsp": "OK"
            },
            "AT+GMR": {
                "flags":"",
                "rsp": "OK"
            }
        }
    },
    "TRM240": {
        "settings": {
            "conn": "serial",
            "baudrate": 115200,
            "bytesize": 8,
            "timeout": 2,
            "stopbits": 1
        },
        "commands": {
            "ATI": {
                "flags":"",
                "rsp": "OK"
            },
            "AT+GMI": {
                "flags":"",
                "rsp": "OK"
            },
            "AT+GMM": {
                "flags":"",
                "rsp": "OK"
            },
            "AT+GMR": {
                "flags":"",
                "rsp": "OK"
            }
        }
    }
}

```

## Instructions

Executing the program without flags will result in the fallowing output
```
usage: main.py [-h] -c CONN -v HOST -d MODEL [-i CONFIGPATH] [-o OUTPUTPATH]
main.py: error: the following arguments are required: -c/--connection, -v/--host, -d/--device
```

Run the program by executing the main python script with the apropriate flags. To get the help page type the fallowing command
```shell
python3 main.py -h
```
To get the fallowing output
```
usage: main.py [-h] -c CONN -v HOST -d MODEL [-i CONFIGPATH] [-o OUTPUTPATH]

options:
  -h, --help            show this help message and exit
  -c CONN, --connection CONN
                        Specify device connection type. (ssh/serial)
  -v HOST, --host HOST  Specify host ip or port.
  -d MODEL, --device MODEL
                        Specify device model.
  -i CONFIGPATH, --input CONFIGPATH
                        Specifies path of config.json file.
  -o OUTPUTPATH, --output OUTPUTPATH
                        Specify output directory.
```

Command examples
```
python3 main.py -c serial -d TRM240 -v /dev/ttyUSB3
python3 main.py -c ssh -d RUTX11 -v 192.168.1.1
```

The program's shows intermediate results and errors in the console. After finishing all the tests the results are save into the specified file (by default: output/{DeviceName}-{Time}.csv)

The program also has a email sendre and a ftp server uploader which can be configured with the config.json.