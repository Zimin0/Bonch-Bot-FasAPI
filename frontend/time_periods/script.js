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

const StatusEnum = {
    'booked': 'booked',
    'free': 'free',
    'break_between_bookings': 'break_between_bookings',
};

const token = await User.get_auth_token();

const time_period_slug = 'TIME_PERIOD_LENGTH';
const start_time_slug = "START_TIME";
const end_time_slug = "END_TIME";
var USE_SETTINGS_FROM_DB = false;

// Только для настроект с значением в минутах //
const settings_slugs = [time_period_slug, start_time_slug, end_time_slug];
// const settings = await Setting.get_settings_by_slugs(settings_slugs);


for (var slug of settings_slugs) {
    var setting_json = await Setting.getSettingBySlug(slug, token);  
    if (setting_json != null){
        console.log(setting_json);
        showMessage(`${slug} = ${setting_json.value}`, 'success');
    }
    else {
        showMessage(`Не удалось получить настройку ${slug}`, 'error');
    }
}


// console.log(settings);
// console.log(settings.get("END_TIME").value);


/**
 * Парсит часы из минуты из времени формата 14:12.
 */
function parseTime(strTime, sumInMinutes=false) {
    var [hours, minutes] = strTime.split(":");
    hours = parseInt(hours);
    minutes = parseInt(minutes);
    if (sumInMinutes) {
        minutes = minutes + hours * 60
        hours = 0;
    }
    return {hours, minutes};
}

// Выбрал ли пользователь загрузку данных из бд // 
document.getElementById('use-db-settings').addEventListener('change', function() {
    USE_SETTINGS_FROM_DB = document.getElementById('use-db-settings').checked;
    console.log("Using settings from db: " + USE_SETTINGS_FROM_DB);
    const timeSelections = document.querySelectorAll('#time-selection');
    timeSelections.forEach(timeSelection => {
        if (this.checked) {
            timeSelection.style.display = 'none';
        } else {
            timeSelection.style.display = 'flex';
        }
    });
});
//////////////////////////////////////////////////

document.getElementById('create-time-periods').addEventListener('click', async () => {
    await createTimePeriods();
});

/**
 * Создает блоки с временными промежутками.
 */
async function createTimePeriods() {
    const token = await User.get_auth_token();
    if (!token) return;

    const start = new Date();
    const end = new Date();

    ///////////// Подтягиваем настройки /////////////
    console.log(USE_SETTINGS_FROM_DB);
    if (USE_SETTINGS_FROM_DB) {
        var startTime = await Setting.getSettingBySlug(start_time_slug, token);
        var endTime = await Setting.getSettingBySlug(end_time_slug, token);
        var intervalTime = await Setting.getSettingBySlug(time_period_slug, token);
    } else {
        var startTime = document.getElementById("start-time");
        var endTime = document.getElementById("end-time");
        var intervalTime = document.getElementById("interval-time");
    }

    startTime = startTime.value;
    endTime = endTime.value;
    intervalTime = intervalTime.value;

    const [startHours, startMinutes] = startTime.split(':');
    const [endHours, endMinutes] = endTime.split(':');
    const [intervalHours, intervalMinutes] = intervalTime.split(":");
    const sumMinutesIntervalBetween = parseInt(intervalMinutes) + parseInt(intervalHours) * 60

    start.setHours(parseInt(startHours), parseInt(startMinutes), 0, 0);
    end.setHours(parseInt(endHours), parseInt(endMinutes), 0, 0);
    // Подстраиваем время под временную зону //
    const startUTC = new Date(start.getTime() - (start.getTimezoneOffset() * 60000));
    const endUTC = new Date(end.getTime() - (end.getTimezoneOffset() * 60000));
    /////////////////////////////////////////////////

    // const user_info = await User.get_user_info(token);
    // if (user_info) {
    //     document.getElementById("username").textContent = `Hello, ${user_info.email}`;
    // }

    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = ''; // Удаляем старые промежутки.

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
                timeEnd.setMinutes(timeEnd.getMinutes() + sumMinutesIntervalBetween);

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

                currentTime.setMinutes(currentTime.getMinutes() + sumMinutesIntervalBetween);
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