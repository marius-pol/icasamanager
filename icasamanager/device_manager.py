import numpy

from icasamanager import simulator_manager, config
from icasamanager.simulator_manager import Command


def get_active_devices():
    state_json = simulator_manager.json_request(config.state_url)
    devices = [device['name'] for device in state_json]

    return devices


def get_device_types():
    device_types = simulator_manager.json_request(config.device_types_url)

    if device_types is None:
        return None

    return [device_type['name'] for device_type in device_types]


def get_devices_in_zone(zone):
    state_json = simulator_manager.json_request(config.state_url)
    devices = [device['name'] for device in state_json if device['location'] == zone]

    return devices


def create_device_in_zone(zone, device_type, device_id):
    if exists_device_in_zone(zone, device_id):
        return

    simulator_manager.send_gogo_command(Command.create_device.value, device_id, device_type)
    simulator_manager.send_gogo_command(Command.move_device_zone.value, device_id, zone)


def exists_device_in_zone(zone, device_id):
    state = simulator_manager.json_request(config.state_url)
    device_exists = [device['name'] for device in state if device['name'] == device_id and device['location'] == zone]

    return len(device_exists) > 0


def create_available_device_types(zone):
    device_types = get_device_types()

    for device in device_types:
        simulator_manager.send_gogo_command(Command.create_device.value, device + '-' + zone.capitalize(), device)
        simulator_manager.send_gogo_command(Command.move_device_zone.value, device + '-' + zone.capitalize(), zone)


def set_device_property(device_id, device_property, value):
    if type(value) is bool:
        simulator_manager.send_gogo_command(Command.set_device_property.value, device_id, device_property, value,
                                            'Boolean')
    if type(value) is numpy.int64:
        simulator_manager.send_gogo_command(Command.set_device_property.value, device_id, device_property, int(value))
    else:
        simulator_manager.send_gogo_command(Command.set_device_property.value, device_id, device_property, value)
