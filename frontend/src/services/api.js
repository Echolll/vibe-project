import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getEvents = async () => {
  try {
    const response = await axios.get(`${API_URL}/events`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при загрузке событий:', error);
    return [];
  }
};

export const getEventById = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/events/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при загрузке события ${id}:`, error);
    return null;
  }
};