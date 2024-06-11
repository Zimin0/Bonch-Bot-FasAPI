import { base_api_url } from '../variables.js';

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
    
    static async isAdmin(token) {
        const userInfo = await User.get_user_info(token);
        if (userInfo) {
            return userInfo.is_superuser;
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
            if (document.getElementById("email") !== null){
                document.getElementById("email").value = user_info.email;
            }
            if (document.getElementById("tg_tag") !== null){
                document.getElementById("tg_tag").value = user_info.tg_tag;
            }
        } else {
            document.getElementById("username").textContent = 'Not logged yet';
        }
    }

    /**
     * Обновляет данные пользователя.
     */
    static async updateUserDetails() {
        const token = await User.get_auth_token();
        if (!token) return;  // No token found, user is not logged in

        const email = document.getElementById("email").value;
        const tg_tag = document.getElementById("tg_tag").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(`${base_api_url}/user`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ email, tg_tag, password })
            });

            if (response.ok) {
                alert("Информация успешно обновлена");
            } else {
                console.error("Ошибка при обновлении информации", response.status);
                alert("Ошибка при обновлении информации");
            }
        } catch (error) {
            console.error("Ошибка при выполнении запроса", error);
            alert("Ошибка при выполнении запроса");
        }
    }

    static async pageOnlyForAdmin() {
        const token = localStorage.getItem('token');
        if (!token) return;
        const is_admin = await User.isAdmin(token);
        if (!is_admin){
            alert("Вы не администратор. 403 ошибка.");
            window.location.href = "/frontend/auth/login/";
        }
    }

    /**
     * Удаляет аккаунт пользователя.
     */
    static async deleteUserAccount() {
        const token = await User.get_auth_token();
        if (!token) return;

        try {
            const response = await fetch(`${base_api_url}/user`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });

            if (response.ok) {
                alert("Аккаунт успешно удален");
                localStorage.removeItem("token");
                window.location.href = "/frontend/auth/login";
            } else {
                console.error("Ошибка при удалении аккаунта", response.status);
                alert("Ошибка при удалении аккаунта");
            }
        } catch (error) {
            console.error("Ошибка при выполнении запроса", error);
            alert("Ошибка при выполнении запроса");
        }
    }
    
     /**
    Проверяет, зашел ли пользователь в систему перед доступом ко странице.  
    В противном случае  редирект на страницу входа.
    */
    static async checkAuthToken() {
            const token = localStorage.getItem('token');
            if (!token) {
                window.location.href = '/frontend/auth/login';
            }
        }

    /**
     * Выход из аккаунта -> удаление токена.
     */
    static async logout() {
        const token = window.localStorage.getItem('token');
        if (token) {
            localStorage.removeItem("token");
            console.log("Токен удален.");
            window.location.href = "/frontend/auth/login";
        } else {
            console.error("Не удалось найти токен и выйти из системы.");
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

    static async getUserAvatar() {
        const token = await User.get_auth_token();
        if (!token) return;

        try {
            const response = await fetch(`${base_api_url}/user/avatar/me`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (response.ok) {
                console.log(`Путь к аватару: ${response.url}`)
                return response.url;
            } else {
                console.error("Ошибка при получении аватара", response.status);
            }
        } catch (error) {
            console.error("Ошибка при выполнении запроса", error);
        }
    }

    static async uploadUserAvatar() {
        const token = await User.get_auth_token();
        if (!token) return;  // No token found, user is not logged in

        const avatarInput = document.getElementById("avatar");
        const formData = new FormData();
        formData.append("file", avatarInput.files[0]);

        try {
            const response = await fetch(`${base_api_url}/user/avatar`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                alert("Аватар успешно загружен");
                // const avatarUrl = await User.getUserAvatar();
                // return avatarUrl;
            } else {
                console.error("Ошибка при загрузке аватара", response.status);
                alert("Ошибка при загрузке аватара");
            }
        } catch (error) {
            console.error("Ошибка при выполнении запроса", error);
            alert("Ошибка при выполнении запроса");
        }
    }
}

window.User = User;
