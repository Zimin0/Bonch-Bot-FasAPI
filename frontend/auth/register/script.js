import { base_api_url } from '../../base_api_url.js';

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