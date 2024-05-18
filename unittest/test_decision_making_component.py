import unittest
from unittest.mock import patch, MagicMock, call
from decision_making_component import DecisionMakingComponent, FIRST_SAMPLES_COUNT, OUTLIER_THRESHOLD
from collections import deque
import json


class TestDecisionMakingComponent(unittest.TestCase):
    @patch('paho.mqtt.client.Client')
    def setUp(self, MockClient):
        self.mock_mqtt_client = MockClient.return_value
        self.broker = 'test_broker'
        self.port = 1883
        self.threshold = 22.0
        self.component = DecisionMakingComponent(self.broker, self.port, self.threshold)
        self.component.client = self.mock_mqtt_client

    def test_mqtt_connection(self):
        self.mock_mqtt_client.connect.assert_called_with(self.broker, self.port)

    def test_start(self):
        self.component.start()
        self.mock_mqtt_client.subscribe.assert_called_with("temperature_meter/+")
        self.mock_mqtt_client.loop_forever.assert_called_once()

    def test_on_message(self):
        user_id = 'user1'
        topic = f'temperature_meter/{user_id}'
        temperature = 25.0
        payload = json.dumps({"temperature": temperature}).encode()
        msg = MagicMock(topic=topic, payload=payload)

        self.component.on_message(None, None, msg)
        self.assertIn(user_id, self.component.temperatures)
        self.assertEqual(self.component.temperatures[user_id][-1], temperature)

    def test_handle_temperature(self):
        user_id = 'user1'
        temperatures = [20.0 + i for i in range(FIRST_SAMPLES_COUNT)]
        for temp in temperatures:
            self.component.handle_temperature(user_id, temp)
        self.assertEqual(len(self.component.temperatures[user_id]), FIRST_SAMPLES_COUNT)
        self.assertEqual(self.component.temperatures[user_id][-1], temperatures[-1])

    def test_detect_outlier(self):
        samples = deque([20.0 + i for i in range(FIRST_SAMPLES_COUNT)], maxlen=FIRST_SAMPLES_COUNT)
        self.assertFalse(self.component.detect_outlier(samples, 25.0))


if __name__ == '__main__':
    unittest.main()
