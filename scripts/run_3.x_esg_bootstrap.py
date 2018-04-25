import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="prepare a virtual machine",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-n", "--vm_node", help="vm node name", required=True)
parser.add_argument("-t", "--git_tag", help="git tag", required=True)
parser.add_argument("-b", "--git_branch", help="git branch", required=True)

args = parser.parse_args()
vm_node = args.vm_node
tag = args.git_tag
branch = args.git_branch

url = "https://github.com/ESGF/esgf-installer.git"

cmd = "git clone {u}".format(u=url)
ret_code = run_cmd(cmd, True, False, True)
if ret_code != SUCCESS:
    print("FAIL...{c}".format(c=cmd))
    sys.exit(ret_code)

cmd = "git checkout {t} -b {b}".format(t=tag, b=branch)
ret_code = run_cmd(cmd, True, False, True, "esgf-installer")

