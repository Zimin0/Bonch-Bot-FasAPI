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
    static async getPCTimePeriods(pcId, token) {
        try {
            const response = await fetch(`${base_api_url}/admin/pc/${pcId}/time_periods`, {
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
                console.error(`Failed to fetch time periods for PC ${pcId}: ${response.status} - ${response.statusText} - ${errorText}`);
                return [];
            }
        } catch (error) {
            console.error(`Error fetching time periods for PC ${pcId}: ${error.message}`);
            return [];
        }
    }
}
