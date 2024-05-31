import { base_api_url } from './base_api_url.js';

export async function get_auth_token() {
    // Подтягивает токен авторизации из локального хранилища.
    const token = window.localStorage.getItem('token');
    if (token) {
        return token;
    } else {
        return null;
    }
}

export async function get_user_info(token) {
    if (!token) return null;

    const response = await fetch(`${base_api_url}/user/me`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.ok) {
        return await response.json();
    } else {
        console.error("Ошибка при получении информации о пользователе", response.status);
        return null;
    }
}

export async function update_user_info() {
    const token = await get_auth_token();
    if (!token) return;  // No token found, user is not logged in

    const user_info = await get_user_info(token);
    if (user_info) {
        document.getElementById("username").textContent = `Hello, ${user_info.email}`;
    } else {
        document.getElementById("username").textContent = 'Not logged in';
    }
}

// Добавим функцию в область видимости окна
window.update_user_info = update_user_info;
window.get_user_info = get_user_info;
window.get_auth_token = get_auth_token;