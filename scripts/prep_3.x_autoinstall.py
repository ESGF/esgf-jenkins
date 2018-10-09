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
parser.add_argument("-t", "--test_suite_node", 
                    help='name of the node where esgf-test-suite is to be run from')
parser.add_argument("-w", "--test_suite_node_jenkins_home", 
                    help='user jenkins home on the node where esgf-test-suite is to be run from')

args = parser.parse_args()
conf_dir = args.conf_dir
vm_node = args.vm_node
test_suite_node = args.test_suite_node
test_suite_node_jenkins_home = args.test_suite_node_jenkins_home

cmds_list = [
    "scp {c}/3.x/esgf.properties.{n} {n}:/tmp/esgf.properties".format(c=conf_dir,
                                                                        n=vm_node),
    "scp {c}/esgf-test-suite/{n}_config.ini {ts}:{ts_jh}/esgf/my_config.ini".format(c=conf_dir,
                                                                                    n=vm_node,
                                                                                    ts=test_suite_node,
                                                                                    ts_jh=test_suite_node_jenkins_home),
    "scp {c}/3.x/esgf_pass {n}:/tmp/.esgf_pass".format(c=conf_dir,
                                                       n=vm_node),
    "scp {c}/keypair.{n}.tar {n}:/tmp/keypair.tar".format(c=conf_dir,
                                                      n=vm_node)
    ]

for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True)
    if status != SUCCESS:
        sys.exit(status)

sys.exit(SUCCESS)
