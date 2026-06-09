import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getEvents } from '../services/api';
import './EventsPage.css';

function EventsPage() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      const data = await getEvents();
      setEvents(data);
      setLoading(false);
    };
    load();
  }, []);

  const filteredEvents = events.filter(event =>
    event.title?.toLowerCase().includes(search.toLowerCase()) ||
    event.location?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <div className="loading">Загрузка...</div>;

  return (
    <div className="events-page">
      <header className="header">
        <div className="logo">Компаньон</div>
        <nav className="nav">
          <Link to="/" className="nav-link">Главная</Link>
          <Link to="/events" className="nav-link active">Активности</Link>
          <Link to="/create" className="nav-link create-link">Создать</Link>
        </nav>
        <div className="auth">
          <button onClick={() => { localStorage.removeItem('token'); window.location.href = '/'; }} className="logout-btn">
            Выйти
          </button>
        </div>
      </header>

      <div className="events-hero">
        <h1>Активности</h1>
        <p>Найдите ваше следующее приключение и познакомьтесь с удивительными людьми</p>
      </div>

      <div className="events-container">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Поиск активностей, мест..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="results-header">
          <span>Найдено {filteredEvents.length} активностей</span>
        </div>

        <div className="events-grid">
          {filteredEvents.map(event => (
            <Link to={`/events/${event.id}`} key={event.id} className="event-card">
              <h3>{event.title}</h3>
              <p className="event-description">{event.description?.substring(0, 100)}...</p>
              <div className="event-meta">
                <span>📅 {event.date?.split('T')[0]}</span>
                <span>📍 {event.location || 'Место не указано'}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default EventsPage;