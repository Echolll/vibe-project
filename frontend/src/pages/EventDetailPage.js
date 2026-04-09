import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getEventById } from '../services/api';

function EventDetailPage() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadEvent = async () => {
      try {
        setLoading(true);
        const data = await getEventById(id);
        if (data) {
          setEvent(data);
        } else {
          setError('Событие не найдено');
        }
      } catch (err) {
        setError('Не удалось загрузить событие');
      } finally {
        setLoading(false);
      }
    };
    loadEvent();
  }, [id]);

  if (loading) return <div style={{ textAlign: 'center', padding: '40px' }}>Загрузка...</div>;
  if (error) return <div style={{ textAlign: 'center', padding: '40px', color: 'red' }}>{error}</div>;
  if (!event) return <div style={{ textAlign: 'center', padding: '40px' }}>Событие не найдено</div>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <Link to="/events" style={{ display: 'inline-block', marginBottom: '20px', textDecoration: 'none', color: '#764ba2' }}>
        ← Назад к списку
      </Link>
      <div style={{ border: '1px solid #ddd', borderRadius: '12px', padding: '30px', background: 'white' }}>
        <h1 style={{ marginBottom: '20px' }}>{event.title}</h1>
        <p style={{ margin: '10px 0', color: '#666' }}>📅 Дата: {event.date}</p>
        <p style={{ margin: '10px 0', color: '#666' }}>📍 Место: {event.location || 'Не указано'}</p>
        <p style={{ margin: '10px 0', color: '#666' }}>👥 Макс. участников: {event.max_participants || '—'}</p>
        {event.description && <p style={{ margin: '10px 0', color: '#888' }}>📝 Описание: {event.description}</p>}
        <p style={{ margin: '10px 0', color: '#764ba2' }}>
          Статус: {event.status === 'active' ? '✅ Активно' : '⏸️ Завершено'}
        </p>
      </div>
    </div>
  );
}

export default EventDetailPage;