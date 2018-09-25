import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *
from MiscUtil import *
from Util2x import update_auto_keypair
parser = argparse.ArgumentParser(description="run esgf 2.x post install steps",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-H", "--vm_jenkins_home", required=True, help="vm user jenkins home directory")

args = parser.parse_args()
workdir = args.vm_jenkins_home

sys.stdout.flush()

#
# run this on vm node as user 'jenkins'
#


#
# update /usr/local/cog/cog_config/cog_settings.cfg
#
print("xxx DEBUG...going to update cog_settings.cfg to set USE_CAPTCHA to False")
file_to_update = '/usr/local/cog/cog_config/cog_settings.cfg'
var_val_pairs_list = ['USE_CAPTCHA=False']
status = update_cog_settings_conf(var_val_pairs_list, '=', workdir)

add_path = "export PATH={}/miniconda2/bin:/sbin:/usr/sbin:$PATH".format(workdir)
activate = "source /usr/local/conda/bin/activate esgf-pub"
cd_cmd = "cd {}/repos/esgf-installer".format(workdir)
stop = "python esg_node.py --stop"
start = "python esg_node.py --start"
deactivate = "source deactivate"

conda_path = "{jenkins_home}/miniconda2/bin"
env = "esgf-pub"
cmds = "{add}; {act}; {cd}; {stop}; sleep 5; {start}; sleep 10; {d}".format(add = add_path,
                                                                            act=activate,
                                                                            cd=cd_cmd,
                                                                            stop=stop,
                                                                            start=start,
                                                                            d=deactivate)
cmd = "sudo -E bash -c \"{the_cmds}\"".format(the_cmds=cmds)
os.system(cmd)

sys.exit(status)

