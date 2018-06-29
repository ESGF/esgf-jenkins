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

#sh "scp ${conf_dir}/3.x/esgf.properties.${vm_node} ${vm_node}:/tmp/esgf.properties"
#sh "scp ${conf_dir}/${vm_node}_config.ini ${test_suite_node}:${test_suite_node_jenkins_home}/esgf/my_config.ini"

# this script is to be run from jenkins master as user 'jenkins'

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

cmd = "scp {c}/2.x/esg-autoinstall.conf.{n} {n}:/tmp/esg-autoinstall.conf".format(c=conf_dir, 
                                                                                  n=vm_node)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

source = "{c}/esgf-test-suite/{n}_config.ini".format(c=conf_dir,
                                                     n=vm_node)
dest = "{ts}:{ts_jh}/esgf/my_config.ini".format(ts=test_suite_node,
                                                ts_jh=test_suite_node_jenkins_home)

cmd = "scp {s} {d}".format(s=source, d=dest)
status = run_cmd(cmd, True, False, True)
sys.exit(status)

                                                                              
