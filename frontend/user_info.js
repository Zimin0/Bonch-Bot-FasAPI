import { base_api_url } from './base_api_url.js';

/**
Подтягивает токен авторизации из локального хранилища.
*/
export async function get_auth_token() {
    const token = window.localStorage.getItem('token');
    console.log(`token = ${token}`);
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

/**
Выход из аккаунта. Удаляет токен и редиректит на страницу входа
 */
export async function logout(){
    const token = window.localStorage.getItem('token');
    if (token){
        localStorage.removeItem("token");
        console.log("Токен удален.")
        window.location.href = "/frontend/auth/login";
    } else {
        console.error("Не удалось найти токен и выйти из системы.");
    }
}

// Добавим функцию в область видимости окна
window.update_user_info = update_user_info;
window.get_user_info = get_user_info;
window.get_auth_token = get_auth_token;
window.logout = logout;