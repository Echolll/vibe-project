import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './Home.module.css';

function Home() {
  const token = localStorage.getItem('token');
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className={styles.homeContainer}>
      <header className={styles.header}>
        <div className={styles.logo}>Вайб</div>
        <nav className={styles.nav}>
          <Link to="/" className={`${styles.navLink} ${styles.active}`}>Главная</Link>
          <Link to="/events" className={styles.navLink}>Активности</Link>
          <Link to="/create" className={`${styles.navLink} ${styles.createLink}`}>Создать</Link>
        </nav>
        <div className={styles.auth}>
          {!token ? (
            <>
              <Link to="/login" className={styles.authLink}>Вход</Link>
              <Link to="/register" className={`${styles.authLink} ${styles.registerBtn}`}>Регистрация</Link>
            </>
          ) : (
            <div className={styles.userMenu}>
              <button onClick={() => setIsMenuOpen(!isMenuOpen)} className={styles.profileBtn}>
                Профиль ▾
              </button>
              {isMenuOpen && (
                <div className={styles.dropdownMenu}>
                  <Link to="/profile" className={styles.dropdownItem}>Мой профиль</Link>
                  <button onClick={() => { localStorage.removeItem('token'); window.location.href = '/'; }} className={styles.dropdownItem} style={{color: '#ef4444'}}>
                    Выйти
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </header>

      <section className={styles.hero}>
        <h1 className={styles.heroTitle}>Найдите идеальную компанию для досуга</h1>
        <p className={styles.heroSubtitle}>
          Знакомьтесь с людьми, которые разделяют ваши интересы. 
          От походов до кинотеатров — находите друзей для любых приключений.
        </p>
        <div className={styles.heroButtons}>
          <Link to="/events" className={`${styles.btn} ${styles.btnPrimary}`}>Смотреть активности</Link>
          <Link to="/create" className={`${styles.btn} ${styles.btnSecondary}`}>Создать активность</Link>
        </div>
      </section>
    </div>
  );
}

export default Home;