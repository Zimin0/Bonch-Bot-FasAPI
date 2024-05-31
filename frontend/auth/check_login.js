/**
Проверяет, зашел ли пользователь в систему перед доступом ко странице.
*/
export function checkAuthToken() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
        window.location.href = '/frontend/auth/login';
    }
}