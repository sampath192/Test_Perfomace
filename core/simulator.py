from paho.mqtt import client as mqtt_client
import time, json, random
from faker import Faker

class Simulator:
    def __init__(
        self,
        broker: str,
        port: int,
        topic: str,
        interval: float = 1.0
    ):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.interval = interval
        self.client = mqtt_client.Client(client_id=f"sim-{random.randint(0, 1000)}")
        self.faker = Faker()

    def connect(self) -> None:
        """Establish MQTT connection."""
        self.client.connect(self.broker, self.port)

    def publish(self, payload: dict) -> None:
        """Publish a JSON payload to the MQTT topic."""
        self.client.publish(self.topic, json.dumps(payload))

    def run(self, duration: float) -> None:
        """
        Run the simulator for `duration` seconds, publishing dose events
        every `interval` seconds.
        """
        self.connect()
        start_ts = time.time()
        while time.time() - start_ts < duration:
            payload = {
                "device_id": self.faker.uuid4(),
                "timestamp": time.time(),
                "dose": round(random.uniform(0.5, 2.0), 3)
            }
            self.publish(payload)
            time.sleep(self.interval)