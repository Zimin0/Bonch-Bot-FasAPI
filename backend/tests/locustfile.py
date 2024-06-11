from locust import HttpUser, TaskSet, task, between
import random

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

SLUG_FILE = "slugs.txt"

class SettingsBehavior(TaskSet):

    def on_start(self):
        # Загружаем slugs из файла
        with open(SLUG_FILE, 'r') as file:
            self.slugs = file.readlines()
        self.slugs = [slug.strip() for slug in self.slugs]

    @task
    def get_all_settings(self):
        self.client.get("/admin/settings/all")

    @task
    def get_setting_by_slug(self):
        # Выбираем случайный slug из списка
        slug = random.choice(self.slugs)
        self.client.get(f"/admin/setting/slug/{slug}")
class AuthenticatedUser(HttpUser):
    tasks = [SettingsBehavior]
    wait_time = between(1, 5)  # время ожидания между запросами

    def on_start(self):
        response = self.client.post("/token", data={"username": "nikzim2004@gmail.com", "password": "12345"})
        if response.status_code == 200:
            try:
                token = response.json().get("access_token")
                if token:
                    self.client.headers.update({"Authorization": f"Bearer {token}"})
                else:
                    print("No access_token in response")
            except ValueError:
                print("Response is not in JSON format")
        else:
            print(f"Failed to authenticate, status code: {response.status_code}, response: {response.text}")

# class WebsiteUser(HttpUser):
#     tasks = [UserBehavior]
#     wait_time = between(1, 5)  # время ожидания между запросами

