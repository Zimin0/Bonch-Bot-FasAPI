import requests
import json
import uuid

API_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{API_URL}/token"
CREATE_SETTING_URL = f"{API_URL}/admin/setting"
HEADERS = {"Content-Type": "application/json"}
NUMBER_OF_SETTINGS = 100
SLUG_FILE = "slugs.txt"
ADMIN_EMAIL = "nikzim2004@gmail.com"
ADMIN_PASSWORD = "12345"

def login():
    payload = {
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    response = requests.post(LOGIN_URL, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to log in: {response.status_code}, {response.text}")

def create_setting(slug, token):
    setting_data = {
        "name": f"Setting {slug}",
        "slug": slug,
        "value": "Some value"
    }
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(CREATE_SETTING_URL, headers=headers, data=json.dumps(setting_data))
    return response

def main():
    token = login()
    with open(SLUG_FILE, 'w') as file:
        for _ in range(NUMBER_OF_SETTINGS):
            slug = str(uuid.uuid4())  # Генерация уникального slug
            response = create_setting(slug, token)
            if response.status_code == 201:
                file.write(f"{slug}\n")
                # print(f"Successfully created setting with slug: {slug}")
            else:
                ...
                # print(f"Failed to create setting with slug: {slug} - {response.status_code}, {response.text}")

if __name__ == "__main__":
    main()
