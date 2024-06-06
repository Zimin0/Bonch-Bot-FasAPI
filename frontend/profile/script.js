import { base_api_url } from '../variables.js';

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

    static async update_user_info() {
        const token = await User.get_auth_token();
        if (!token) return;  

        const user_info = await User.get_user_info(token);
        if (user_info) {
            document.getElementById("username").textContent = `Hello, ${user_info.email}`;
            document.getElementById("email").value = user_info.email;
            document.getElementById("tg_tag").value = user_info.tg_tag;
        } else {
            document.getElementById("username").textContent = 'Not logged yet';
        }
    }

    static async updateUserDetails() {
        const token = await User.get_auth_token();
        if (!token) return;  

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
