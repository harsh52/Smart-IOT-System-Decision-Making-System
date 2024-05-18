import unittest
from unittest.mock import patch, MagicMock
from simulate_heating_system import HeatingSystemSimulator
import json

class TestHeatingSystemSimulator(unittest.TestCase):
    @patch('paho.mqtt.client.Client')
    def setUp(self, MockClient):
        self.mock_mqtt_client = MockClient.return_value
        self.broker = 'test_broker'
        self.port = 1883
        self.simulator = HeatingSystemSimulator(self.broker, self.port)
        self.simulator.client = self.mock_mqtt_client

    def test_mqtt_connection(self):
        self.mock_mqtt_client.connect.assert_called_with(self.broker, self.port)

    def test_start(self):
        self.simulator.start()
        self.mock_mqtt_client.subscribe.assert_called_with("heating_system/+/control")
        self.mock_mqtt_client.loop_forever.assert_called_once()

    def test_on_message_turn_on(self):
        user_id = 'user1'
        topic = f'heating_system/{user_id}/control'
        payload = json.dumps({"action": "turn_on"}).encode()
        msg = MagicMock(topic=topic, payload=payload)

        with patch('builtins.print') as mock_print:
            self.simulator.on_message(None, None, msg)
            mock_print.assert_called_with(f"Heating system for user {user_id} turned on")

    def test_on_message_turn_off(self):
        user_id = 'user1'
        topic = f'heating_system/{user_id}/control'
        payload = json.dumps({"action": "turn_off"}).encode()
        msg = MagicMock(topic=topic, payload=payload)

        with patch('builtins.print') as mock_print:
            self.simulator.on_message(None, None, msg)
            mock_print.assert_called_with(f"Heating system for user {user_id} turned off")

    def test_on_message_invalid_action(self):
        user_id = 'user1'
        topic = f'heating_system/{user_id}/control'
        payload = json.dumps({"action": "invalid"}).encode()
        msg = MagicMock(topic=topic, payload=payload)

        with patch('builtins.print') as mock_print:
            self.simulator.on_message(None, None, msg)
            mock_print.assert_not_called()

    def test_on_message_invalid_json(self):
        user_id = 'user1'
        topic = f'heating_system/{user_id}/control'
        payload = b'invalid_json'
        msg = MagicMock(topic=topic, payload=payload)

        with patch('builtins.print') as mock_print:
            self.simulator.on_message(None, None, msg)
            mock_print.assert_called_with('Error handling MQTT message: Expecting value: line 1 column 1 (char 0)')

if __name__ == '__main__':
    unittest.main()
