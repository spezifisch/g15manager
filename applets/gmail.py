import subprocess
import urllib2
from xml import sax

import gobject

def start():

    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password("New mail feed", "https://mail.google.com", mail, password)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

    process = subprocess.Popen(["g15composer", "/tmp/g15manager-gmail"])

    gobject.add_timeout(minutes * 60000, applet)

    return process

def applet():

    feed = urllib2.urlopen("https://mail.google.com/gmail/feed/atom")
    feed = feed.read()

    class handler(sax.ContentHandler):

        def __init__(self):
            self.startDocument()
            self.entries = list()
            self.actual = list()
            self.mail_count = "0"

        def startElement(self, name, attrs):
            self.actual.append(name)

            if name == "entry":
                self.entries.append(["", "", ""])

        def endElement(self, name):
            self.actual.pop()

        def characters(self, content):
            if (self.actual == ["feed", "fullcount"]):
                self.mail_count = int(self.mail_count + content)

            if (self.actual == ["feed", "entry", "title"]):
                temp_mail = self.entries.pop()
                temp_mail[0] = temp_mail[0] + content
                self.entries.append(temp_mail)

            if (self.actual == ["feed", "entry", "author", "name"]):
                temp_mail = self.entries.pop()
                temp_mail[1] = temp_mail[1] + content
                self.entries.append(temp_mail)

            if (self.actual == ["feed", "entry", "author", "email"]):
                temp_mail = self.entries.pop()
                temp_mail[2] = temp_mail[2] + content
                self.entries.append(temp_mail)


    atom = handler()
    sax.parseString(feed, atom)


    text = "TO 0 0 0 0 \"You have %i new mails from:\"" % atom.mail_count

    with open("/tmp/g15manager-gmail", "w") as pipe:
        pipe.write(text)

    return loop