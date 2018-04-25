import sys
import os
import argparse
import re

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *
from vm_util import *

parser = argparse.ArgumentParser(description="prepare a virtual machine",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-H", "--vm_host", help="vm_host", required=True)
parser.add_argument("-x", "--vmx", help="full path vmx file name", required=True)

args = parser.parse_args()

vm_host = args.vm_host
vmx = args.vmx

# stop vm if running
ret_code = stop_vm_if_running(vm_host, vmx)
sys.exit(ret_code)

