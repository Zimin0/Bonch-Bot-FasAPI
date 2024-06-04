/**
 * Обработка кнопки Выйти в верхнем меню.
 */
export function processLogoutButton(){
    document.addEventListener('DOMContentLoaded', () => {
        const logoutLink = document.getElementById('logout_button');
        if (logoutLink){
            logoutLink.addEventListener('click', (event) =>{
                event.preventDefault();

                const token = window.localStorage.getItem('token');
                if (token) {
                    localStorage.removeItem("token");
                    console.log("Токен удален.")
                    window.location.href = "/frontend/auth/login";
                } else {
                    console.error("Не удалось найти токен и выйти из системы.");
                }
            })
        }
    });
}

/** 
Выводит сообщения об ошибках на страницу.
*/
export function showMessage(message, type) {
    const messageContainer = document.getElementById('message-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    messageContainer.appendChild(messageDiv);
}

/** 
Проверяет, что пользователь является админом. В ином случае - сообщение 403 и редирект.
*/


