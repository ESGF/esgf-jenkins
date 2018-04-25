import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="install esgf 2.x",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-d", "--dist", required=True, choices=['master', 'devel'],
                    help="distribution, 'devel' or 'master'")
parser.add_argument("-v", "--version", required=True,
                    help="distribution, 'devel' or 'master'")

args = parser.parse_args()
dist = args.dist
version = args.version

# get esg-bootstrap
base_url = "http://distrib-coffee.ipsl.jussieu.fr/pub/esgf/dist"
bin_dir = "/usr/local/bin"
if dist == 'devel':
    url = "{b}/devel/{v}/esgf-installer/esg-bootstrap".format(b=base_url,
                                                             v=version)
else:
    url = "{b}/{v}/esgf-installer/esg-bootstrap".format(b=base_url,
                                                        v=version)
    
cmd = "sudo wget -O esg-bootstrap {u} --no-check-certificate".format(u=url)

status = run_cmd(cmd, True, False, True, bin_dir)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo chmod 555 esg-bootstrap"
status = run_cmd(cmd, True, False, True, bin_dir)
if status != SUCCESS:
    sys.exit(status)

cmd = "sudo ./esg-bootstrap"
status = run_cmd(cmd, True, False, True, bin_dir)

sys.exit(status)

