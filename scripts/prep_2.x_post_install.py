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

args = parser.parse_args()
vm_node = args.vm_node
dir = args.dir

sys.stdout.flush()

#
# run this on master node as user 'jenkins'
#

cmd = "scp {dir}/keypair.tar {n}:/tmp".format(dir=dir, n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

cmd = "scp {d}/tomcat.server.xml {n}:/tmp/server.xml".format(n=vm_node, d=dir)

status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)


dest_file = "/etc/httpd/conf/esgf-httpd.conf"
cmd = "scp {d}/esgf-httpd.conf {n}:/tmp".format(n=vm_node, d=dir)
status = run_cmd(cmd, True, False, True)

sys.exit(status)

