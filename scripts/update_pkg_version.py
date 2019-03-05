import sys
import os
import argparse
import re
import tempfile
from shutil import copyfile

SUCCESS = 0
FAILURE = 1

parser = argparse.ArgumentParser(description="update package version for ansible installer to pick up",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-d", "--ansible_repo_dir", required=True, 
                    help="esgf-ansible repo directory")
parser.add_argument("-p", "--pkg", required=True, 
                    help="pkg to be updated")
parser.add_argument("-v", "--pkg_version", required=True, 
                    help="pkg version to be updated")


pkg_to_ansible_var_map = {
    "esgf-dashboard"   : "esgf_dash_board",
    #"esgf-getcert"    NEED TO BE ADDED to ansible
    "esgf-idp"         : "idp",
    "esgf-node-manager": "node_manager",
    "esgf-security"    : "security",
    "esg-orp"          : "orp",    
    "esg-search"       : "search",
    "esgf-stats-api"   : "stats_api"
}

args = parser.parse_args()
ansible_repo_dir = args.ansible_repo_dir
pkg = args.pkg
pkg_version = args.pkg_version

def update_pkg_version(file_to_update, pkg, version):
    section = None
    found = False
    temp_file = tempfile.NamedTemporaryFile()
    with open(temp_file.name, 'w') as f:
        src_f = open(file_to_update, "r")
        for line in src_f:
            if section is None:
                m = re.match(r'^versions:', line)
                if m:
                    section = 'versions'
                f.write(line)
            elif section == 'versions' and found is False:
                ansible_var_for_pkg = pkg_to_ansible_var_map[pkg]
                match_str = "^\s+{p}:\s+".format(p=ansible_var_for_pkg)
                m = re.match(match_str, line)
                if m:
                    new_line = "  {var}: {version}\n".format(var=ansible_var_for_pkg,
                                                           version=version)
                    f.write(new_line)
                    found = True
                else:
                    f.write(line)
            else:
                f.write(line)
    if found:
        print("Updating {f}".format(f=file_to_update))
        copyfile(temp_file.name, file_to_update)
        return SUCCESS
    else:
        return FAILURE
#
#
#
file_to_update = "{d}/group_vars/all.yml".format(d=ansible_repo_dir)
status = update_pkg_version(file_to_update, pkg, pkg_version)

sys.exit(status)

