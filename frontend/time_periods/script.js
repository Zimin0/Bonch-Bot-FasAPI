import { User } from '../api/user.js'
import { PC } from '../api/pc.js'
import { Setting } from '../api/setting.js'
import { processLogoutButton, showMessage } from '../common.js'
import { base_api_url } from '../variables.js';

await User.pageOnlyForAdmin();

processLogoutButton();

//////////////////////
User.checkAuthToken(); // Проверяем наличие токена перед загрузкой страницы
////////////////////// 

const token = await User.get_auth_token();
var slug = 'TIME_PERIOD_LENGTH';
const setting = await Setting.getSettingBySlug(slug, token);
showMessage(`${slug} = ${parseInt(setting.value)/60} минут`, 'success');

const StatusEnum = {
    'booked': 'booked',
    'free': 'free',
    'break_between_bookings': 'break_between_bookings',
};

document.getElementById('create-time-periods').addEventListener('click', async () => {
    await createTimePeriods();
});

/**
    Создает блоки с временными промежутками.
*/
async function createTimePeriods() {
    const token = await User.get_auth_token();
    if (!token) return;
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = ''; // Удаляем старые промежутки.

    if (!token) {
        showMessage('Error: No token found. Please login.', 'error');
        return;
    }

    const user_info = await User.get_user_info(token);
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
                    status: StatusEnum['Свободно'], // Use the correct enum value
                    time_start: timeStart.toISOString().split('T')[1].slice(0, 8),
                    time_end: timeEnd.toISOString().split('T')[1].slice(0, 8),
                    computer_id: pc.id
                };

                const response = await fetch(`${base_api_url}/admin/time_period`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(timePeriod)
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Failed to create time period: ${response.status} - ${response.statusText} - ${errorText}`);
                }

                currentTime.setMinutes(currentTime.getMinutes() + intervalMinutes);
            }
        }

        showMessage('Time periods created successfully.', 'success');
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

window.User = User;
window.PC = PC;
window.Setting = Setting;
window.User.get_auth_token = User.get_auth_token;