import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Const import *
from CondaUtils import *

valid_py_vers = ["py2", "py3", "py2.7", "py3.6", "py3.7"]

parser = argparse.ArgumentParser(description="install miniconda",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-w", "--workdir",
                    help="working directory -- miniconda will be installed here")
parser.add_argument("-p", "--py_ver", choices=valid_py_vers,
                    help="python version, 'py2.7' or 'py3' or 'py3.7'")

args = parser.parse_args()
workdir = args.workdir
py_ver = args.py_ver

status, conda_path = install_miniconda(workdir, py_ver)
if status != SUCCESS:
    sys.exit(status)

conda_cmd = os.path.join(conda_path, 'conda')
cmd = "{c} install pip".format(c=conda_cmd)
status = run_cmd(cmd)

sys.exit(status)
