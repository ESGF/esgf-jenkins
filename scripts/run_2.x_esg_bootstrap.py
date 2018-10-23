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
                    help="version, for ex: '2.6/7'")
parser.add_argument("-m", "--mirror", required=True, default='aims',
                    help="mirror url, 'fr' or 'aims'")

args = parser.parse_args()
dist = args.dist
version = args.version
mirror = args.mirror

# get esg-bootstrap

if mirror == 'fr':
    base_url = "http://distrib-coffee.ipsl.jussieu.fr/pub/esgf/dist"
elif mirror == 'aims':
    base_url = "https://aims1.llnl.gov/esgf/dist"

bin_dir = "/usr/local/bin"
bootstrap_filename = "esg-bootstrap"

if dist == 'devel':
    url = "{b}/devel/{v}/esgf-installer/{f}".format(b=base_url,
                                                    v=version, 
                                                    f=bootstrap_filename)
else:
    url = "{b}/{v}/esgf-installer/{f}".format(b=base_url,
                                              v=version,
                                              f=bootstrap_filename)

if dist == 'devel':
    bootstrap_cmd = "sudo ./{f} --devel".format(f=bootstrap_filename)
else:
    bootstrap_cmd = "sudo ./{f}".format(f=bootstrap_filename)

cmds = ["sudo wget {u} --no-check-certificate".format(u=url),
        "sudo chmod 555 {f}".format(f=bootstrap_filename),
        bootstrap_cmd]

for cmd in cmds:
    status = run_cmd(cmd, True, False, True, bin_dir)
    if status != SUCCESS:
        sys.exit(status)

sys.exit(SUCCESS)

