from smtplib import SMTP_SSL
import ssl

def sendDoneMsg(cfg):
    context = ssl.create_default_context()
    with SMTP_SSL(cfg["server"], cfg["port"], context=context) as server:
        server.login(cfg["sender"], cfg["pass"])
        server.sendmail(cfg["sender"], cfg["receiver"], cfg["subject"] + "\n\n" + cfg["message"])