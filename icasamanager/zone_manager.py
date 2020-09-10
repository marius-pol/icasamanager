from enum import Enum

from icasamanager import simulator_manager
from icasamanager.simulator_manager import Command


def set_temperature(zone, value):
    modify_zone_variable(zone, ZoneVariable.temperature.value, value)


def set_illuminance(zone, value):
    modify_zone_variable(zone, ZoneVariable.illuminance.value, value)


def set_power(zone, value):
    modify_zone_variable(zone, ZoneVariable.power.value, value)


def move_person_zone(person, zone):
    simulator_manager.send_gogo_command(Command.move_person_zone.value, person, zone)


def modify_zone_variable(zone, variable, value):
    simulator_manager.send_gogo_command(Command.modify_zone_variable.value, zone, variable.capitalize(), value)


class ZoneVariable(Enum):
    temperature = 'Temperature'
    illuminance = 'Illuminance'
    power = 'Electricity'
