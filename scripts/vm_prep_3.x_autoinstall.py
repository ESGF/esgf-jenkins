import sys
import os
import argparse
import time

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="vm prepare for 3.x esgf autoinstall",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

#
# This script is to be run on the VM right before esg-autoinstall is run.
# This script prepares the esg-autoinstall.conf
#
current_time = time.localtime(time.time())
time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)

cmds_list = []
esgf_autoinstall_conf = "/esg/config/esgf.properties"

cmds_list = ["sudo mv {conf} {conf}.backup.{time_str}".format(conf=esgf_autoinstall_conf,
                                                             time_str=time_str),
            "sudo mv /tmp/esgf.properties {conf}".format(conf=esgf_autoinstall_conf),
            "sudo chown root {conf}".format(conf=esgf_autoinstall_conf),
            "sudo chgrp root {conf}".format(conf=esgf_autoinstall_conf),
            "sudo mv /tmp/.esgf_pass /esg/config/.esgf_pass",
            "sudo cp /esg/config/.esgf_pass /esg/config/.esg_pg_publisher_pass",
            "sudo cp /esg/config/.esgf_pass /esg/config/.esg_pg_pass",
            "sudo cp /esg/config/.esgf_pass /esg/config/.esg_keystore_pass"]

for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True)
    if status != SUCCESS:
        sys.exit(status)

