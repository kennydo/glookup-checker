import os
import smtplib

from difflib import unified_diff
from email.mime.text import MIMEText
from getpass import getuser
from subprocess import Popen, PIPE

OLD_GLOOKUP_PATH = os.path.expanduser("~/.old_glookup")

def get_old_glookup(filename=OLD_GLOOKUP_PATH):
    try:
        with open(filename, "r") as f:
            return f.read()
    except IOError as e:
        return ""

def get_new_glookup():
    p = Popen(["glookup"], stdout=PIPE, stderr=PIPE)
    return "%s\n%s" % (p.stdout.read(), p.stderr.read())

def email_address():
    return "%s@imail.eecs.berkeley.edu" % getuser()

def save_old_glookup(s, filename=OLD_GLOOKUP_PATH):
    with open(filename, "w") as f:
        f.write(s)

def get_diff(old, new):
    d = unified_diff(old, new)
    ret = ""
    for line in d:
        ret += line + "\n"
    return ret

if __name__=="__main__":
    old_glookup = get_old_glookup()
    new_glookup = get_new_glookup()

    diff = get_diff(old_glookup.split("\n"), new_glookup.split("\n"))
    if diff:
        msg = MIMEText(diff)
        email_addr = email_address()

        msg["Subject"] = "glookup Changed"
        msg["From"] = email_addr
        msg["To"] = email_addr

        s = smtplib.SMTP("localhost")
        s.sendmail(msg["From"], [msg["To"]], msg.as_string())
        s.quit()

        save_old_glookup(new_glookup)
