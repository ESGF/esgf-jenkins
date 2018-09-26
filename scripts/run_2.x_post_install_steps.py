import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *
from MiscUtil import *
from Util2x import update_auto_keypair
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

auto_keypair_file = "{w}/auto-keypair.exp".format(w=workdir)
status = update_auto_keypair(auto_keypair_file, workdir)
if status != SUCCESS:
    sys.exit(status)

#
# update /usr/local/tomcat/conf/server.xml
#
dest_file = '/usr/local/tomcat/conf/server.xml'

cmds_list = ["sudo mv {orig} {orig}.ORIG".format(orig=dest_file),
             "sudo cp /tmp/server.xml {dest_file}".format(dest_file=dest_file),
             "sudo chown tomcat {dest_file}".format(dest_file=dest_file),
             "sudo chgrp tomcat {dest_file}".format(dest_file=dest_file)
             ]
for cmd in cmds_list:
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
file_to_update = '/usr/local/cog/cog_config/cog_settings.cfg'
var_val_pairs_list = ['USE_CAPTCHA=False']
status = update_cog_settings_conf(var_val_pairs_list, '=', workdir)

sys.exit(status)

