import os
import time
import fileinput
import re

from Const import *
from Util import *
from MiscUtil import update_file



def get_admin_cred():

    autoinstall_conf = '/usr/local/etc/esg-autoinstall.conf'

    cmd = "sudo bash -c \"chmod 644 {f}\"".format(f=autoinstall_conf)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        return None

    conf_fh = open(autoinstall_conf, 'r')

    p = None
    for line in conf_fh:
        match_obj = re.match(r'set\s+ADMINPASS\s+\"(\S+)\"', line)
        if match_obj:
            p = match_obj.group(1)
    if not p:
        print("FAIL...did not find the setting for ADMINPASS in {f}".format(f=autoinstall_conf))
        return None

    cmd = "sudo bash -c \"chmod 640 {f}\"".format(f=autoinstall_conf)
    ret_code = run_cmd(cmd, True, False, True)

    return p

def update_auto_keypair(file_to_update, workdir):

    p = get_admin_cred()
    if p:
        update_file(file_to_update, 'CHANGEME', p, workdir)
    else:
        return FAILURE

    return SUCCESS

def update_myproxy_logon_exp(node, home, workdir):
    '''
    repo_dir: esgf-jenkins repo dir
    workdir: working directory where temporary files can be created.
    '''
    p = get_admin_cred()
    this_dir = os.path.abspath(os.path.dirname(__file__))
    file_to_update = os.path.join(this_dir, '..', 'scripts', 'expect', 'myproxy-logon.exp')

    if p:
        update_file(file_to_update, 'CHANGEME', p, workdir)
        update_file(file_to_update, 'ESGFNODE', node, workdir)
        update_file(file_to_update, 'USERHOME', home, workdir)

    return SUCCESS

