/**
Проверяет, зашел ли пользователь в систему перед доступом ко странице.
*/
export function checkAuthToken() {
    const token = localStorage.getItem('token');
    
    if (!token) {
        window.location.href = '/frontend/auth/login';
    }
}