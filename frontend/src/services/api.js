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

// ========== СВЯЗАННЫЕ С ПОЛЬЗОВАТЕЛЯМИ И ПРОФИЛЕМ ==========

export const getMyProfile = async () => {
  const response = await apiClient.get('/users/me');
  return response.data;
};

export const getUserProfile = async (userId) => {
  const response = await apiClient.get(`/users/${userId}`);
  return response.data;
};

export const updateUserProfile = async (userId, data) => {
  const response = await apiClient.patch(`/users/${userId}`, data);
  return response.data;
};

export const deleteUser = async (userId, password) => {
  const response = await apiClient.delete(`/users/${userId}`, { data: { password } });
  return response.data;
};

// (Временно, если на бэкенде появится ручка для событий конкретного юзера. Пока будем тянуть все и фильтровать)
// Но так как у нас нет /users/{id}/events, мы можем просто загрузить все события и отфильтровать по creator_id

// ========== СВЯЗАННЫЕ С ОТЗЫВАМИ ==========

export const getUserReviews = async (userId) => {
  const response = await apiClient.get(`/reviews/user/${userId}`);
  return response.data;
};

export const getUserRating = async (userId) => {
  const response = await apiClient.get(`/reviews/user/${userId}/rating`);
  return response.data;
};

export const createReview = async (reviewData) => {
  const response = await apiClient.post('/reviews/', reviewData);
  return response.data;
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

export const deleteEvent = async (eventId) => {
  const response = await apiClient.delete(`/events/${eventId}`);
  return response.data;
};