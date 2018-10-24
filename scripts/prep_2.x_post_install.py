import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="prep for 2.x post install",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-n", "--vm_node", required=True, help="node to copy keypair from")
parser.add_argument("-d", "--dir", required=True, help="directory on master where keypair and other files for vm node will be copied from")
parser.add_argument("-w", "--vm_jenkins_home", required=True, help="vm node jenkins' home")

args = parser.parse_args()
vm_node = args.vm_node
dir = args.dir
vm_jenkins_home = args.vm_jenkins_home

sys.stdout.flush()

#
# run this on master node as user 'jenkins'
#
#dest_file = "/etc/httpd/conf/esgf-httpd.conf"

#src_file = "myproxy-logon.exp.{n}".format(n=vm_node)

cmds_list = [
    "scp {dir}/keypairs/keypair.{n}.tar {n}:/tmp/keypair.tar".format(dir=dir, n=vm_node),
    "scp {d}/tomcat.server.xml {n}:/tmp/server.xml".format(n=vm_node, d=dir),
    "scp {d}/esgf-httpd.conf {n}:/tmp".format(n=vm_node, d=dir),
    "scp {d}/2.x/auto-keypair.exp.{n} {n}:{h}/auto-keypair.exp".format(d=dir,
                                                                       n=vm_node,
                                                                       h=vm_jenkins_home),
    ]

#    "scp {d}/2.x/{f} {n}:{h}/myproxy-logon.exp".format(d=dir,
#                                                       f=src_file,
#                                                       n=vm_node,
#                                                       h=vm_jenkins_home)

for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True)
    if status != SUCCESS:
        sys.exit(status)

sys.exit(SUCCESS)

