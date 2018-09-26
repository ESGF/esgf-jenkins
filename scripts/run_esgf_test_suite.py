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
parser.add_argument("-w", "--workdir", required=True, help="working directory where this script can write to")
parser.add_argument("-c", "--config_ini", required=True, help="my_config.ini full path file name")

args = parser.parse_args()
branch = args.branch
run_options = args.run_test_suite_options
python_path = args.python_path
firefox_path = args.firefox_path
geckodriver_path = args.geckodriver_path
workdir = args.workdir
config_ini = args.config_ini

print("run_options: {o}".format(o=run_options))

#
# ASSUMPTIONS -- the node where this script is running should have the following:
#    miniconda is installed under <workdir>/esgf/miniconda2/bin
#    firefox is installed under <firefox_path>
#    geckodriver is installed under <geckodriver_path>
#    my_config.ini is available in this node's <workdir>
#

def get_esgf_test_suite(workdir, branch='master'):

    repo_dir = "{d}/repos".format(d=workdir)
    if os.path.isdir(repo_dir) is False:
        cmd = "mkdir -p {d}".format(repo_dir)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{c}".format(c=cmd))
            return ret_code
    
    the_repo_dir = "{d}/esgf-test-suite".format(d=repo_dir)
    if os.path.isdir(the_repo_dir) is False:
        if branch == 'master':
            cmd = "git clone https://github.com/ESGF/esgf-test-suite.git {d}".format(d=the_repo_dir)
        else:
            cmd = "git clone -b {b} https://github.com/ESGF/esgf-test-suite.git {d}".format(d=the_repo_dir,
                                                                                            b=branch)
        ret_code = run_cmd(cmd, True, False, True)
    cmd = "git pull"
    ret_code = run_cmd(cmd, True, False, True, "{d}".format(d=the_repo_dir))
    return(ret_code)

def install_packages(python_path):

    os.environ["PATH"] = python_path + os.pathsep + os.environ["PATH"]
 
    cmd = "which python"
    ret_code = run_cmd(cmd, True, False, True)

    cmd = "pip install -U nose pyopenssl MyProxyClient selenium requests nose-testconfig nose-htmloutput lxml"
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        return ret_code

    cmd = "pip install --upgrade pip"
    ret_code = run_cmd(cmd, True, False, True)
    return(ret_code)

def run_esgf_test_suite(config_ini_file, workdir, run_options):

    os.environ["PATH"] = firefox_path + os.pathsep + geckodriver_path + os.pathsep + os.environ["PATH"] 

    cmd = "which firefox"
    ret_code = run_cmd(cmd, True, False, True)

    #std_options = "--nocapture --nologcapture --with-html --with-id -v"
    std_options = "--with-html --with-id --verbosity=2 --verbose"
    user_home = os.environ['HOME']
    conf_file_options = "--tc-file {config_ini}".format(config_ini=config_ini_file,
                                                        home=user_home)

    cmd = "{path}/python esgf-test.py {std_opt} {conf_opt} -a \'{opts}\'".format(path=python_path,
                                                                                 std_opt=std_options,
                                                                                 conf_opt=conf_file_options,
                                                                                 opts=run_options)
    test_dir = "{w}/repos/esgf-test-suite/esgf-test-suite".format(w=workdir)
    print("xxx xxx test_dir: {d}".format(d=test_dir))

    ret_code = run_cmd(cmd, True, False, True, test_dir)
    return(ret_code)


current_time = time.localtime(time.time())
time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)
user_home = os.environ['HOME']

status = install_packages(python_path)
if status != SUCCESS:
    print("FAIL...install_packages")
    sys.exit(status)

status = get_esgf_test_suite(workdir, branch)
if status != SUCCESS:
    print("FAIL...get_esgf_test_suite")
    sys.exit(status)

status = run_esgf_test_suite(config_ini, workdir, run_options)
if status != SUCCESS:
    print("FAIL...run_esgf_test_suite")

sys.exit(status)

