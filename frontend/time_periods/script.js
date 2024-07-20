import { User } from '../api/user.js'
import { PC } from '../api/pc.js'
import { Setting } from '../api/setting.js'
import { processLogoutButton, showMessage } from '../common.js'
import { base_api_url } from '../variables.js';

await User.pageOnlyForAdmin(); // ??????????????

//////////////////////
processLogoutButton(); // Обработка нажатия на кнопку Выйти
//////////////////////

////////////////////////
User.pageOnlyForAdmin(); // Эта страница может быть открыта только админом.
////////////////////////

const token = await User.get_auth_token();

const time_period_slug = 'TIME_PERIOD_LENGTH';
const start_time_slug = "START_TIME";
const end_time_slug = "END_TIME";

// Только для настроект с значением в минутах //
const settings_slugs = [time_period_slug, start_time_slug, end_time_slug];
const settings = await get_settings_by_slugs(settings_slugs);

// console.log(settings);
// console.log(settings.get("END_TIME").value);

/**
 * Получает настройки из переданного списка слагов.
 */
async function get_settings_by_slugs(sug_list){
    var settings = new Map();

    for (var slug of settings_slugs) {
        const setting_json = await Setting.getSettingBySlug(slug, token);
        settings.set(slug, setting_json);
        if (setting_json !== null){
            showMessage(`${slug} = ${parseInt(setting_json.value)} минут`, 'success');
        }
        else {
            showMessage(`Не удалось получить настройку ${slug}`, 'error');
        }
    }
    return settings;
}

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
    const intervalMinutes = parseInt(settings.get(time_period_slug).value);

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
            await fetch(`${base_api_url}/time_periods/pc/${pc.physical_number}`, {
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
                    pc_physical_number: pc.physical_number
                };

                const response = await fetch(`${base_api_url}/time_period`, {
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