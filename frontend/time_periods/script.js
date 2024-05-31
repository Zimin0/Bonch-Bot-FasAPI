import { base_api_url } from '../base_api_url.js';
import { get_auth_token, get_user_info, update_user_info } from '../user_info.js';

document.getElementById('create-time-periods').addEventListener('click', async () => {
    await createTimePeriods();
});

async function createTimePeriods() {
    const token = await get_auth_token();
    if (!token) return;  // Прекращаем выполнение, если токен не найден

    const user_info = await get_user_info(token);
    if (user_info) {
        document.getElementById("username").textContent = `Hello, ${user_info.email}`;
    }

    const startTime = "10:00";
    const endTime = "21:00";
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

    const pcs = await fetch(`${base_api_url}/pc/all`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(response => response.json());

    for (const pc of pcs) {
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

    alert('Time periods created successfully.');
}
