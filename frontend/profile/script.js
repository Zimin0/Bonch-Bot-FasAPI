import { User } from '../api/user.js';

document.addEventListener('DOMContentLoaded', () => {
    User.update_user_info();

    document.getElementById('logout_button').addEventListener('click', () => {
        User.logout();
    });

    document.querySelector('.user-form').addEventListener('submit', (event) => {
        event.preventDefault();
        User.updateUserDetails();
    });

    document.querySelector('.delete-button').addEventListener('click', () => {
        User.deleteUserAccount();
    });

    User.getUserAvatar(); // Добавить вызов для загрузки аватара
});
