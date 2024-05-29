import { base_api_url } from '../base_api_url.js';

export async function displaySettings() {
    try {
        const response = await fetch(`${base_api_url}/admin/settings/all`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
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
                        <button onclick="updateSetting(${setting.id})">Обновить</button>
                        <button onclick="deleteSetting(${setting.id})">Удалить</button>
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

function displayError(message) {
    const table = document.querySelector("#settings-table");
    table.innerHTML = `<tr><td colspan="4" class="error">${message}</td></tr>`;
}

export async function addSetting() {
    const name = document.getElementById("new-name").value;
    const slug = document.getElementById("new-slug").value;
    const value = document.getElementById("new-value").value;

    const response = await fetch(`${base_api_url}/admin/setting`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, slug, value }),
    });

    if (response.ok) {
        location.reload();
    } else {
        alert("Ошибка добавления настройки");
    }
}

export async function updateSetting(id) {
    const name = document.getElementById(`name-${id}`).value;
    const slug = document.getElementById(`slug-${id}`).value;
    const value = document.getElementById(`value-${id}`).value;

    const response = await fetch(`${base_api_url}/admin/setting/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, slug, value }),
    });

    if (response.ok) {
        location.reload();
    } else {
        alert("Ошибка обновления настройки");
    }
}

export async function deleteSetting(id) {
    const response = await fetch(`${base_api_url}/admin/setting/${id}`, {
        method: 'DELETE',
    });

    if (response.ok) {
        location.reload();
    } else {
        alert("Ошибка удаления настройки");
    }
}

// Инициализация функций для доступа из HTML
window.displaySettings = displaySettings;
window.addSetting = addSetting;
window.updateSetting = updateSetting;
window.deleteSetting = deleteSetting;