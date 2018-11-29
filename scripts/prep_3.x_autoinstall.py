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

# this script is to be run from jenkins master as user 'jenkins'
#
# This scripts prepare the vm-node where we are going to run esg_node.py on.
# + copy over esgf.properties from master to vm node:
#   scp <conf_dir>/3.x/esgf.properties.<vm_node> <vm_node>:/tmp/esgf.properties
# + copy over config.ini needed for running esgf-test-suite later on.
#   scp <conf_dir>/esgf-test-suite/esgf-dev1_config.ini \
#       <test_suite_node>:<test_suite_node_jenkins_home>/esgf/my_config.ini
# + copy over esgf_pass to vm node
#   scp <conf_dir>/3.x/esgf_pass to <vm_node>:/tmp/.esgf_pass
#

parser.add_argument("-d", "--conf_dir", 
                    help='a directory on master where configs/templates can be found')
parser.add_argument("-n", "--vm_node", 
                    help='vm node name where esgf node is to be installed')
parser.add_argument("-H", "--vm_jenkins_home", 
                    help='vm node name jenkins home')
parser.add_argument("-t", "--test_suite_node", 
                    help='name of the node where esgf-test-suite is to be run from')
parser.add_argument("-w", "--test_suite_node_jenkins_home", 
                    help='user jenkins home on the node where esgf-test-suite is to be run from')
parser.add_argument("-m", "--migrate", default=False, action="store_true",
                    help="specify if doing migration")

args = parser.parse_args()
conf_dir = args.conf_dir
vm_node = args.vm_node
vm_jenkins_home = args.vm_jenkins_home
test_suite_node = args.test_suite_node
test_suite_node_jenkins_home = args.test_suite_node_jenkins_home
migrate = args.migrate

source = "{c}/esgf-test-suite/{n}_config.ini".format(c=conf_dir,
                                                     n=vm_node)
dest = "{ts}:{ts_jh}/esgf/{n}_config.ini".format(ts=test_suite_node,
                                                 ts_jh=test_suite_node_jenkins_home,
                                                 n=vm_node)

vm_dest = "{n}:{vm_jh}/esgf/{n}_config.ini".format(n=vm_node,
                                                   vm_jh=vm_jenkins_home)

cp_ts_conf_cmd = "scp {s} {d}".format(s=source, d=dest)
cp_vm_conf_cmd = "scp {s} {d}".format(s=source, d=vm_dest)

prop_file = "esgf.properties"

if migrate:
    src_prop_file = "{f}.{n}.migration".format(f=prop_file,
                                               n=vm_node)
else:
    src_prop_file = "{f}.{n}.fresh_install".format(f=prop_file,
                                                   n=vm_node)

cmds_list = [
    "scp {c}/3.x/{src_f} {n}:/tmp/{f}".format(c=conf_dir,
                                              src_f=src_prop_file,
                                              n=vm_node,
                                              f=prop_file),
    cp_ts_conf_cmd,
    cp_vm_conf_cmd,    
    "scp {c}/3.x/esgf_pass {n}:/tmp/.esgf_pass".format(c=conf_dir,
                                                       n=vm_node),
    "scp {c}/keypairs/keypair.{n}.tar {n}:/tmp/keypair.tar".format(c=conf_dir,
                                                      n=vm_node)
    ]

for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True)
    if status != SUCCESS:
        sys.exit(status)

sys.exit(SUCCESS)
