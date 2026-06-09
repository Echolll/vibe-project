import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import './AuthModal.css';

function AuthModal() {
  const { isAuthModalOpen, authMode, setAuthMode, closeAuthModal, login } = useContext(AuthContext);
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isAuthModalOpen) return null;

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleOverlayClick = (e) => {
    if (e.target.className === 'auth-modal-overlay') {
      closeAuthModal();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (authMode === 'login') {
        const formData = new URLSearchParams();
        formData.append('username', form.username);
        formData.append('password', form.password);

        const response = await axios.post('http://localhost:8000/auth/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        login(response.data.access_token);
        // Page reload or state updates might be handled elsewhere if needed
        // but login() already sets token and closes modal.
      } else {
        await axios.post('http://localhost:8000/auth/register', {
          username: form.username,
          email: form.email,
          password: form.password,
        });
        
        // Auto-login or switch to login mode after successful registration
        setAuthMode('login');
        setForm({ username: '', email: '', password: '' });
      }
    } catch (err) {
      setError(err.response?.data?.detail || (authMode === 'login' ? 'Ошибка входа' : 'Ошибка регистрации'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-modal-overlay" onClick={handleOverlayClick}>
      <div className="auth-modal-content">
        <button className="auth-modal-close" onClick={closeAuthModal}>&times;</button>
        
        <h2 className="auth-modal-title">
          {authMode === 'login' ? 'Вход' : 'Регистрация'}
        </h2>
        
        {error && <p className="auth-error-message">{error}</p>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="text"
            name="username"
            placeholder="Логин"
            value={form.username}
            onChange={handleChange}
            required
            className="auth-input"
          />
          {authMode === 'register' && (
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={form.email}
              onChange={handleChange}
              required
              className="auth-input"
            />
          )}
          <input
            type="password"
            name="password"
            placeholder="Пароль"
            value={form.password}
            onChange={handleChange}
            required
            className="auth-input"
          />
          
          <button type="submit" disabled={loading} className="auth-submit-btn">
            {loading ? 'Загрузка...' : (authMode === 'login' ? 'Войти' : 'Зарегистрироваться')}
          </button>
        </form>

        <p className="auth-switch-text">
          {authMode === 'login' ? 'Нет аккаунта?' : 'Уже есть аккаунт?'}
          <button 
            type="button" 
            className="auth-switch-btn" 
            onClick={() => {
              setAuthMode(authMode === 'login' ? 'register' : 'login');
              setError('');
            }}
          >
            {authMode === 'login' ? 'Зарегистрироваться' : 'Войти'}
          </button>
        </p>
      </div>
    </div>
  );
}

export default AuthModal;
