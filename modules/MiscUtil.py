import os
import time

from Const import *
from Util import *

def convert_list_to_dict(var_val_pairs_list, separator):

    var_val_dict = {k.strip():v.strip() for k,v in (a_pair.split(separator) for a_pair in var_val_pairs_list) }
    for a_key in var_val_dict.keys():
        print("xxx DEBUG...{k}: {v}".format(k=a_key, v=var_val_dict[a_key]))
    return var_val_dict

def generate_copy_of_updated_file(file_to_update, var_val_pairs_list, separator, workdir):
    
    var_val_dict = convert_list_to_dict(var_val_pairs_list, separator)

    current_time = time.localtime(time.time())
    time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)
    fname = os.path.basename(file_to_update)
    temp_file_name = "{f}.{d}.txt".format(f=fname, d=time_str)
    temp_file = os.path.join(workdir, temp_file_name)

    src_f = open(file_to_update, "r")
    temp_file = open(temp_file, "w+")
    update_count = 0
    for a_line in src_f:
        if len(a_line.split(separator)) > 1:
            orig_key, orig_val = a_line.split(separator)
            if orig_key:
                src_key = orig_key.strip()
                src_val = orig_val.strip()
            else:
                continue
        
            if src_key in var_val_dict:
                temp_file.write("{key} {sep} {val}\n".format(key=src_key,
                                                           sep=separator,
                                                           val=var_val_dict[src_key]))
                update_count += 1
            else:
                temp_file.write(a_line)
         
    src_f.close()
    temp_file.close()
    if update_count == len(var_val_pairs_list):
        return temp_file
    else:
        print("FAIL...generate_copy_of_updated_file()...")
        return None


    
def update_cog_settings_conf(var_val_pairs_list, separator, workdir):
    file_to_update = '/usr/local/cog/cog_config/cog_settings.cfg.TEMP'
    var_val_pairs_list = ['USE_CAPTCHA=False']
    temp_file = generate_copy_of_updated_file(file_to_update, var_val_pairs_list, '=', workdir)
    if not temp_file:
        return FAILURE
    
    cmd = "sudo bash -c \"cp {f} {f}.backup\"".format(f=file_to_update)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        return ret_code

    cmd = "sudo bash -c \"chmod +w {f}\"".format(f=file_to_update)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        return ret_code

    cmd = "sudo bash -c \"cp {src} {dest}\"".format(src=temp_file, dest=file_to_update)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        return ret_code

    cmd = "sudo bash -c \"chmod -w {f}\"".format(f=file_to_update)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        return ret_code

    return ret_code
