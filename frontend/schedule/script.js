// import { base_api_url } from '../base_api_url.js';
// import { get_auth_token, logout, update_user_info } from '../user_info.js';
// import { checkAuthToken } from '../check_login.js';

import { User } from '../api/user.js'
import { PC } from '../api/pc.js'
import { processLogoutButton } from '../common.js'

processLogoutButton();

if (!User.isAdmin()){
    displayNotAdminMessage();
}

//////////////////////
User.checkAuthToken(); // Проверяем наличие токена перед загрузкой страницы
//////////////////////

/**
 * Выводит все временные промежутки в шаблон.
 */
async function displayTimePeriods() {
    const token = await User.get_auth_token()
    if (!token) return;
    const pcs = await PC.getPCs(token);
    for (let pc of pcs) {
        let timePeriods = await PC.getPCTimePeriods(pc.id, token);
        createAndAppendBlock('pc-containers', pc.id, timePeriods);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    displayTimePeriods();
});

function createAndAppendBlock(containerId, pcNumber, timeSlots) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const pcContainer = document.createElement('div');
    pcContainer.className = 'container';

    const pcBlock = document.createElement('div');
    pcBlock.className = 'pc-block';
    pcBlock.textContent = pcNumber;

    pcContainer.appendChild(pcBlock);

    timeSlots.forEach(slot => {
        const timeSlot = document.createElement('div');
        let statusClass = 'time-slot ';
        switch (slot.status) {
            case 'free':
                statusClass += 'time-slot-green';
                break;
            case 'booked':
                statusClass += 'time-slot-red';
                break;
            case 'break_between_bookings':
                statusClass += 'time-slot-yellow';
                break;
            default:
                statusClass += 'time-slot-black';
                break;
        }
        timeSlot.className = statusClass;
        if (slot.start) {
            timeSlot.textContent = `${formatTime(slot.start)}`;
        } else {
            timeSlot.textContent = 'N/A';
        }
        pcContainer.appendChild(timeSlot);
    });

    container.appendChild(pcContainer);
}

/**
 * Форматирует время до HH:MM, если timeString определено
 */
function formatTime(timeString) {
    return timeString ? timeString.slice(0, 5) : 'N/A';
}

window.User = User;
window.PC = PC;
