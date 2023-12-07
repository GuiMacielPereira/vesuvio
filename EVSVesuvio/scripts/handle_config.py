import os
from shutil import copyfile, copytree, ignore_patterns

VESUVIO_CONFIG_PATH = os.path.join(os.path.expanduser("~"), '.mvesuvio')
VESUVIO_CONFIG_FILE = "vesuvio.user.properties"
VESUVIO_INPUTS_FILE = "analysis_inputs.py"
VESUVIO_PACKAGE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANTID_CONFIG_FILE = "Mantid.user.properties"
VESUVIO_IPFOLDER_PATH = os.path.join(VESUVIO_CONFIG_PATH, "ip_files")


def setup_default_config():
    success = __mk_dir('config', VESUVIO_CONFIG_PATH)
    if success:
        copytree(os.path.join(VESUVIO_PACKAGE_PATH, "config", "ip_files"), VESUVIO_IPFOLDER_PATH, ignore=ignore_patterns('__*'))
        set_expr_dir(VESUVIO_CONFIG_PATH, "default")

        copyfile(os.path.join(VESUVIO_PACKAGE_PATH, "config", VESUVIO_CONFIG_FILE), os.path.join(VESUVIO_CONFIG_PATH, VESUVIO_CONFIG_FILE))
        copyfile(os.path.join(VESUVIO_PACKAGE_PATH, "config", MANTID_CONFIG_FILE), os.path.join(VESUVIO_CONFIG_PATH, MANTID_CONFIG_FILE))

        set_config_vars({'caching.location': VESUVIO_CONFIG_PATH,
                         'caching.experiment': "default",
                         'caching.ipfolder': VESUVIO_IPFOLDER_PATH}, verbose=False)


def set_expr_dir(cache_dir, experiment):
    expr_path = os.path.join(cache_dir, "experiments", experiment)
    success = __mk_dir('experiment', expr_path)
    if success:
        copyfile(os.path.join(VESUVIO_PACKAGE_PATH, "config", VESUVIO_INPUTS_FILE),
                 os.path.join(cache_dir, "experiments", experiment, VESUVIO_INPUTS_FILE))


def __mk_dir(type, path):
    success = False
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
            success = True
        except:
            print(f'Unable to make {type} directory at location: {path}')
    return success


def set_config_vars(var_dict, verbose=True):
    file_path = os.path.join(VESUVIO_CONFIG_PATH, VESUVIO_CONFIG_FILE)
    lines = __read_config(file_path)

    updated_lines = []
    for line in lines:
        match = False
        for var in var_dict:
            if line.startswith(var):
                new_line = f'{var}={var_dict[var]}'
                updated_lines.append(f'{new_line}\n')
                match = True
                if verbose:
                    print(f'Setting: {new_line}')
                break

        if not match:
            updated_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)


def read_config_var(var, throw_on_not_found=True):
    file_path = f'{VESUVIO_CONFIG_PATH}/{VESUVIO_CONFIG_FILE}'
    lines = __read_config(file_path, throw_on_not_found)

    result = ""
    for line in lines:
        if line.startswith(var):
            result = line.split("=", 2)[1].strip('\n')
            break
    if not result and throw_on_not_found:
        raise ValueError(f'{var} was not found in the vesuvio config')
    return result


def __read_config(config_file_path, throw_on_not_found=True):
    lines = ""
    try:
        with open(config_file_path, 'r') as file:
            lines = file.readlines()
    except IOError:
        if throw_on_not_found:
            raise RuntimeError(f"Could not read from vesuvio config file: {config_file_path}")
    return lines


def config_set():
    if read_config_var('caching.location', False):
        return True
    else:
        return False


def check_dir_exists(type, path):
    if not os.path.isdir(path):
        print(f"Directory of {type} could not be found at location: {path}")
        return False
    return True
