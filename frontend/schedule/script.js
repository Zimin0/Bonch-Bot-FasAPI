// import { base_api_url } from '../base_api_url.js';
// import { get_auth_token, logout, update_user_info } from '../user_info.js';
// import { checkAuthToken } from '../check_login.js';

import { User } from '../api/user.js'
import { PC } from '../api/pc.js'
import { processLogoutButton } from '../common.js'

processLogoutButton();

//////////////////////
User.checkAuthToken(); // Проверяем наличие токена перед загрузкой страницы
//////////////////////


// async function getPCs() {
//     const token = await get_auth_token();
//     if (!token) return [];

//     const response = await fetch(`${base_api_url}/pc/all`, {
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     });

//     if (response.ok) {
//         return response.json();
//     } else {
//         console.error('Failed to fetch PCs');
//         return [];
//     }
// }

/**
Подтягивает все временные промежутки существующих ПК.
*/
// async function getPCTimePeriods(pcId) {
//     const token = await get_auth_token();
//     if (!token) return [];

//     const response = await fetch(`${base_api_url}/admin/pc/${pcId}/time_periods`, {
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     });

//     if (response.ok) {
//         const timePeriods = await response.json();
//         // Добавляем статус к каждому временному промежутку
//         return timePeriods.map(t => ({
//             start: t.time_start,
//             end: t.time_end,
//             status: t.status
//         }));
//     } else {
//         console.error('Failed to fetch time periods for PC', pcId);
//         return [];
//     }
// }




/**
 * Выводит все временные промежутки в шаблон.
 */
async function displayTimePeriods() {
    const token = await User.get_auth_token()
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
            case 'Свободно':
                statusClass += 'time-slot-green';
                break;
            case 'Забронировано':
                statusClass += 'time-slot-red';
                break;
            case 'Перерыв между бронями':
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

// window.User.update_user_info = User.update_user_info;
// window.PC.getPCs = PC.getPCs; 
// window.PC.getPCTimePeriods = PC.getPCTimePeriods;