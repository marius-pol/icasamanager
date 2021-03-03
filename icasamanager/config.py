import os

download_path = 'http://adeleresearchgroup.github.io/iCasa/snapshot/distributions/'
download_file = 'icasa.teaching.distribution.with.apps-1.2.7-SNAPSHOT.zip'
local_base_dir = 'ext/'
simulator_dir = 'icasa.teaching.distribution.with.apps/'
chameleon_cache_dir = 'chameleon-cache/'
simulator_path = os.path.join(local_base_dir, simulator_dir)
archive_file = os.path.join(local_base_dir, download_file)

start_simulator_script = 'startGateway.sh'
chameleon_script = 'chameleon.sh'
script_house_lights = 'SetupHouseWithLights.bhv'
start_simulator_script_path = os.path.join(simulator_path, start_simulator_script)

port = 9000  # set in icasa_path/conf/application.conf, with line http.port = 9000 (default value)
process_pid = None

clock_url = 'http://localhost:{0}/icasa/clocks/clock/default'.format(port)
login_url = 'http://localhost:{0}/monitor/login'.format(port)
instances_url = 'http://localhost:{0}/monitor/ipojo.json'.format(port)
device_types_url = 'http://localhost:{0}/icasa/devices/deviceTypes'.format(port)
shell_execute_url = 'http://localhost:{0}/icasa/shell/execute/'.format(port)
state_url = 'http://localhost:{0}/icasa/devices/devices'.format(port)
