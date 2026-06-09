import axios from 'axios';

const API_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
});

// Автоматически подставляем токен в каждый запрос
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ========== СВЯЗАННЫЕ С УЧАСТНИКАМИ ==========

// Получить список участников события (для организатора)
export const getParticipants = async (eventId) => {
  const response = await apiClient.get(`/events/${eventId}/participants`);
  return response.data;
};

// Подать заявку на участие
export const joinEvent = async (eventId) => {
  const response = await apiClient.post(`/events/${eventId}/join`);
  return response.data;
};

// Отменить заявку или покинуть событие
export const leaveEvent = async (eventId) => {
  const response = await apiClient.delete(`/events/${eventId}/join`);
  return response.data;
};

// Изменить статус заявки (принять/отклонить)
export const moderateParticipant = async (eventId, participantId, newStatus) => {
  const response = await apiClient.patch(`/events/${eventId}/participants/${participantId}`, {
    new_status: newStatus,
  });
  return response.data;
};

// Получить статус текущего пользователя для события
export const getUserEventStatus = async (eventId) => {
  try {
    const response = await apiClient.get(`/events/${eventId}/my-status`);
    return response.data; // { status: "pending"/"accepted"/"rejected"/null }
  } catch {
    return { status: null };
  }
};
 


export const getEvents = async () => {
  const response = await apiClient.get('/events/');
  return response.data;
};

export const getEventById = async (id) => {
  const response = await apiClient.get(`/events/${id}`);
  return response.data;
};

export const createEvent = async (eventData) => {
  const response = await apiClient.post('/events/', eventData);
  return response.data;
};