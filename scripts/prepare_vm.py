import sys
import os
import argparse
import re

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="prepare a virtual machine",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-H", "--vm_host", help="vm_host", required=True)
parser.add_argument("-x", "--vmx", help="full path vmx file name", required=True)
parser.add_argument("-s", "--snapshot", help="vm snapshot to use", required=True)
parser.add_argument("-n", "--vm_node", help="vm node", required=True)
args = parser.parse_args()

vm_host = args.vm_host
vmx = args.vmx
vm_snapshot = args.snapshot
vm_node = args.vm_node

def check_num_of_vm_running(vm_host):

    # check if vm is running
    cmd = "ssh jenkins@{h} \"vmrun list\"".format(h=vm_host)
    ret_code, output = run_cmd_capture_output(cmd, True, False, True)

    n_running_vm = 0
    for a_line in output:
        m = re.match(r'Total\s+running\s+VMs:\s+(\d+)', a_line)
        if m:
            n_running_vm = m.group(1)

    return(ret_code, n_running_vm)


def stop_vm_if_running(vm_host, vmx):

    ret_code, n_running_vm = check_num_of_vm_running(vm_host)
    if ret_code != SUCCESS:
        return ret_code

    if n_running_vm == '1':
        print("vm is running... shutting it down")
        cmd = "ssh jenkins@{h} \"vmrun stop {vmx}\"".format(h=vm_host,
                                                            vmx=vmx)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{cmd}".format(cmd=cmd))
            return ret_code

        ret_code, n_running_vm = check_num_of_vm_running(vm_host)                
        print("number of running vm now: " + n_running_vm)

    return ret_code

def revert_vm_to_snapshot(vm_host, vmx, vm_snapshot):

    cmd = "ssh jenkins@{h} \"vmrun revertToSnapshot {vmx} {s}\"".format(h=vm_host,
                                                                        vmx=vmx,
                                                                        s=vm_snapshot)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))

    return ret_code
    

def start_vm(vm_host, vmx):
    cmd = "ssh jenkins@{h} \"vmrun start {vmx} nogui\"".format(h=vm_host,
                                                               vmx=vmx)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))
        return ret_code

    ret_code, n_running_vm = check_num_of_vm_running(vm_host)                
    print("number of running vm now: " + n_running_vm)
    return(ret_code)

def get_vm_ready(vm_node):
    cmd = "ssh jenkins@{n} \"sudo ntpdate -u 0.centos.pool.ntp.org\"".format(n=vm_node)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))

    cmd = "ssh jenkins@{n} \"date\"".format(n=vm_node)
    run_cmd(cmd, True, False, True)

    return ret_code


# stop vm if running
ret_code = stop_vm_if_running(vm_host, vmx)
if ret_code != SUCCESS:
    sys.exit(ret_code)

# revert vm to snapshot and start it
ret_code = revert_vm_to_snapshot(vm_host, vmx, vm_snapshot)
if ret_code != SUCCESS:
    sys.exit(ret_code)

ret_code = start_vm(vm_host, vmx)
if ret_code != SUCCESS:
    sys.exit(ret_code)

ret_code = get_vm_ready(vm_node)
sys.exit(ret_code)

