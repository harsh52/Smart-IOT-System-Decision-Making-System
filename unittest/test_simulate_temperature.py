import unittest
from unittest.mock import patch, MagicMock
import json
import random
from simulate_temperature import TemperatureMeterSimulator


class TestTemperatureMeterSimulator(unittest.TestCase):
    @patch('paho.mqtt.client.Client')
    def setUp(self, MockClient):
        self.mock_mqtt_client = MockClient.return_value
        self.broker = 'test_broker'
        self.port = 1883
        self.user_ids = ['user1']
        self.simulator = TemperatureMeterSimulator(self.broker, self.port, self.user_ids)
        self.simulator.client = self.mock_mqtt_client

    def test_mqtt_connection(self):
        self.mock_mqtt_client.connect.assert_called_with(self.broker, self.port)

    @patch('simulate_temperature.TemperatureMeterSimulator.simulate_temperature')
    def test_start(self, mock_simulate_temperature):
        self.simulator.start()
        mock_simulate_temperature.assert_called_once()


if __name__ == '__main__':
    unittest.main()
