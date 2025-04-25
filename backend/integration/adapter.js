import axios from 'axios';
import { newIntegrationCredentials } from './credentials';

const BASE_URL = '[]';
const TIMEOUT = 60000;
const MAX_RETRIES = 3;

async function fetchData(endpoint) {
    const url = `${BASE_URL}${endpoint}`;
    const headers = {
        'Authorization': `Bearer ${newIntegrationCredentials.apiKey}`,
        // Add other headers as needed
    };

    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
        try {
            const response = await axios.get(url, { headers, timeout: TIMEOUT });
            console.log('Request URL:', url);
            console.log('Request Headers:', headers);
            console.log('Response:', response.data);
            return response.data;
        } catch (error) {
            if (error.response) {
                console.error('Error Response:', { status_code: error.response.status, ...error.response.data });
            } else {
                console.error('Error:', error.message);
            }

            if (attempt < MAX_RETRIES - 1 && (error.code === 'ECONNABORTED' || !error.response || error.response.status >= 500)) {
                const delay = Math.pow(2, attempt) * 1000;
                console.log(`Retrying in ${delay}ms...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            } else {
                throw error;
            }
        }
    }
}

export { fetchData };