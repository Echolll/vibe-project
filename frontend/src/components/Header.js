import React, { useContext, useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Header.css';

function Header() {
  const { token, logout, openLoginModal, openRegisterModal } = useContext(AuthContext);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    setIsMenuOpen(false);
    navigate('/');
  };

  return (
    <header className="shared-header">
      <div className="shared-logo">
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>Vibe</Link>
      </div>
      <nav className="shared-nav">
        <Link to="/" className="shared-nav-link">Главная</Link>
        <Link to="/events" className="shared-nav-link">Активности</Link>
        <Link to="/create" className="shared-nav-link shared-create-link">Создать</Link>
      </nav>
      <div className="shared-auth">
        {!token ? (
          <>
            <button onClick={openLoginModal} className="shared-auth-link">Вход</button>
            <button onClick={openRegisterModal} className="shared-auth-link shared-register-btn">Регистрация</button>
          </>
        ) : (
          <div className="shared-user-menu" ref={menuRef}>
            <button 
              className="shared-profile-btn"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              Профиль <span style={{ fontSize: '12px' }}>▼</span>
            </button>
            {isMenuOpen && (
              <div className="shared-dropdown-menu">
                <Link to="/profile" className="shared-dropdown-item" onClick={() => setIsMenuOpen(false)}>
                  Мой профиль
                </Link>
                <button onClick={handleLogout} className="shared-dropdown-item" style={{color: '#ef4444'}}>
                  Выйти
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
