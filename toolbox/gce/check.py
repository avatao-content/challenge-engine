import logging
import os
import re
from glob import glob

from toolbox.config.gce import CONFIG_KEYS, CRP_CONFIG_KEYS, MAX_CPU_CORES
from toolbox.utils import check_common_files, counted_error, validate_bool, validate_flag, validate_ports


# pylint: disable=too-many-branches
def check_config(config: dict):
    invalid_keys = set(config.keys()) - set(CONFIG_KEYS)
    if invalid_keys:
        counted_error('Invalid key(s) found in config.yml: %s', invalid_keys)

    if not isinstance(config.get('crp_config'), dict):
        counted_error('config.yml:crp_config must a dictionary.')

    invalid_keys = set(config['crp_config'].keys()) - set(CRP_CONFIG_KEYS)
    if invalid_keys:
        counted_error('Invalid key(s) found in config.yml:crp_config: %s', invalid_keys)

    if not config['crp_config'].get('source_image_family'):
        counted_error('Missing source_image_family - e.g. debian-9')

    try:
        cpu_cores = int(config['crp_config'].get('cpu_cores', 0))
        if cpu_cores < 1 or (cpu_cores > 1 and cpu_cores % 2 != 0) or cpu_cores > MAX_CPU_CORES:
            raise ValueError
    except Exception:
        counted_error('Invalid cpu_cores value: %s. It must be 1 or an even number up to %s.',
                      config['crp_config'].get('cpu_cores'), MAX_CPU_CORES)

    else:
        # We must know the number of CPU cores.
        try:
            mem_limit_gb = float(config['crp_config'].get('mem_limit_gb', 0))
            if mem_limit_gb < 0.9 * cpu_cores or mem_limit_gb > 6.5 * cpu_cores or mem_limit_gb % 0.25 != 0:
                raise ValueError
        except Exception:
            counted_error('Invalid mem_limit value: %s. It must be between 0.9 * cpu_cores and 6.5 * cpu_cores in 0.25 increments.',
                            config['crp_config'].get('mem_limit_gb'))

    try:
        if not 10 <= int(config['crp_config'].get('storage_limit_gb', 0)) <= 100:
            raise ValueError
    except Exception:
        counted_error('Invalid storage_limit_gb value: %s. It must be between 10 and 100 GigaBytes.',
                        config['crp_config'].get('storage_limit_gb'))

    validate_bool('nested', config['crp_config'].get('nested', '0'))
    validate_bool('internet_access', config['crp_config'].get('internet_access', '0'))
    validate_ports(config['crp_config'].get('ports', []), config['crp_config'].get('buttons', None))
    validate_flag(config)


# TODO: Allow JavaScript and Go...
def check_controller(config: dict):
    is_static = bool(config.get('flag'))
    if is_static:
        if glob('controller/*'):
            counted_error('Controllers are incompatible with static flags.')

    elif not glob('controller/main.py'):
        counted_error('Missing controller/main.py')

    else:
        controller_script = open('controller/main.py', 'r').read()
        if 'def main(request' not in controller_script:
            counted_error('Missing main(request: flask.Request) from controller/main.py')

        if not glob('controller/requirements.txt'):
            logging.warning('Missing controller/requirements.txt')


def check_misc(repo_name: str):
    # This is a restriction of Google Cloud and must be followed.
    if re.match(r"^[a-z][a-z0-9-]{0,61}[a-z0-9]$", repo_name) is None:
        counted_error("Invalid repo name. Valid pattern: ^[a-z][a-z0-9-]{0,61}[a-z0-9]$")

    check_common_files()

    if not glob('setup.sh'):
        counted_error('Missing setup.sh file. Use it for what you would use a Dockerfile for.')

    if not glob('rootfs/*'):
        logging.warning('Missing or empty "rootfs" directory. Please place your source files there '
                        'if your challenge has any.')


# pylint: disable=unused-argument
def run(repo_path: str, repo_name: str, repo_branch: str, config: dict):
    os.chdir(repo_path)
    check_config(config)
    check_controller(config)
    check_misc(repo_name)
