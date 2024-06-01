import { User } from '../../api/user.js'
import { processLogoutButton } from '../../common.js'

processLogoutButton();

/**
 * Получает данные (почта, telegram tag, пароль) из формы регистрации.
 */
function getUserData(){
    const email = document.getElementById("email").value;
    const tg_tag = document.getElementById("tg_tag").value;
    const password = document.getElementById("password").value;
    return { email, tg_tag, password };
}

function getDataAndRegister(){
    const { email, tg_tag, password } = getUserData();
    User.register(email, tg_tag, password);
}

// Инициализация функций для доступа из HTML
window.getDataAndRegister = getDataAndRegister;