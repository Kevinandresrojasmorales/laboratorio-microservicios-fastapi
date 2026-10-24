from locust import HttpUser, between, task


class UsuarioCarga(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def consultar_servicio(self):
        self.client.get("/__SERVICE__", name="/__SERVICE__")
