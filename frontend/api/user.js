import { base_api_url } from '../variables.js'
/**
 * Класс Юзера в api.
 */
export class User {
    static async get_auth_token() {
        const token = window.localStorage.getItem('token');
        console.log(`token = ${token}`);
        if (token) {
            return token;
        } else {
            return null;
        }
    }

    /**
     * Получает все данные о самом себе, если зашел в аккаунт.
     */
    static async get_user_info(token) {
        if (!token) return null;

        try {
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
        } catch (error) {
            console.error("Ошибка при выполнении запроса", error);
            return null;
        }
    }

    /**
     * Обновляет почту пользователя, если он зашел в аккаунт.
     */
    static async update_user_info() {
        const token = await User.get_auth_token();
        if (!token) return;  // No token found, user is not logged in

        const user_info = await User.get_user_info(token);
        if (user_info) {
            document.getElementById("username").textContent = `Hello, ${user_info.email}`;
        } else {
            document.getElementById("username").textContent = 'Not logged yet';
        }
    }
    /**
     * Выход из аккаунта -> удаление токена.
     */
    static async logout() {
        const token = window.localStorage.getItem('token');
        if (token) {
            localStorage.removeItem("token");
            console.log("Токен удален.")
            window.location.href = "/frontend/auth/login";
        } else {
            console.error("Не удалось найти токен и выйти из системы.");
        }
    }

    /**
    Проверяет, зашел ли пользователь в систему перед доступом ко странице.
    В противном случае - редирект на страницу входа.
    */
    static async checkAuthToken() {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/frontend/auth/login';
        }
    }

    static async isAdmin(token) {
        try {
            const userInfo = await User.get_user_info(token);
            if (userInfo) {
                return userInfo.is_superuser;
            } else {
                console.error('User info is null');
                return false;
            }
        } catch (error) {
            console.error(`Error checking admin status: ${error.message}`);
            return false;
        }
    }

    static async pageOnlyForAdmin() {
        const token = localStorage.getItem('token');
        if (!token) return;
        const is_admin = await User.isAdmin(token);
        if (!is_admin){
            alert("Вы не администратор. 403 ошибка.");
            window.location.href = "/frontend/auth/login/"
        }
    }

    

    /**
     * Вход в систему -> получение токена.
     */
    static async login() {
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
    
        const response = await fetch(`${base_api_url}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData.toString(),
        });
    
        if (response.ok) {
            const data = await response.json();
            alert("Вход выполнен успешно");
            window.localStorage.setItem('token', data.access_token);
        } else {
            alert("Ошибка входа");
        }
    }

    /**
     * Регистрация пользователя.
     */
    static async register(email, tg_tag, password) {
        const response = await fetch(`${base_api_url}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, tg_tag, password }),
        });
    
        if (response.ok) {
            alert("Регистрация успешна");
            window.location.href = "/frontend/auth/login";
        } else {
            alert("Ошибка регистрации");
        }
    }
}

window.User = User;