import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import styles from './Home.module.css';

function Home() {
  return (
    <div className={styles.homeContainer}>
      <Header />

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