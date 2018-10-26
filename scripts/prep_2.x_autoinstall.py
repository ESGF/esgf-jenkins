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

#
# this script is to be run from jenkins master as user 'jenkins'
# scp <conf_dir>/2.x/esg-autoinstall.conf.<vm> <vm>:/tmp/esg-autoinstall.conf
# scp <conf_dir>/esgf-test-suite/<vm>_config.ini \
#        <test_suite_node>:<test_suite_node_jenkins_home>/esgf/my_config.ini
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

args = parser.parse_args()
conf_dir = args.conf_dir
vm_node = args.vm_node
vm_jenkins_home = args.vm_jenkins_home
test_suite_node = args.test_suite_node
test_suite_node_jenkins_home = args.test_suite_node_jenkins_home
autoinstall_conf = 'esg-autoinstall.conf'
cp_config_cmd = "scp {c}/2.x/{conf}.{n} {n}:/tmp/{conf}".format(c=conf_dir,
                                                                conf=autoinstall_conf,
                                                                n=vm_node)
source = "{c}/esgf-test-suite/{n}_config.ini".format(c=conf_dir,
                                                     n=vm_node)
dest = "{ts}:{ts_jh}/esgf/{n}_config.ini".format(n=vm_node,
                                                 ts=test_suite_node,
                                                 ts_jh=test_suite_node_jenkins_home)

vm_dest = "{n}:{vm_jh}/esgf/{n}_config.ini".format(n=vm_node,
                                                  vm_jh=vm_jenkins_home)


cp_ts_conf_cmd = "scp {s} {d}".format(s=source, d=dest)
cp_vm_conf_cmd = "scp {s} {d}".format(s=source, d=vm_dest)

cmds = [cp_config_cmd,
        cp_ts_conf_cmd,
        cp_vm_conf_cmd
        ]
for cmd in cmds:
    status = run_cmd(cmd, True, False, True)
    if status != SUCCESS:
        sys.exit(status)

sys.exit(status)


                                                                              
