import { User } from '../api/user.js';

document.addEventListener('DOMContentLoaded', () => {
    User.update_user_info();

    document.getElementById('logout_button').addEventListener('click', () => {
        User.logout();
    });

    document.getElementById('info-form').addEventListener('submit', (event) => {
        event.preventDefault();
        User.updateUserDetails();
    });

    document.querySelector('.delete-button').addEventListener('click', () => {
        User.deleteUserAccount();
    });

    document.getElementById('avatar-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        await User.uploadUserAvatar();
        displayAvatar(); // Обновление аватара на странице после загрузки
    });

    displayAvatar(); // Загрузить аватар при загрузке страницы
});

async function displayAvatar() {
    const avatar_path = await User.getUserAvatar();
    document.getElementById("user-photo").src = avatar_path;
}
