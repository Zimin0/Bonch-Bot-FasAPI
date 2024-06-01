class SettingAPI {
    static async displaySettings() {
        try {
            const token = await get_auth_token();
            if (!token) return;  // Прекращаем выполнение, если токен не найден

            const user_info = await get_user_info(token);
            if (user_info) {
                document.getElementById("username").textContent = `Hello, ${user_info.email}`;
            }

            const response = await fetch(`${base_api_url}/admin/settings/all`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
            });
            if (response.ok) {
                const settings = await response.json();
                console.log(settings); // Выводим настройки в консоль для проверки
                const tableBody = document.querySelector("#settings-table tbody");
                tableBody.innerHTML = "";  // Очищаем таблицу перед добавлением данных
                settings.forEach(setting => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td><input type="text" id="name-${setting.id}" value="${setting.name}"></td>
                        <td><input type="text" id="slug-${setting.id}" value="${setting.slug}"></td>
                        <td><input type="text" id="value-${setting.id}" value="${setting.value}"></td>
                        <td>
                            <button onclick="Setting_api.updateSetting(${setting.id})">Обновить</button>
                            <button onclick="Setting_api.deleteSetting(${setting.id})">Удалить</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                console.error("Ошибка при получении настроек", response.status);
                displayError(`Ошибка ${response.status}: Не удалось получить настройки`);
            }
        } catch (error) {
            console.error("Сервер не отвечает", error);
            displayError("Ошибка: Сервер не отвечает");
        }
    }

    static async addSetting() {
        const token = await get_auth_token();
        if (!token) return;

        const name = document.getElementById("new-name").value;
        const slug = document.getElementById("new-slug").value;
        const value = document.getElementById("new-value").value;

        const response = await fetch(`${base_api_url}/admin/setting`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ name, slug, value }),
        });

        if (response.ok) {
            location.reload();
        } else {
            alert("Ошибка добавления настройки");
        }
    }

    static async updateSetting(id) {
        const token = await get_auth_token();
        if (!token) return;

        const name = document.getElementById(`name-${id}`).value;
        const slug = document.getElementById(`slug-${id}`).value;
        const value = document.getElementById(`value-${id}`).value;

        const response = await fetch(`${base_api_url}/admin/setting/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ name, slug, value }),
        });

        if (response.ok) {
            location.reload();
        } else {
            alert("Ошибка обновления настройки");
        }
    }

    static async deleteSetting(id) {
        const token = await get_auth_token();
        if (!token) return;

        const response = await fetch(`${base_api_url}/admin/setting/${id}`, {
            method: 'DELETE',
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.ok) {
            location.reload();
        } else {
            alert("Ошибка удаления настройки");
        }
    }
}