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

args = parser.parse_args()
vm_node = args.vm_node
dir = args.dir
workdir = "/tmp"
print("xxx workdir: ", workdir)
print("xxx dir: ", dir)

#
# run this on master node
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

cmd = "ssh {n} bash -c \"cd {w}; git clone https://github.com/ESGF/esgf-test-suite\n".format(w=workdir,
                                                                                             n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo expect auto-keypair.exp".format(n=vm_node)
status = run_cmd(cmd, True, False, True, "{w}/esgf-test-suite/scripts-llnl".format(w=workdir))
if status != SUCCESS:
    sys.exit(status)

#
# update /usr/local/tomcat/conf/server.xml
#
dest_file = '/usr/local/tomcat/conf/server.xml'
cmd = "scp {d}/server.xml {n}:/tmp".format(n=node, d=dir)
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
cmd = "scp {d}/esgf-httpd.conf {n}:/tmp".format(n=node, d=dir)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "ssh {n} sudo cp /tmp/esgf-httpd.conf {dest_file}".format(n=vm_node,
                                                                dest_file=dest_file)
status = run_cmd(cmd, True, False, True)
sys.exit(status)

