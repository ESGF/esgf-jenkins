import os
import time
import fileinput
import re

from Const import *
from Util import *
from MiscUtil import update_file


def update_auto_keypair(file_to_update):

    autoinstall_conf = '/usr/local/etc/esg-autoinstall.conf'
    conf_fh = open(autoinstall_conf, 'r')

    p = None
    for line in conf_fh:
        match_obj = re.match(r'set\s+ADMINPASS\s+(\S+)')
        if match_obj:
            p = match_obj.group(1)
            p.strip("\"")
            print("xxx xxx DEBUG DEBUG p: {p}".format(p=p))

    if not p:
        print("FAIL...did not find the setting for ADMINPASS in {f}".format(f=autoinstall_conf))
        return FAILURE

    update_file(file_to_update, 'CHANGEME', p)
    return SUCCESS


    
    
