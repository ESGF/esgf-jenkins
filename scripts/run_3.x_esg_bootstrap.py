import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="run 3.x esg_bootstrap",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-w", "--workdir", required=True, 
                    help="workdir where this script will write to")

parser.add_argument("-b", "--branch", default='master',
                    help="branch of esgf-installer repo to use")

parser.add_argument("-m", "--migrate", default=False, action="store_true",
                    help="specify if doing migration")


args = parser.parse_args()
workdir = args.workdir
branch  = args.branch
migrate = args.migrate

repo_url = "https://github.com/ESGF/esgf-installer.git"
if branch == 'master':
    cmd = "git clone {repo}".format(repo=repo_url)
else:
    cmd = "git clone -b {branch} {repo}".format(branch=branch,
                                                repo=repo_url)

status = run_cmd(cmd, True, False, True, workdir)
if status != SUCCESS:
    print("FAIL...{cmd}".format(cmd=cmd))
    sys.exit(status)

repo_dir = "{workdir}/esgf-installer".format(workdir=workdir)
if migrate:
    cmd = "sudo {repo_dir}/esg_bootstrap.sh migrate".format(repo_dir=repo_dir)
else:
    cmd = "sudo {repo_dir}/esg_bootstrap.sh".format(repo_dir=repo_dir)

status = run_cmd(cmd, True, False, True, repo_dir)
sys.exit(status)



