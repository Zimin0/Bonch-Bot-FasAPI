import { base_api_url } from '../../base_api_url.js';

////////////////// Обработка кнопки Выйти ////////////////// 
document.addEventListener('DOMContentLoaded', () => {
    update_user_info();
    displayTimePeriods();

    // Добавляем обработчик события для ссылки "Выйти"
    const logoutLink = document.getElementById('logout_button');
    if (logoutLink){
        logoutLink.addEventListener('click', (event) =>{
            event.preventDefault();
            logout();
        })
    }
});
////////////////////////////////////////////////////////////

export async function loginUser() {
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
        window.location.href = "/";
    } else {
        alert("Ошибка входа");
    }
}

// Инициализация функций для доступа из HTML
window.loginUser = loginUser;