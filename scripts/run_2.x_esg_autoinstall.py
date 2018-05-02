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
parser.add_argument("-w", "--workdir", help="work directory")

args = parser.parse_args()
dist = args.dist
version = args.version
workdir = args.workdir

sys.stdout.flush()

cmd = "hostname -s"
status, cmd_output = run_cmd_capture_output(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

this_host = cmd_output[0].rstrip()
dest_file = "/usr/local/etc/esg-autoinstall.conf"

#cmd = "sudo mv {d} {d}.ORIG".format(d=dest_file)
cmd = "mv {d} {d}.ORIG".format(d=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

#cmd = "sudo cp {w}/repos/esgf-jenkins/configs/esg-autoinstall.conf.{h} {d}".format(w=workdir,
#                                                                                   h=this_host,
#                                                                                   d=dest_file)
cmd = "cp {w}/repos/esgf-jenkins/configs/esg-autoinstall.conf.{h} {d}".format(w=workdir,
                                                                              h=this_host,
                                                                              d=dest_file)
status = run_cmd(cmd, True, False, True)
if status != SUCCESS:
    sys.exit(status)

#cmd = "sudo script -c '/usr/local/bin/esg-autoinstall' {w}/installation.log".format(w=workdir)
#cmd = "sudo -- sh -c 'export TERM=vt100; /usr/local/bin/esg-autoinstall'"
#cmd = "sudo bash -c 'export TERM=vt100; script -c /usr/local/bin/esg-autoinstall installation.log"
###cmd = "sudo bash -c 'export TERM=vt100; /usr/local/bin/esg-autoinstall installation.log"

#cmd = "sudo -- sh -c 'export TERM=vt100; /usr/local/bin/esg-autoinstall'"
#cmd = "bash -c 'export TERM=vt100; /usr/local/bin/esg-autoinstall'"

sys.stdout.flush()
os.environ["TERM"] = "vt100"
cmd = "/usr/local/bin/esg-autoinstall"

#status = run_cmd(cmd, True, False, True)
status = run_cmd(cmd, True, True, True)
if status != SUCCESS:
    sys.exit(status)

sys.stdout.flush()

cmd = "grep 'Node installation is complete.' {w}/installation.log".format(w=workdir)
status = run_cmd(cmd, True, False, True)

# touch a file
cmd = "touch {w}/esg-autoinstall.COMPLETE".format(w=workdir)
status1 = run_cmd(cmd, True, True, True)
sys.stdout.flush()
print("xxx...exiting from run_2.x_esg_autoinstall.py...")
sys.exit(status)

