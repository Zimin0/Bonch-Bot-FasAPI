import { User } from '../../api/user.js'
import { processLogoutButton } from '../../common.js'

processLogoutButton();

// Инициализация функций для доступа из HTML
window.User.login = User.login;
window.User.update_user_info = User.update_user_info;