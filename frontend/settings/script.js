// Import necessary modules and functions
import { User } from '../api/user.js'
import { PC } from '../api/pc.js'
import { Setting } from '../api/setting.js'
import { processLogoutButton, showMessage } from '../common.js'

////////////////////////
User.pageOnlyForAdmin(); // Эта страница может быть открыта только админом.
////////////////////////

//////////////////////
processLogoutButton(); // Обработка нажатия на кнопку Выйти
//////////////////////

//////////////////////
User.checkAuthToken(); // Проверяем наличие токена перед загрузкой страницы
//////////////////////

// Define the functions to be used in the HTML
async function getTokenAndDisplaySettings() {
    const token = await User.get_auth_token();
    if (!token) return;
    Setting.displaySettings(token);
}

async function getTokenAndAddSetting() {
    const token = await User.get_auth_token();
    if (!token) return;
    Setting.addSetting(token);
}

async function getSetting() {
    const token = await User.get_auth_token();
    if (!token) return;

}

// Ensure functions are accessible in the global scope
window.User = User;
window.PC = PC;
window.Setting = Setting;
window.getTokenAndDisplaySettings = getTokenAndDisplaySettings;
window.getTokenAndAddSetting = getTokenAndAddSetting;
