from locust import HttpUser, task, between

class PumpUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def send_dose(self):
        self.client.post("/api/dose", json={"dose": 1.0})