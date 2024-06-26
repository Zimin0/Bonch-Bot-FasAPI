import { base_api_url } from '../variables.js';

/**
 * Класс ПК из api.
 */
export class PC {
    /**
     * Подтягивает все существующие ПК.
     */
    static async getPCs(token) {
        try {
            const response = await fetch(`${base_api_url}/pc/all`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                return response.json();
            } else {
                const errorText = await response.text();
                console.error(`Failed to fetch PCs: ${response.status} - ${response.statusText} - ${errorText}`);
                return [];
            }
        } catch (error) {
            console.error(`Error fetching PCs: ${error.message}`);
            return [];
        }
    }

    /**
     * Подтягивает все временные промежутки существующих ПК.
     */
    static async getPCTimePeriods(physical_number, token) {
        try {
            const response = await fetch(`${base_api_url}/time_periods/pc/${physical_number}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const timePeriods = await response.json();
                // Добавляем статус к каждому временному промежутку
                return timePeriods.map(t => ({
                    start: t.time_start,
                    end: t.time_end,
                    status: t.status
                }));
            } else {
                const errorText = await response.text();
                console.error(`Failed to fetch time periods for PC ${physical_number}: ${response.status} - ${response.statusText} - ${errorText}`);
                return [];
            }
        } catch (error) {
            console.error(`Error fetching time periods for PC ${physical_number}: ${error.message}`);
            return [];
        }
    }
}
