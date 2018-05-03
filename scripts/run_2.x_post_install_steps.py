import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="install esgf 2.x",
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
# run this on master node as user 'jenkins'
#

#
# install keypair
#

cmd = "scp {dir}/keypair.tar {n}:/tmp".format(dir=dir, n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo bash -c 'cd /tmp; tar -xvf /tmp/keypair.tar'".format(n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} git clone https://github.com/ESGF/esgf-test-suite".format(n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo expect {w}/esgf-test-suite/scripts-llnl/auto-keypair.exp".format(w=workdir,
                                                                                     n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

#
# update /usr/local/tomcat/conf/server.xml
#
dest_file = '/usr/local/tomcat/conf/server.xml'
cmd = "scp {d}/tomcat.server.xml {n}:/tmp/server.xml".format(n=vm_node, d=dir)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo cp /tmp/server.xml {dest_file}".format(n=vm_node,
                                                           dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo chown tomcat {dest_file}".format(n=vm_node,
                                                     dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo chgrp tomcat {dest_file}".format(n=vm_node,
                                                     dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

#
# updated /etc/httpd/conf/esgf-httpd.conf
#
dest_file = "/etc/httpd/conf/esgf-httpd.conf"
cmd = "scp {d}/esgf-httpd.conf {n}:/tmp".format(n=vm_node, d=dir)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo cp /tmp/esgf-httpd.conf {dest_file}".format(n=vm_node,
                                                                dest_file=dest_file)
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
cmd = "ssh {n} sudo /usr/local/bin/esg-node start".format(n=vm_node)
status = run_cmd(cmd, True, False, True)
sys.exit(status)

