import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

parser = argparse.ArgumentParser(description="install esgf 2.x",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-d", "--dist", required=True, choices=['master', 'devel'],
                    help="distribution, 'devel' or 'master'")
parser.add_argument("-v", "--version", required=True,
                    help="distribution, 'devel' or 'master'")
parser.add_argument("-w", "--workdir", help="work directory")

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
if status != SUCCESS:
    sys.exit(status)

cmd = "hostname -s"
status, cmd_output = run_cmd_capture_output(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

this_host = cmd_output[0].rstrip()
dest_file = "/usr/local/etc/esg-autoinstall.conf"
cmd = "sudo cp {w}/repos/esgf-jenkins/configs/esg-autoinstall.conf.{h} {d}".format(w=workdir,
                                                                                   h=this_host,
                                                                                   d=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)


cmd = "sudo script -c '/usr/local/bin/esg-autoinstall' installation.log"
status = run_cmd(cmd, True, False, workdir)
if status != SUCCESS:
    sys.exit(status)

cmd = "grep 'Node installation is complete.' {w}/installation.log".format(w=workdir)
status = run_cmd(cmd, True, False, workdir)

sys.exit(status)

