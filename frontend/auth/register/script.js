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

export async function registerUser() {
    const email = document.getElementById("email").value;
    const tg_tag = document.getElementById("tg_tag").value;
    const password = document.getElementById("password").value;
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

window.registerUser = registerUser;