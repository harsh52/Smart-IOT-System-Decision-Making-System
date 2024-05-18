import argparse
import paho.mqtt.client as mqtt
from statistics import mean, stdev
from collections import deque
import json

# Constants
FIRST_SAMPLES_COUNT = 100
OUTLIER_THRESHOLD = 3

class DecisionMakingComponent:
    """
    A class that implements a decision-making component for a smart heating system.
    """

    def __init__(self, broker, port, threshold):
        """
        Initialize the DecisionMakingComponent.

        Args:
            broker (str): The address of the MQTT broker.
            port (int): The port number of the MQTT broker.
            threshold (float): The temperature threshold in degrees Celsius.
        """
        try:
            self.client = mqtt.Client()
            self.client.on_message = self.on_message
            self.client.connect(broker, port)
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            raise

        self.threshold = threshold
        self.temperatures = {}
        self.heating_systems = {}

    def start(self):
        """
        Start the DecisionMakingComponent by subscribing to the temperature meter topic and starting the MQTT loop.
        """
        try:
            self.client.subscribe("temperature_meter/+")
            self.client.loop_forever()
        except Exception as e:
            print(f"Error starting the DecisionMakingComponent: {e}")
            raise

    def on_message(self, client, userdata, msg):
        """
        Callback function called when an MQTT message is received.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata (any): User-defined data passed to the callback function.
            msg (mqtt.MQTTMessage): The received MQTT message.
        """
        try:
            topic = msg.topic.split("/")
            user_id = topic[1]
            payload = json.loads(msg.payload.decode())

            if topic[0] == "temperature_meter":
                temperature = payload["temperature"]
                self.handle_temperature(user_id, temperature)
        except Exception as e:
            print(f"Error handling MQTT message: {e}")

    def handle_temperature(self, user_id, temperature):
        """
        Handle a temperature reading received from the temperature meter.

        Args:
            user_id (str): The ID of the user associated with the temperature reading.
            temperature (float): The temperature reading.
        """
        try:
            if user_id not in self.temperatures:
                self.temperatures[user_id] = deque(maxlen=FIRST_SAMPLES_COUNT)
                self.heating_systems[user_id] = False

            self.temperatures[user_id].append(temperature)

            if len(self.temperatures[user_id]) < FIRST_SAMPLES_COUNT:
                return

            is_outlier = self.detect_outlier(self.temperatures[user_id], temperature)
            if is_outlier:
                return

            avg_temp = mean(self.temperatures[user_id])
            self.control_heating_system(user_id, avg_temp)
        except Exception as e:
            print(f"Error handling temperature reading: {e}")

    def detect_outlier(self, samples, value):
        """
        Detect if a temperature reading is an outlier using the Z-score algorithm.

        Args:
            samples (deque): The deque containing the last FIRST_SAMPLES_COUNT temperature readings.
            value (float): The temperature reading to check for an outlier.

        Returns:
            bool: True if the temperature reading is an outlier, False otherwise.
        """
        try:
            if len(samples) < FIRST_SAMPLES_COUNT:
                return False

            avg = mean(samples)
            std_dev = stdev(samples)
            z_score = (value - avg) / std_dev

            if abs(z_score) > OUTLIER_THRESHOLD:
                return True

            return False
        except Exception as e:
            print(f"Error detecting outlier: {e}")
            return False

    def control_heating_system(self, user_id, avg_temp):
        """
        Control the heating system based on the average temperature for the user.

        Args:
            user_id (str): The ID of the user associated with the heating system.
            avg_temp (float): The average temperature for the user.
        """
        try:
            if avg_temp < self.threshold and not self.heating_systems[user_id]:
                payload = json.dumps({"action": "turn_on"})
                self.client.publish(f"heating_system/{user_id}/control", payload)
                print(f'sent signal to heating device to turn on for user id: {user_id}')
                self.heating_systems[user_id] = True
            elif avg_temp >= self.threshold and self.heating_systems[user_id]:
                payload = json.dumps({"action": "turn_off"})
                self.client.publish(f"heating_system/{user_id}/control", payload)
                print(f'sent signal to heating device to turn off for user id: {user_id}')
                self.heating_systems[user_id] = False
        except Exception as e:
            print(f"Error controlling heating system: {e}")

if __name__ == "__main__":
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-b", "--broker", required=True, help="MQTT broker address")
        parser.add_argument("-p", "--port", type=int, default=1883, help="MQTT broker port")
        parser.add_argument("-t", "--threshold", type=float, required=True, help="Temperature threshold in degrees Celsius")
        args = parser.parse_args()

        # Create and start the DecisionMakingComponent
        decision_making_component = DecisionMakingComponent(args.broker, args.port, args.threshold)
        decision_making_component.start()
    except Exception as e:
        print(f"Error running DecisionMakingComponent: {e}")