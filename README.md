# Smart-IOT-System-Decision-Making-System

# Smart Heating System Simulation

This project control heating system using MQTT for communication between different components. The system consists of three main components:
1. **DecisionMakingComponent**: Manages temperature readings and controls heating systems based on a threshold and logic.
2. **HeatingSystemSimulator**: Simulates a heating system, responding to control messages.
3. **TemperatureMeterSimulator**: Simulates temperature meters, publishing temperature readings for multiple users.

## Components

### DecisionMakingComponent

This component subscribes to temperature readings from various users, processes these readings, and controls the heating systems based on a specified temperature threshold.

#### Usage

```bash
python decision_making_component.py -b <broker_address> -p <port> -t <temperature_threshold>
```

- `broker_address`: The address of the MQTT broker.
- `port`: The port number of the MQTT broker (default: 1883).
- `temperature_threshold`: The temperature threshold in degrees Celsius for controlling the heating system.

#### Example

```bash
python decision_making_component.py -b mqtt.eclipseprojects.io -p 1883 -t 20
```

### HeatingSystemSimulator

This component simulates a heating system, subscribing to control messages and logging actions (turn on/off) for specific users.

#### Usage

```bash
python simulate_heating_system.py -b <broker_address> -p <port>
```

- `broker_address`: The address of the MQTT broker.
- `port`: The port number of the MQTT broker (default: 1883).

#### Example

```bash
python simulate_heating_system.py -b  mqtt.eclipseprojects.io -p 1883
```

### TemperatureMeterSimulator

This component simulates temperature meters for multiple users, publishing random temperature readings to the MQTT broker.

#### Usage

```bash
python simulate_temperature.py -b <broker_address> -p <port>
```

- `broker_address`: The address of the MQTT broker.
- `port`: The port number of the MQTT broker (default: 1883).

#### Example

```bash
python simulate_temperature.py -b mqtt.eclipseprojects.io -p 1883
```

## Installation

Ensure you have Python 3 installed. Then, install the required packages using pip:

```bash
pip install paho-mqtt
```

## Running the System

1. Start the `HeatingSystemSimulator`:

    ```bash
    python simulate_heating_system.py -b  mqtt.eclipseprojects.io -p 1883
    ```

2. Start the `DecisionMakingComponent` with your desired threshold:

    ```bash
    python decision_making_component.py -b mqtt.eclipseprojects.io -p 1883 -t 20
    ```

3. Start the `TemperatureMeterSimulator`:

    ```bash
    python simulate_temperature.py -b mqtt.eclipseprojects.io -p 1883
    ```

## Project Structure

- `decision_making_component.py`: Contains the `DecisionMakingComponent` class.
- `heating_system_simulator.py`: Contains the `HeatingSystemSimulator` class.
- `temperature_meter_simulator.py`: Contains the `TemperatureMeterSimulator` class.
- `Test`: Contains unittest modules.

This README provides an overview of the smart heating system simulation project, instructions for usage.