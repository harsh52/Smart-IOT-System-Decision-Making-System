import paho.mqtt.client as mqtt
import json
import argparse

class HeatingSystemSimulator:
    """
    A class that simulates a heating system and responds to control messages received via MQTT.
    """

    def __init__(self, broker, port):
        """
        Initialize the HeatingSystemSimulator.

        Args:
            broker (str): The address of the MQTT broker.
            port (int): The port number of the MQTT broker.
        """
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        try:
            self.client.connect(broker, port)
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            raise

    def start(self):
        """
        Start the HeatingSystemSimulator by subscribing to the heating system control topic and starting the MQTT loop.
        """
        try:
            self.client.subscribe("heating_system/+/control")
            self.client.loop_forever()
        except Exception as e:
            print(f"Error starting the HeatingSystemSimulator: {e}")
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

            if topic[2] == "control":
                if payload["action"] == "turn_on":
                    print(f"Heating system for user {user_id} turned on")
                elif payload["action"] == "turn_off":
                    print(f"Heating system for user {user_id} turned off")
        except Exception as e:
            print(f"Error handling MQTT message: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heating System Simulation")
    parser.add_argument("-b", "--broker", required=True, help="MQTT broker address")
    parser.add_argument("-p", "--port", type=int, default=1883, help="MQTT broker port (default: 1883)")

    args = parser.parse_args()

    try:
        # Create and start the HeatingSystemSimulator
        simulator = HeatingSystemSimulator(args.broker, args.port)
        simulator.start()
    except Exception as e:
        print(f"Error running HeatingSystemSimulator: {e}")