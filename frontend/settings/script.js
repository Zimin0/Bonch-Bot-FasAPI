import { User } from '../api/user.js'
import { PC } from '../api/pc.js'
import { Setting } from '../api/setting.js'
import { processLogoutButton } from '../common.js'

////////////////////////
User.pageOnlyForAdmin(); // Эта страница может быть открыта только админом.
////////////////////////

//////////////////////
processLogoutButton(); // Обработка нажатия на кнопку Выйти
//////////////////////


/**
 * Подтягивает данные новой настройки из формы.
 */
function getSettingData(){
    const name = document.getElementById("new-name").value;
    const slug = document.getElementById("new-slug").value;
    const value = document.getElementById("new-value").value;
    return {name, slug, value};   
}

async function getTokenAndDisplaySettings() {
    const token = await User.get_auth_token();
    if (!token) return;
    Setting.displaySettings(token);
}

async function getTokenAndAddSetting() {
    const token = await User.get_auth_token();
    if (!token) return;
    const {name, slug, value} = getSettingData();
    Setting.addSetting(token, name, slug, value);
}

async function getSetting() {
    const token = await User.get_auth_token();
    if (!token) return;
}

window.User = User;
window.PC = PC;
window.Setting = Setting;
window.getTokenAndDisplaySettings = getTokenAndDisplaySettings;
window.getTokenAndAddSetting = getTokenAndAddSetting;
