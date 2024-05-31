import { base_api_url } from '../base_api_url.js';
import { get_auth_token, get_user_info, update_user_info, logout  } from '../user_info.js';
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

document.getElementById('create-time-periods').addEventListener('click', async () => {
    await createTimePeriods();
});

/**
    Создает блоки с временными промежутками.
*/
async function createTimePeriods() {
    const token = await get_auth_token();
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = ''; // Удаляем старые промежутки.

    if (!token) {
        showMessage('Error: No token found. Please login.', 'error');
        return;
    }

    const user_info = await get_user_info(token);
    if (user_info) {
        document.getElementById("username").textContent = `Hello, ${user_info.email}`;
    }

    const startTime = document.getElementById("start-time").value;
    const endTime = document.getElementById("end-time").value;
    const intervalMinutes = 15;

    const start = new Date();
    const end = new Date();

    const [startHours, startMinutes] = startTime.split(':');
    const [endHours, endMinutes] = endTime.split(':');

    start.setHours(parseInt(startHours), parseInt(startMinutes), 0, 0);
    end.setHours(parseInt(endHours), parseInt(endMinutes), 0, 0);

    // Adjust start and end time to UTC
    const startUTC = new Date(start.getTime() - (start.getTimezoneOffset() * 60000));
    const endUTC = new Date(end.getTime() - (end.getTimezoneOffset() * 60000));

    try {
        const pcs = await fetch(`${base_api_url}/pc/all`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }).then(response => response.json());

        for (const pc of pcs) {
            // Delete old time periods for this PC
            await fetch(`${base_api_url}/admin/pc/${pc.id}/time_periods`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            let currentTime = new Date(startUTC);
            while (currentTime < endUTC) {
                const timeStart = new Date(currentTime);
                const timeEnd = new Date(currentTime);
                timeEnd.setMinutes(timeEnd.getMinutes() + intervalMinutes);

                const timePeriod = {
                    time_start: timeStart.toISOString().split('T')[1].slice(0, 8),
                    time_end: timeEnd.toISOString().split('T')[1].slice(0, 8),
                    computer_id: pc.id
                };

                await fetch(`${base_api_url}/admin/time_period`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(timePeriod)
                });

                currentTime.setMinutes(currentTime.getMinutes() + intervalMinutes);
            }
        }

        showMessage('Time periods created successfully.', 'success');
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

/** 
Выводит сообщения об ошибках на страницу.
*/
function showMessage(message, type) {
    const messageContainer = document.getElementById('message-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    messageContainer.appendChild(messageDiv);
}


window.update_user_info = update_user_info;
