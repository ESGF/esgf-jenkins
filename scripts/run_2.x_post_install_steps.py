import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="install esgf 2.x",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-w", "--workdir", required=True, 
                    help="work directory that this script can write to.")
parser.add_argument("-n", "--node", required=True, help="node to copy keypair from")
parser.add_argument("-d", "--dir", required=True, help="directory on node where keypair and other files for vm host will be copied from")

args = parser.parse_args()
workdir = args.workdir
node = args.node
dir = args.dir

#
# install keypair
#

cmd = "scp jenkins@{n}:{dir}/keypair.tar /tmp".format(n=node, dir=dir)
status = run_cmd(cmd, True, True, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "tar -xvf keypair.tar"
status = run_cmd(cmd, True, True, True, "/tmp")
if status != SUCCESS:
    sys.exit(status)

cmd = "git clone https://github.com/ESGF/esgf-test-suite"
status = run_cmd(cmd, True, True, True, workdir)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo expect auto-keypair.exp"
status = run_cmd(cmd, True, True, True, "{w}/esgf-test-suite/scripts-llnl".format(w=workdir))
if status != SUCCESS:
    sys.exit(status)

#
# update /usr/local/tomcat/conf/server.xml
#
dest_file = '/usr/local/tomcat/conf/server.xml'
cmd = "sudo scp jenkins@{n}:{d}/server.xml {dest_file}".format(n=node, d=dir,
                                                       dest_file=dest_file)
status = run_cmd(cmd, True, True, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo chown tomcat {dest_file}".format(dest_file=dest_file)
status = run_cmd(cmd, True, True, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo chgrp tomcat {dest_file}".format(dest_file=dest_file)
status = run_cmd(cmd, True, True, True)
if status != SUCCESS:
    sys.exit(status)

#
# updated /etc/httpd/conf/esgf-httpd.conf
#
dest_file = "/etc/httpd/conf/esgf-httpd.conf"
cmd = "sudo scp {n}:{d}/esgf-httpd.conf {dest_file}".format(n=node, d=dir,
                                                            dest_file=dest_file)
status = run_cmd(cmd, True, True, True)
if status != SUCCESS:
    sys.exit(status)

