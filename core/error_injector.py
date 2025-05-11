import time, subprocess, random

class ErrorInjector:
    def __init__(self, wifi_port: int = 1883):
        self.wifi_port = wifi_port

    def wifi_drop(self, duration: float) -> None:
        """
        Temporarily block outbound TCP traffic on `wifi_port` to simulate
        a Wi-Fi dropout. Requires root privileges.
        """
        subprocess.call([
            "iptables", "-A", "OUTPUT",
            "-p", "tcp", "--dport", str(self.wifi_port),
            "-j", "DROP"
        ])
        time.sleep(duration)
        subprocess.call([
            "iptables", "-D", "OUTPUT",
            "-p", "tcp", "--dport", str(self.wifi_port),
            "-j", "DROP"
        ])

    def corrupt_data(self, data: dict, probability: float = 0.1) -> dict:
        """
        With given probability, pick a random key in `data` and set it to None.
        """
        if random.random() < probability:
            key = random.choice(list(data.keys()))
            data[key] = None
        return data