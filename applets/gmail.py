import subprocess
import gobject
import urllib2
import base64
from xml import sax

import gnomekeyring

def start(user,passwd, minutes):

    process = subprocess.Popen(["g15composer", "/tmp/g15manager-gmail"])

    user_passwd = "%s:%s" % (user,passwd)
    
    applet(user_passwd)
    gobject.timeout_add(minutes*60000, applet, user_passwd)

    return process

def applet(user_passwd):

    title = "MC 1\n" + "TO 0 0 1 1 \"Gmail - Inbox\"\n"

    try:
        auth = base64.encodestring(user_passwd).strip()
        request = urllib2.Request("https://mail.google.com/gmail/feed/atom")
        request.add_header("Authorization", "Basic %s" % auth)
        opener = apply(urllib2.build_opener)
        feed = opener.open(request).read()
        opener.close()

    except urllib2.HTTPError,e:
        if str(e).split()[2] == "401:":
            text = title + "TO 0 20 1 1 \"The user or password are wrong\"\n" + "MC 0\n"

        else:
            text = title + "TO 0 25 0 1 \"G15 Manager can't connect to Gmail\"\n" + "MC 0\n"

        with open("/tmp/g15manager-gmail", "w") as pipe:
            pipe.write(text)
        return loop


    class handler(sax.ContentHandler):

        def __init__(self):
                self.startDocument()
                self.entries=list()
                self.actual=list()
                self.mail_count="0"

        def startElement( self, name, attrs):
                self.actual.append(name)

                if name == "entry":
                        self.entries.append(["","",""])

        def endElement( self, name):
                self.actual.pop()

        def characters( self, content):
                if (self.actual==[ "feed", "fullcount" ]):
                        self.mail_count = int(self.mail_count+content)

                if (self.actual==[ "feed", "entry", "author", "email" ]):
                        temp_mail=self.entries.pop()
                        temp_mail[0]=temp_mail[0]+content
                        self.entries.append(temp_mail)

                if (self.actual==[ "feed", "entry", "author", "name" ]):
                        temp_mail=self.entries.pop()
                        temp_mail[1]=temp_mail[1]+content
                        self.entries.append(temp_mail)

                if (self.actual==[ "feed", "entry", "title" ]):
                        temp_mail=self.entries.pop()
                        temp_mail[2]=temp_mail[2]+content
                        self.entries.append(temp_mail)


    parsed_feed = handler()
    sax.parseString(feed, parsed_feed)

    if parsed_feed.mail_count == 0:
        text = title + "TO 0 10 1 1 \"You haven't new mails\"\n"

    elif parsed_feed.mail_count == 1:
        text = title + "TO 0 10 0 1 \"You have 1 new mail from:\"\n" + \
            "TO 0 20 0 1 \"%s\"\n" % parsed_feed.entries[0][0]

    else:
        text = title + "TO 0 10 0 1 \"You have %i new mail from:\"\n" % parsed_feed.mail_count + \
            "TO 0 20 0 1 \"%s\"\n" % parsed_feed.entries[0][0] + \
            "TO 0 28 0 1 \"%s\"\n" % parsed_feed.entries[1][0]
        if parsed_feed.mail_count > 2:
            text += "TO 0 36 0 1 \"%s\"\n" % parsed_feed.entries[2][0]

    text += "MC 0\n"
    
    with open("/tmp/g15manager-gmail", "w") as pipe:
        pipe.write(text)

    return loop


def save(user,passwd):
    if gnomekeyring.get_info_sync("g15_manager").get_is_locked():
        gnomekeyring.unlock_sync("g15_manager","password")

    if not "g15_manager" in gnomekeyring.list_keyring_names_sync():
        gnomekeyring.create_sync("g15_manager","password")
    if user != "" and passwd != "":
        gnomekeyring.item_create_sync("g15_manager", gnomekeyring.ITEM_GENERIC_SECRET,user,{},passwd,True)

    gnomekeyring.lock_sync("g15_manager")


def load():
    user = ""
    passwd = ""

    if gnomekeyring.get_info_sync("g15_manager").get_is_locked():
        gnomekeyring.unlock_sync("g15_manager","password")


    if "g15_manager" in gnomekeyring.list_keyring_names_sync():
        ids = gnomekeyring.list_item_ids_sync("g15_manager")
        item = gnomekeyring.item_get_info_sync("g15_manager", ids[0])
        user = item.get_display_name()
        passwd = item.get_secret()

    gnomekeyring.lock_sync("g15_manager")

    return user, passwd