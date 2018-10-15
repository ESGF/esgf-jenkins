import sys
import os
import argparse
import time
import getpass

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="run esgf scanner",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-b", "--branch", default='master', help="git branch")
parser.add_argument("-w", "--workdir", required=True, help='work dir where esgf_scanner will be checked out')
parser.add_argument("-p", "--python_path", required=True, help="python3 path")
parser.add_argument("-n", "--node", required=True, help='esgf node')

args = parser.parse_args()
branch = args.branch
workdir = args.workdir
python_path = args.python_path
node = args.node
user = getpass.getuser()

url = "https://github.com/SNIC-NSC/esgf_scanner.git"

def get_esgf_scanner(workdir, branch='master'):

    repo_dir = "{d}/repos".format(d=workdir)
    if os.path.isdir(repo_dir) is False:
        cmd = "mkdir -p {d}".format(repo_dir)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{c}".format(c=cmd))
            return ret_code

    the_repo_dir = "{d}/esgf_scanner".format(d=repo_dir)
    if os.path.isdir(the_repo_dir) is False:
        if branch == 'master':
            cmd = "git clone {url} {d}".format(url=url,d=the_repo_dir)
        else:
            cmd = "git clone -b {b} {url} {d}".format(d=the_repo_dir,
                                                      url=url,
                                                      b=branch)
        ret_code = run_cmd(cmd, True, False, True)
    cmd = "git pull"
    ret_code = run_cmd(cmd, True, False, True, "{d}".format(d=the_repo_dir))
    return(ret_code, the_repo_dir)

status, the_repo_dir = get_esgf_scanner(workdir, branch)
if status != SUCCESS:
    print("FAIL...get_esgf_scanner")
    sys.exit(status)

cmds_list = ["git submodule init",
             "git submodule update",
             "bash firstuse.sh",
             "bash rungetpackagelists.sh {n} {u}".format(n=vm_node, u=user),
             "bash generate_esgfconf.sh",
             "cp esgf.conf cvechecker",
             "cp exportedmutes cvechecker"]

for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True, the_repo_dir)
    if status != SUCCESS:
        print("FAIL...{c}".format(c=cmd))
        sys.exit(status)




