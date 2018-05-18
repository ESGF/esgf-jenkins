import sys
import os
import argparse
import time

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="run esgf-test-suite",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-b", "--branch", required=True, default='master',
                    help="git branch")
parser.add_argument("-o", "--run_test_suite_options", 
                    default='!compute,!cog_create_user,!slcs',
                    help="options to run testsuite with - this will be passed as value to -a option ")

args = parser.parse_args()
branch = args.branch
run_options = args.run_test_suite_options
print("xxx run_options: {o}".format(o=run_options))

def get_esgf_test_suite(workdir, branch='master'):

    if branch == 'master':
        cmd = "git clone https://github.com/ESGF/esgf-test-suite.git {d}".format(d=workdir)
    else:
        cmd = "git clone -b {b} https://github.com/ESGF/esgf-test-suite.git {d}".format(d=workdir,
                                                                                        b=branch)
    
    ret_code = run_cmd(cmd, True, False, True)
    return(ret_code)


def run_esgf_test_suite(workdir, run_options):

    std_options = "--nocapture --nologcapture --with-html --with-id -v"
    user_home = os.environ['HOME']
    conf_file_options = "--tc-file {home}/configs/my_config.ini".format(home=user_home)
    
    cmd = "python esgf-test.py {std_opt} {conf_opt} -a {opts}".format(std_opt=std_options,
                                                                      conf_opt=conf_file_options,
                                                                      opts=run_options)
    test_dir = "{w}/esgf-test-suite".format(w=workdir)

    ret_code = run_cmd(cmd, True, False, True, test_dir)
    return(ret_code)


current_time = time.localtime(time.time())
time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)
user_home = os.environ['HOME']
workdir = "{home}/work/esgf-test-suite-{time_stamp}".format(home=user_home,
                                                                time_stamp=time_str)
cmd = "mkdir -p {workdir}".format(workdir=workdir)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    print("FAIL...{cmd}".format(cmd=cmd))
    sys.exit(status)

status = get_esgf_test_suite(workdir, branch)
if status != SUCCESS:
    print("FAIL...get_esgf_test_suite")
    sys.exit(status)

status = run_esgf_test_suite(workdir, run_options)
if status != SUCCESS:
    print("FAIL...run_esgf_test_suite")

sys.exit(status)
