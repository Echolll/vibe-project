import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getEventById, joinEvent, leaveEvent, getUserEventStatus } from '../services/api';
import './EventDetailPage.css';

function EventDetailPage() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [userStatus, setUserStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [currentUserId, setCurrentUserId] = useState(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [eventData, statusData] = await Promise.all([
        getEventById(id),
        getUserEventStatus(id),
      ]);
      setEvent(eventData);
      setUserStatus(statusData.status);
      
      // Пробуем получить ID текущего пользователя из токена
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const payload = JSON.parse(atob(token.split('.')[1]));
          setCurrentUserId(payload.sub);
        }
      } catch (e) {
        console.log('Не удалось получить ID пользователя из токена');
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [id]);

  const handleJoin = async () => {
    setActionLoading(true);
    try {
      await joinEvent(id);
      await loadData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка при подаче заявки');
    } finally {
      setActionLoading(false);
    }
  };

  const handleLeave = async () => {
    setActionLoading(true);
    try {
      await leaveEvent(id);
      await loadData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка при отмене');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) return <div className="loading">Загрузка...</div>;
  if (!event) return <div className="loading">Событие не найдено</div>;

  const confirmedCount = event.confirmed_participants_count || 0;
  const maxParticipants = event.max_participants;
  const isFull = maxParticipants && confirmedCount >= maxParticipants;
  const canJoin = !userStatus && !isFull;
  const isOrganizer = currentUserId && event.creator_id === parseInt(currentUserId);

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  };

  const formatTime = (dateStr) => {
    return new Date(dateStr).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="detail-page">
      <div className="detail-header">
        <Link to="/events" className="back-link">← Назад к списку</Link>
        <h1 className="detail-title">{event.title}</h1>
      </div>

      <div className="detail-content">
        {/* Левая колонка — описание */}
        <div className="detail-main">
          <div className="cover-image">
            <div className="cover-placeholder">🏞️</div>
          </div>
          <h2>Об этой активности</h2>
          <p className="description">{event.description || 'Описание отсутствует'}</p>
        </div>

        {/* Правая колонка — детали и управление */}
        <div className="detail-sidebar">
          <div className="info-card">
            <h3>Детали</h3>
            <div className="info-row">
              <span className="info-label">📅 Дата</span>
              <span className="info-value">{formatDate(event.date)}</span>
            </div>
            <div className="info-row">
              <span className="info-label">⏰ Время</span>
              <span className="info-value">{formatTime(event.date)}</span>
            </div>
            <div className="info-row">
              <span className="info-label">📍 Место</span>
              <span className="info-value">{event.location || 'Не указано'}</span>
            </div>
            <div className="info-row">
              <span className="info-label">👥 Участники</span>
              <span className="info-value">{confirmedCount} из {maxParticipants || '∞'} записалось</span>
            </div>
          </div>

          {/* Прогресс-бар мест */}
          {maxParticipants && (
            <div className="progress-section">
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${(confirmedCount / maxParticipants) * 100}%` }} />
              </div>
              <p className="progress-text">
                {confirmedCount} из {maxParticipants} мест заполнено
              </p>
            </div>
          )}

          {/* Кнопка действия */}
          <div className="action-buttons">
            {!userStatus && (
              <button
                onClick={handleJoin}
                disabled={actionLoading || !canJoin}
                className={`btn-action btn-join ${!canJoin ? 'disabled' : ''}`}
              >
                {canJoin ? '🔘 Присоединиться' : '❌ Мест нет'}
              </button>
            )}

            {userStatus === 'pending' && (
              <>
                <button disabled className="btn-action btn-pending">⏳ Заявка на рассмотрении</button>
                <button onClick={handleLeave} disabled={actionLoading} className="btn-action btn-cancel">Отменить заявку</button>
              </>
            )}

            {userStatus === 'accepted' && (
              <>
                <button disabled className="btn-action btn-accepted">✅ Вы участвуете</button>
                <button onClick={handleLeave} disabled={actionLoading} className="btn-action btn-leave">Покинуть событие</button>
              </>
            )}

            {userStatus === 'rejected' && (
              <button onClick={handleJoin} disabled={actionLoading || isFull} className="btn-action btn-join">
                {isFull ? 'Мест нет' : 'Попробовать снова'}
              </button>
            )}

            {/* Ссылка для организатора */}
            {isOrganizer && (
              <Link to={`/events/${id}/manage`} className="btn-action btn-manage">
                🛠 Управлять участниками
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default EventDetailPage;