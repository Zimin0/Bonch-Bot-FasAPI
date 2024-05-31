import { base_api_url } from '../base_api_url.js';
import { get_auth_token, logout, update_user_info } from '../user_info.js';
import { checkAuthToken } from '../check_login.js';

/////////////////
checkAuthToken(); // Проверяем наличие токена перед загрузкой страницы
/////////////////   

////////////////// Обработка кнопки Выйти ////////////////// 
document.addEventListener('DOMContentLoaded', () => {
    update_user_info();
    displayTimePeriods();

    // Добавляем обработчик события для ссылки "Выйти"
    const logoutLink = document.getElementById('logout_button');
    if (logoutLink){
        logoutLink.addEventListener('click', (event) =>{
            event.preventDefault();
            logout();
        })
    }
});
////////////////////////////////////////////////////////////

/**
Подтягивает все существующие ПК.
*/
async function getPCs() {
    const token = await get_auth_token();
    if (!token) return [];

    const response = await fetch(`${base_api_url}/pc/all`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        return response.json();
    } else {
        console.error('Failed to fetch PCs');
        return [];
    }
}

/**
Подтягивает все временные промежутки существующих ПК.
*/
async function getPCTimePeriods(pcId) {
    const token = await get_auth_token();
    if (!token) return [];

    const response = await fetch(`${base_api_url}/admin/pc/${pcId}/time_periods`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        return response.json();
    } else {
        console.error('Failed to fetch time periods for PC', pcId);
        return [];
    }
}

/**
Выводит все временные промежутки в шаблон.
*/
async function displayTimePeriods() {
    // Выводит временные промежутки и ПК
    const pcs = await getPCs();
    for (let pc of pcs) {
        let timePeriods = await getPCTimePeriods(pc.id);
        const timeSlots = timePeriods.map(t => {
            return {
                start: t.time_start,
                end: t.time_end
            };
        });
        createAndAppendBlock('pc-containers', pc.id, timeSlots);
    }
}

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
        timeSlot.className = 'time-slot time-slot-green'; // Adjust class based on your criteria
        timeSlot.textContent = `${formatTime(slot.start)}`;
        pcContainer.appendChild(timeSlot);
    });

    container.appendChild(pcContainer);
}

function formatTime(timeString) {
    // Форматирует время до HH:MM
    return timeString.slice(0, 5);
}

window.update_user_info = update_user_info;
