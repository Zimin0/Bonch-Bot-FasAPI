/**
 * Класс Временного промежутка в api.
 */
class TimePeriods {
    static async displayTimePeriods() {
        const pcs = await PC_api.getPCs();
        for (let pc of pcs) {
            let timePeriods = await PC_api.getPCTimePeriods(pc.id);
            TimePeriods.createAndAppendBlock('pc-containers', pc.id, timePeriods);
        }
    }

    static createAndAppendBlock(containerId, pcNumber, timeSlots) {
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
                timeSlot.textContent = `${TimePeriods.formatTime(slot.start)}`;
            } else {
                timeSlot.textContent = 'N/A';
            }
            pcContainer.appendChild(timeSlot);
        });

        container.appendChild(pcContainer);
    }

    static formatTime(timeString) {
        // Форматирует время до HH:MM, если timeString определено
        return timeString ? timeString.slice(0, 5) : 'N/A';
    }

    static async createTimePeriods() {
        const token = await get_auth_token();
        const messageContainer = document.getElementById('message-container');
        messageContainer.innerHTML = ''; // Удаляем старые промежутки.

        if (!token) {
            TimePeriods.showMessage('Error: No token found. Please login.', 'error');
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

            TimePeriods.showMessage('Time periods created successfully.', 'success');
        } catch (error) {
            TimePeriods.showMessage(`Error: ${error.message}`, 'error');
        }
    }

    static showMessage(message, type) {
        const messageContainer = document.getElementById('message-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = type;
        messageDiv.textContent = message;
        messageContainer.appendChild(messageDiv);
    }
}