import logging
import os
import os.path
import shutil
import stat
import subprocess
import time
import zipfile
from collections import defaultdict
from enum import Enum

import pandas as pd
import psutil
import requests

from icasamanager import config


def install():
    create_local_base_dir()
    download()
    unzip()
    make_executable()


def create_local_base_dir():
    if not os.path.isdir(config.local_base_dir):
        os.mkdir(config.local_base_dir)


def download():
    target_file = ''.join([config.local_base_dir, config.download_file])

    if os.path.isfile(target_file):
        return

    response = requests.get(''.join([config.download_path, config.download_file]), allow_redirects=True)
    open(target_file, 'wb').write(response.content)

    print('iCasa simulator downloaded to {0}'.format(target_file))


def unzip():
    if os.path.isdir(config.simulator_path):
        return

    archive = zipfile.ZipFile(config.archive_file)

    for file in archive.namelist():
        if file.startswith(config.simulator_dir):
            archive.extract(file, config.local_base_dir)

    print('iCasa simulator installed in {0}'.format(config.simulator_path))


def make_executable():
    file_execute = config.start_simulator_script_path
    file_status = os.stat(file_execute)
    os.chmod(file_execute, file_status.st_mode | stat.S_IEXEC)

    file_execute = os.path.join(config.simulator_path, config.chameleon_script)
    file_status = os.stat(file_execute)
    os.chmod(file_execute, file_status.st_mode | stat.S_IEXEC)


def open_process():
    logging.debug('felix process open')
    config.process_pid = subprocess.Popen(['/bin/bash', os.path.abspath(config.start_simulator_script_path)],
                                          cwd=config.simulator_path,
                                          stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL).pid


def kill_process():
    if config.process_pid:
        os_process = psutil.Process(config.process_pid)

        for child_process in os_process.children(recursive=True):
            child_process.kill()

        os_process.kill()

        config.process_pid = None


def start():
    shutil.rmtree(os.path.join(config.simulator_path, config.chameleon_cache_dir), ignore_errors=True)

    open_process()

    while True:
        response = request_get(config.clock_url)

        if response:
            break

    print('iCasa simulator started')


def stop():
    logging.info('simulator stop')
    kill_process()
    shutil.rmtree(os.path.join(config.simulator_path, config.chameleon_cache_dir), ignore_errors=True)


def is_running():
    return get_current_time() is not None


def start_script(script_name):
    send_gogo_command(Command.reset_context.value)
    response = send_gogo_command(Command.execute_script.value, script_name)

    while True:
        if response and response.status_code == 200 and 'Executing script' in str(response.content):
            break
        else:
            time.sleep(1)
            response = send_gogo_command(Command.execute_script.value, script_name)


def get_system_state():
    system_state_json = json_request(config.state_url)
    data_columns = [device['name'] + '_' + device_property['name'] for device in system_state_json
                    for device_property in device['properties']]
    data_values = [device_property['value'] for device in system_state_json for device_property in
                   device['properties']]
    data = pd.Series(data_values, index=data_columns, name=get_current_time())

    return data


def get_current_time():
    json_response = json_request(config.clock_url)

    if json_response is None:
        return None

    return int(json_response['currentTime'])


def get_current_time_factor():
    json_response = json_request(config.clock_url)

    if json_response is None:
        return None

    return int(json_response['factor'])


def send_gogo_command(command, *parameter_list):
    url = get_shell_command_url(command)

    parameters_dict = defaultdict(list)
    parameters_dict['parameters'] = parameter_list

    return request_post(url, parameters_dict)


def get_shell_command_url(command):
    return config.shell_execute_url + command


def json_request(url):
    response = request_get(url)

    if response:
        return response.json()
    else:
        return None


def request_get(url):
    try:
        response = requests.get(url, timeout=1)

        if response and response.ok:
            return response
        else:
            return None

    except requests.exceptions.RequestException as error:
        logging.info('waiting for simulator to start...')
        time.sleep(1)
        return None
    except:
        import sys
        print("Unknown exception:", sys.exc_info()[0])
        return None


def request_post(url, parameters):
    try:
        response = requests.post(url, json=parameters)

        if response and response.ok:
            return response
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def admin_json_request(url):
    id_data = {
        'username': 'admin',
        'password': 'admin'
    }

    with requests.Session() as session:
        session.post(config.login_url, data=id_data)
        response = session.get(url)

        if response.status_code == 200:
            return response.json()


class Command(Enum):
    execute_script = 'execute-script'
    reset_context = 'reset-context'
    create_device = 'create-device'
    move_device_zone = 'move-device-zone'
    set_device_property = 'set-device-property'
    modify_zone_variable = 'modify-zone-variable'
    attach_zone_device = 'attach-zone-device'
    show_zones = 'show-zones'
    move_person_zone = 'move-person-zone'
