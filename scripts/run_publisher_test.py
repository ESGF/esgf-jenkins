import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="run esgf-test-suite",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-b", "--branch", default='devel', help="git branch of esg-publisher repo")
parser.add_argument("-w", "--workdir", required=True, help="working directory where this script can write to")
parser.add_argument("-e", "--esgf_conda_env", default='devel', help="esgf conda environment to run test in")

args = parser.parse_args()
branch = args.branch
workdir = args.workdir
esgf_conda_env = args.esgf_conda_env

def get_esg_publisher(workdir, env, branch='devel'):

    repo_dir = "{d}/repos".format(d=workdir)
    if os.path.isdir(repo_dir) is False:
        cmd = "mkdir -p {d}".format(repo_dir)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{c}".format(c=cmd))
            return ret_code
    
    the_repo_dir = "{d}/esg-publisher".format(d=repo_dir)
    if os.path.isdir(the_repo_dir) is False:
        if branch == 'master':
            cmd = "git clone https://github.com/ESGF/esg_publisher.git {d}".format(d=the_repo_dir)
        else:
            cmd = "git clone -b {b} https://github.com/ESGF/esg_publisher {d}".format(d=the_repo_dir,
                                                                                            b=branch)
        ret_code = run_cmd(cmd, True, False, True)
    cmd = "git pull"
    ret_code = run_cmd(cmd, True, False, True, "{d}".format(d=the_repo_dir))
    if ret_code != SUCCESS:
        print("FAIL...{c}".format(c=cmd))
        return ret_code

    dir = "{repo_dir}/src/python/esgcet".format(repo_dir=repo_dir)
    cmds_list = ["cd {dir}".format(dir=dir),
                 "sudo python setup.py install",
                 "sudo esgtest_publish -x -d"]
    conda_path = "/usr/local/conda/bin"
    ret_code = run_in_conda_env(conda_path, env, cmds_list)
    return(ret_code)

def run_esgf_publisher_test(esgf_conda_env):

    cmds_list = ["sudo esgtest_publish -x -d"]
    conda_path = "/usr/local/conda/bin"
    ret_code = run_in_conda_env(conda_path, esgf_conda_env, cmds_list)
    return(ret_code)

status = get_esg_publisher(workdir, esgf_conda_env, branch)
if status != SUCCESS:
    sys.exit(status)

status = run_esgf_publisher_test(esgf_conda_env)
sys.exit(status)






