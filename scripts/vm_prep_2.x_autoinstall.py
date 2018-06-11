import sys
import os
import argparse
import time

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="vm prepare for 2.x esgf autoinstall",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

#
# This script is to be run on the VM right before esg-autoinstall is run.
# This script prepares the esg-autoinstall.conf
#
current_time = time.localtime(time.time())
time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)

esgf_autoinstall_conf = "/usr/local/etc/esg-autoinstall.conf"
cmd = "sudo mv {conf} {conf}.backup.{time_str}".format(conf=esgf_autoinstall_conf,
                                                       time_str=time_str)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo mv /tmp/esg-autoinstall.conf {conf}".format(conf=esgf_autoinstall_conf)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo chown root {conf}".format(conf=esgf_autoinstall_conf)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo chgrp root {conf}".format(conf=esgf_autoinstall_conf)
status = run_cmd(cmd, True, False, True)
sys.exit(status)


