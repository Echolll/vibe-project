import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getEvents } from '../services/api';

function EventsPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadEvents = async () => {
      try {
        setLoading(true);
        const data = await getEvents();
        setEvents(data);
      } catch (err) {
        setError('Не удалось загрузить события');
      } finally {
        setLoading(false);
      }
    };
    loadEvents();
  }, []);

  if (loading) return <div style={{ textAlign: 'center', padding: '40px' }}>Загрузка событий...</div>;
  if (error) return <div style={{ textAlign: 'center', padding: '40px', color: 'red' }}>{error}</div>;
  if (events.length === 0) return <div style={{ textAlign: 'center', padding: '40px' }}>Пока нет событий</div>;

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '40px' }}>События</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
        {events.map((event) => (
          <Link
            to={`/events/${event.id}`}
            key={event.id}
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            <div style={{ border: '1px solid #ddd', borderRadius: '12px', padding: '20px', background: 'white', transition: 'all 0.2s', cursor: 'pointer', height: '100%' }}>
              <h3 style={{ marginBottom: '10px' }}>{event.title}</h3>
              <p style={{ margin: '5px 0', color: '#666' }}>📍 {event.location || 'Место не указано'}</p>
              <p style={{ margin: '5px 0', color: '#666' }}>📅 {event.date}</p>
              <p style={{ margin: '5px 0', color: '#666' }}>👥 Макс. участников: {event.max_participants || '—'}</p>
              {event.description && (
                <p style={{ margin: '10px 0 0 0', color: '#888', fontSize: '14px' }}>{event.description}</p>
              )}
              <p style={{ margin: '10px 0 0 0', color: '#764ba2' }}>
                Статус: {event.status === 'active' ? '✅ Активно' : '⏸️ Завершено'}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default EventsPage;