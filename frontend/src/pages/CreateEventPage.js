import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './CreateEventPage.css';

function CreateEventPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: '',
    description: '',
    date: '',
    time: '',
    location: '',
    max_participants: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const token = localStorage.getItem('token');
    if (!token) {
      setError('Вы не авторизованы');
      setLoading(false);
      return;
    }

    const dateTime = `${form.date}T${form.time}:00`;

    try {
      await axios.post('http://localhost:8000/events/', {
        title: form.title,
        description: form.description,
        date: dateTime,
        location: form.location,
        max_participants: parseInt(form.max_participants),
        creator_id: 1
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      navigate('/events');
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка создания события');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-page">
      <header className="header">
        <div className="logo">Вайб</div>
        <nav className="nav">
          <Link to="/" className="nav-link">Главная</Link>
          <Link to="/events" className="nav-link">Активности</Link>
          <Link to="/create" className="nav-link create-link">Создать</Link>
        </nav>
      </header>

      <div className="create-container">
        <h1>Создать активность</h1>
        <p className="subtitle">Поделитесь своими планами и пригласите других присоединиться!</p>

        <form onSubmit={handleSubmit} className="create-form">
          <div className="form-section">
            <h3>Детали активности</h3>

            <div className="form-group">
              <label>Название активности *</label>
              <input
                name="title"
                placeholder="Например: Субботний утренний поход в Воробьевы горы"
                value={form.title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Описание *</label>
              <textarea
                name="description"
                placeholder="Расскажите людям, чего ожидать, что взять с собой и другие важные детали..."
                rows="5"
                value={form.description}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Дата *</label>
                <input type="date" name="date" value={form.date} onChange={handleChange} required />
              </div>
              <div className="form-group">
                <label>Время *</label>
                <input type="time" name="time" value={form.time} onChange={handleChange} required />
              </div>
            </div>

            <div className="form-group">
              <label>Место *</label>
              <input name="location" placeholder="Город, место проведения или точка встречи" value={form.location} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Максимум участников *</label>
              <input type="number" name="max_participants" placeholder="10" value={form.max_participants} onChange={handleChange} required />
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Создание...' : 'Создать активность'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default CreateEventPage;