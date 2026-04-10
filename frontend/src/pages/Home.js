import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="app">
      {/* Герой-блок */}
      <div className="hero">
        <h1 className="hero-title">Найдите идеальную компанию для досуга</h1>
        <p className="hero-text">
          Знакомьтесь с людьми, которые разделяют ваши интересы. 
          От походов до киновечеров — находите друзей для любых приключений.
        </p>
        <div className="hero-buttons">
          <Link to="/events" className="button button-primary">
            Смотреть активности
          </Link>
          <Link to="/create" className="button button-secondary">
            Создать активность
          </Link>
        </div>
      </div>

      {/* Категории */}
      <div className="categories">
        <h2 className="section-title">Категории</h2>
        <div className="categories-grid">
          <div className="category-card">🏔️ Походы</div>
          <div className="category-card">🎬 Кино</div>
          <div className="category-card">🎲 Настольные игры</div>
          <div className="category-card">✈️ Путешествия</div>
          <div className="category-card">💪 Фитнес</div>
          <div className="category-card">🍜 Еда и рестораны</div>
          <div className="category-card">🎵 Музыка и концерты</div>
          <div className="category-card">✨ Другое</div>
        </div>
      </div>
    </div>
  );
}

export default Home;