import { base_api_url } from '../base_api_url.js';
import { get_auth_token, get_user_info } from '../user_info.js';

async function displaySettings() {
    try {
        const token = await get_auth_token();
        if (!token) return;  // Прекращаем выполнение, если токен не найден

        const user_info = await get_user_info(token);
        if (user_info) {
            document.getElementById("username").textContent = `Hello, ${user_info.email}`;
        }

        // Другие операции, связанные с отображением настроек или данных на странице
    } catch (error) {
        console.error("Сервер не отвечает", error);
        displayError("Ошибка: Сервер не отвечает");
    }
}

function displayError(message) {
    const table = document.querySelector("#settings-table");
    table.innerHTML = `<tr><td colspan="4" class="error">${message}</td></tr>`;
}

// Инициализация функций для доступа из HTML
window.displaySettings = displaySettings;
