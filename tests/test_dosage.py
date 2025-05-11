import pytest
from core.simulator import Simulator

@pytest.fixture
def sim_publisher(monkeypatch):
    # 1) Prevent real network connects
    monkeypatch.setattr(Simulator, "connect", lambda self: None)

    # 2) Create simulator (connect() is now a no-op)
    sim = Simulator(broker="localhost", port=1883, topic="test/topic", interval=0.0)

    # 3) Capture all published payloads
    published = []
    def dummy_publish(payload):
        published.append(payload)
    monkeypatch.setattr(sim, "publish", dummy_publish)

    return sim, published

def test_dose_value_ranges(sim_publisher):
    sim, published = sim_publisher
    # Now run() only calls our stubbed connect() + dummy_publish()
    sim.run(duration=0.05)
    assert published, "No payloads published"
    for p in published:
        assert 0.5 <= p["dose"] <= 2.0