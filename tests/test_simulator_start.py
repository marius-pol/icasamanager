import os
from unittest import TestCase

from icasamanager import config, simulator_manager


class TestSimulatorStart(TestCase):
    def test_simulator_start(self):
        os.chdir('..')
        simulator_manager.install()

        simulator_manager.start()
        simulator_manager.start_script(config.script_house_lights)

        assert simulator_manager.is_running()

        simulator_manager.stop()
