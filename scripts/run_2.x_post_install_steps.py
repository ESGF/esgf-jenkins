import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *
from MiscUtil import *

parser = argparse.ArgumentParser(description="run esgf 2.x post install steps",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-H", "--vm_jenkins_home", required=True, help="vm user jenkins home directory")

args = parser.parse_args()
workdir = args.vm_jenkins_home

sys.stdout.flush()

#
# run this on vm node as user 'jenkins'
#

#
# install keypair
#

cmd = "sudo bash -c 'cd /tmp; tar -xvf keypair.tar'"
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

# in case this is a rerun, and esgf-test-suite repo already exists
cmd = "rm -rf {workdir}/esgf-test-suite".format(workdir=workdir)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "git clone https://github.com/ESGF/esgf-test-suite"
status = run_cmd(cmd, True, False, True, workdir)
if status != SUCCESS:
    sys.exit(status)

#cmd = "sudo bash -c \"export TERM=vt100; expect {w}/esgf-test-suite/scripts-llnl/auto-keypair.exp\"".format(w=workdir)
#status = run_cmd(cmd, True, False, True)
#if status != SUCCESS:
#    sys.exit(status)

#
# update /usr/local/tomcat/conf/server.xml
#
dest_file = '/usr/local/tomcat/conf/server.xml'
cmd = "sudo mv {orig} {orig}.ORIG".format(orig=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo cp /tmp/server.xml {dest_file}".format(dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo chown tomcat {dest_file}".format(dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo chgrp tomcat {dest_file}".format(dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

#
# updated /etc/httpd/conf/esgf-httpd.conf
#
dest_file = "/etc/httpd/conf/esgf-httpd.conf"
cmd = "sudo cp /tmp/esgf-httpd.conf {dest_file}".format(dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

#
# update /usr/local/cog/cog_config/cog_settings.cfg
#
print("xxx DEBUG...going to update cog_settings.cfg to set USE_CAPTCHA to False")
file_to_update = '/usr/local/cog/cog_config/cog_settings.cfg'
var_val_pairs_list = ['USE_CAPTCHA=False']
status = update_cog_settings_conf(var_val_pairs_list, '=', workdir)

sys.exit(status)

