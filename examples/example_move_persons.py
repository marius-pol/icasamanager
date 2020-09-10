import random
import time
from enum import Enum

from icasamanager import config, simulator_manager, zone_manager


class Zone(Enum):
    out = 'out'
    bathroom = 'bathroom'
    bedroom = 'bedroom'
    hall = 'hall'
    kitchen = 'kitchen'
    livingroom = 'livingroom'


class Person(Enum):
    marie = 'Marie'
    paul = 'Paul'


if __name__ == '__main__':
    simulator_manager.install()

    simulator_manager.start()
    simulator_manager.start_script(config.script_house_lights)

    for x in range(0, 30):
        zone = random.choice(list(Zone)).value
        person = random.choice(list(Person)).value

        zone_manager.move_person_zone(person, zone)
        print('iCasa - moved {0} in {1}'.format(person, zone))

        time.sleep(1)

    simulator_manager.stop()
