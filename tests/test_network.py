import pytest
from core.simulator import Simulator
from core.error_injector import ErrorInjector
import core.error_injector as ei_mod

@pytest.fixture
def pump_sim(monkeypatch):
    # 1) Stub out MQTT connect (no real network)
    monkeypatch.setattr(Simulator, "connect", lambda self: None)

    # 2) Stub out iptables calls in ErrorInjector
    monkeypatch.setattr(ei_mod.subprocess, "call", lambda *args, **kwargs: 0)

    # 3) Create simulator instance
    sim = Simulator(broker='localhost', port=1883, topic='test/topic', interval=0.01)
    # Dummy client so we can track 'connected' state
    class DummyClient:
        def __init__(self):
            self.connected = True
        def connect(self, broker, port):
            # simulate a drop
            self.connected = False
        def publish(self, topic, payload):
            pass

    sim.client = DummyClient()
    return sim

def test_wifi_recovery(pump_sim):
    injector = ErrorInjector()
    # This will now call our stubbed subprocess.call and not raise
    injector.wifi_drop(duration=0.01)

    # Run the simulator (connect was stubbed, so no real socket calls)
    pump_sim.run(duration=0.02)

    # After running, we expect the client to have reconnected at simulate connect()
    assert pump_sim.client.connected