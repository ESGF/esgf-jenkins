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
parser.add_argument("-p", "--python_path", required=True, help="python3 path on the node where this script is running from")
parser.add_argument("-n", "--node", required=True, help='esgf node')
parser.add_argument("-d", "--scp_dest", default="jenkins@pcmdi11.llnl.gov:/home/jenkins/jenkins_cvecheckerruns",
                    help="destination to scp cvechecker report to.")

args = parser.parse_args()
branch = args.branch
workdir = args.workdir
python_path = args.python_path
node = args.node
user = getpass.getuser()
scp_dest = args.scp_dest

url = "https://github.com/SNIC-NSC/esgf_scanner.git"

if not os.path.isdir(workdir):
    os.mkdir(workdir)

def get_esgf_scanner(workdir, branch='master'):

    repo_dir = "{d}/repos".format(d=workdir)
    if os.path.isdir(repo_dir) is False:
        cmd = "mkdir -p {d}".format(d=repo_dir)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{c}".format(c=cmd))
            return ret_code
    print("xxx repo_dir: {d}".format(d=repo_dir))
    the_repo_dir = "{d}/esgf_scanner".format(d=repo_dir)
    if os.path.isdir(the_repo_dir) is False:
        if branch == 'master':
            cmd = "git clone {url} {d}".format(url=url,d=the_repo_dir)
        else:
            cmd = "git clone -b {b} {url} {d}".format(d=the_repo_dir,
                                                      url=url,
                                                      b=branch)
        print("CMD: {c}".format(c=cmd))
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{cmd}".format(cmd=cmd))
            return ret_code

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
             "bash rungetpackagelists.sh {n} {u}".format(n=node, u=user),
             "bash generate_esgfconf.sh",
             "cp esgf.conf cvechecker",
             "cp exportedmutes cvechecker"]

for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True, the_repo_dir)
    if status != SUCCESS:
        print("FAIL...{c}".format(c=cmd))
        sys.exit(status)

current_path = os.environ["PATH"]
os.environ["PATH"] = "{p}:{curr}".format(p=python_path,
                                         curr=current_path)

report = os.path.join(the_repo_dir, 'esgfreport.txt')
cvechecker_dir = os.path.join(the_repo_dir, 'cvechecker')
cmds_list = ["md5sum exportedmutes",
             "bash firstuse.sh",
             "python3 cvechecker.py -u",
             "python3 cvechecker.py -i exportedmutes"]

for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True, cvechecker_dir)
    if status != SUCCESS:
        print("FAIL...{c}".format(c=cmd))
        sys.exit(status)

add_path = "export PATH={p}:$PATH".format(p=python_path)
cmd = "cd {d}; {a}; python3 cvechecker.py -r esgf.conf > {f}".format(d=cvechecker_dir,
                                                                     a=add_path,
                                                                     f=report)
print("CMD: {c}".format(c=cmd))
status = os.system(cmd)

current_time = time.localtime(time.time())
time_str = time.strftime("%Y%b%d%H%M", current_time)

tar_file = "jenkins_cvecheckerrun_{t}.tgz".format(t=time_str)
report_files = "packagelists.tgz {r}".format(r=report)
tar_cmd = "tar -cvzf {tar_file} {files}".format(tar_file=tar_file,
                                                files=report_files)

scp_cmd = "scp {tar_file} {dest}".format(tar_file=tar_file,
                                             dest=scp_dest)
cmds_list = [tar_cmd, scp_cmd]
for cmd in cmds_list:
    status = run_cmd(cmd, True, False, True, the_repo_dir)
    if status != SUCCESS:
        print("FAIL...{c}".format(c=cmd))
        sys.exit(status)

sys.exit(SUCCESS)
