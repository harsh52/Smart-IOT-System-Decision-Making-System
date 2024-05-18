import paho.mqtt.client as mqtt
import time
import json
import random
import argparse

class TemperatureMeterSimulator:
    """
    A class that simulates a temperature meter and publishes temperature readings to an MQTT broker.
    """

    def __init__(self, broker, port, user_ids):
        """
        Initialize the TemperatureMeterSimulator.

        Args:
            broker (str): The address of the MQTT broker.
            port (int): The port number of the MQTT broker.
            user_ids (list): A list of user IDs to simulate temperature readings for.
        """
        self.client = mqtt.Client()
        try:
            self.client.connect(broker, port)
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            raise
        self.user_ids = user_ids
        self.topic = "temperature_meter/{}"

    def start(self):
        """
        Start the TemperatureMeterSimulator by simulating temperature readings.
        """
        try:
            self.simulate_temperature()
        except Exception as e:
            print(f"Error simulating temperature readings: {e}")
            raise

    def simulate_temperature(self):
        """
        Simulate temperature readings by publishing random temperatures to the MQTT broker.
        """
        while True:
            for user_id in self.user_ids:
                temperature = random.uniform(10, 30)
                message = json.dumps({"temperature": temperature})
                try:
                    self.client.publish(self.topic.format(user_id), message)
                    print(f"Published {message} to {self.topic.format(user_id)}")
                except Exception as e:
                    print(f"Error publishing temperature reading: {e}")
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temperature Simulation")
    parser.add_argument("-b", "--broker", required=True, help="MQTT broker address")
    parser.add_argument("-p", "--port", type=int, default=1883, help="MQTT broker port (default: 1883)")

    args = parser.parse_args()

    try:
        # User IDs to simulate multiple devices
        user_ids = ["user1", "user2", "user3"]

        # Create and start the TemperatureMeterSimulator
        simulator = TemperatureMeterSimulator(args.broker, args.port, user_ids)
        simulator.start()
    except Exception as e:
        print(f"Error running TemperatureMeterSimulator: {e}")