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

parser.add_argument("-b", "--branch", default='master', help="git branch")
parser.add_argument("-p", "--python_path", required=True, help="python path")
parser.add_argument("-o", "--run_test_suite_options", 
                    default='!compute,!cog_create_user,!slcs',
                    help="options to run testsuite with - this will be passed as value to -a option ")
parser.add_argument("-f", "--firefox_path", required=True, help="path where firefox binary is installed")
parser.add_argument("-g", "--geckodriver_path", required=True, help="path where geckodriver is installed")

args = parser.parse_args()
branch = args.branch
run_options = args.run_test_suite_options
python_path = args.python_path
firefox_path = args.firefox_path
geckodriver_path = args.geckodriver_path

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

    #
    # assumptions: miniconda is installed under <workdir>/miniconda2/bin
    #
    conda_path = os.path.join(workdir, 'miniconda2', 'bin')
    os.environ["PATH"] = firefox_path + os.pathsep + geckodriver_path + os.pathsep + conda_path + os.pathsep +  os.environ["PATH"] 

    cmd = "env"
    ret_code = run_cmd(cmd, True, False, True)

    cmd = "which python"
    ret_code = run_cmd(cmd, True, False, True)

    std_options = "--nocapture --nologcapture --with-html --with-id -v"
    user_home = os.environ['HOME']
    conf_file_options = "--tc-file {home}/configs/my_config.ini".format(home=user_home)

    cmd = "{path}/python esgf-test.py {std_opt} {conf_opt} -a \'{opts}\'".format(path=python_path,
                                                                             std_opt=std_options,
                                                                             conf_opt=conf_file_options,
                                                                             opts=run_options)
    test_dir = "{w}/esgf-test-suite".format(w=workdir)
    print("xxx xxx test_dir: {d}".format(d=test_dir))

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

