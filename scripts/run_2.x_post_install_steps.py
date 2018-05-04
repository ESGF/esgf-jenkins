import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="run esgf 2.x post install steps",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-n", "--vm_node", required=True, help="node to copy keypair from")
parser.add_argument("-d", "--dir", required=True, help="directory on master where keypair and other files for vm node will be copied from")
parser.add_argument("-H", "--vm_jenkins_home", required=True, help="vm user jenkins home directory")

args = parser.parse_args()
vm_node = args.vm_node
dir = args.dir
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
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo bash -c \"expect {w}/esgf-test-suite/scripts-llnl/auto-keypair.exp\"".format(w=workdir)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

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
# reboot vm
#
print("REBOOTING...{n}".format(n=vm_node))
cmd = "ssh {n} sudo reboot".format(n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

print("...wait for 15 seconds...")
time.sleep(15)
#cmd = "ssh {n} sudo /usr/local/bin/esg-node start".format(n=vm_node)
#cmd = "ssh -t -t {n} sudo bash -c 'export TERM=vt100; /usr/local/bin/esg-node start'".format(n=vm_node)

#cmd = "ssh -t -t jenkins@{n} sudo bash -c 'export TERM=vt100; /usr/local/bin/esg-node start'".format(n=vm_node)
cmd = "ssh -t -t {n} sudo /usr/local/bin/esg-node start".format(n=vm_node)
status = run_cmd(cmd, True, False, True)
sys.exit(status)

