from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    @task
    def get_all_pc(self):
        self.client.get("/pc/all")

    @task
    def get_all_sessions(self):
        self.client.get("/sessions")

    @task
    def get_all_settings(self):
        self.client.get("/admin/settings/all")

    @task
    def get_all_time_periods(self):
        self.client.get("/admin/time_periods/all")

    @task
    def get_pc_time_periods(self):
        self.client.get("/admin/pc/1/time_periods")

    @task
    def get_user(self):
        self.client.get("/user/nikzim2004@gmail.com")

    @task
    def get_setting_by_slug(self):
        self.client.get('/admin/setting/slug/MOSKOW_LOCATION')


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # время ожидания между запросами

# Если нужно выполнять аутентификацию перед каждым запросом, добавьте метод on_start
class AuthenticatedUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # время ожидания между запросами

    def on_start(self):
        response = self.client.post("/token", data={"username": "nikzim2004@gmail.com", "password": "12345"})
        token = response.json()["access_token"]
        self.client.headers.update({"Authorization": f"Bearer {token}"})
