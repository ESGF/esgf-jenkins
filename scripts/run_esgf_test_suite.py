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
parser.add_argument("-o", "--run_test_suite_options", required=True, default='master',
                    help="options to run testsuite with - this will be passed as value to -a option ")

args = parser.parse_args()
branch = args.branch

def get_esgf_test_suite(branch='master'):
    current_time = time.localtime(time.time())
    time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)
    user_home = os.environ['HOME']
    workdir = "{home}/work/esgf-test-suite-{time_stamp}".format(home=user_home,
                                                                time_stamp=time_str)
    cmd = "mkdir -p {workdir}".format(workdir=workdir)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))
        return ret_code

    if branch == 'master':
        cmd = "git clone https://github.com/ESGF/esgf-test-suite.git {d}".format(d=workdir)
    else:
        cmd = "git clone -b {b} https://github.com/ESGF/esgf-test-suite.git {d}".format(d=workdir,
                                                                                        b=branch)
    
    ret_code = run_cmd(cmd, True, False, True, workdir)
    return(ret_code)

ret_code = get_esgf_test_suite(branch)
