import { User } from '../../api/user.js'
import { processLogoutButton } from '../../common.js'

//////////////////////
processLogoutButton(); // Обработка нажатия на кнопку Выйти
//////////////////////

window.User.login = User.login;
window.User.update_user_info = User.update_user_info;