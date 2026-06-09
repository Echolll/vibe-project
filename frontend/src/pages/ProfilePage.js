import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  getUserProfile, 
  getMyProfile, 
  updateUserProfile,
  getUserRating, 
  getUserReviews, 
  createReview,
  getEvents
} from '../services/api';
import './ProfilePage.css';

function ProfilePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [profile, setProfile] = useState(null);
  const [rating, setRating] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [events, setEvents] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  
  // Состояния для редактирования
  const [showEditModal, setShowEditModal] = useState(false);
  const [editForm, setEditForm] = useState({ username: '', email: '', full_name: '', bio: '', avatar: '' });
  
  // Состояния модального окна для аватара
  const [showAvatarPrompt, setShowAvatarPrompt] = useState(false);
  const [tempAvatarUrl, setTempAvatarUrl] = useState('');
  
  // Состояние формы отзыва
  const [newReviewText, setNewReviewText] = useState('');
  const [newReviewRating, setNewReviewRating] = useState(5);
  
  const token = localStorage.getItem('token');
  const isMyProfile = !id; // Если ID нет в URL, значит это мой профиль (/profile)
  
  let currentUserId = null;
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      currentUserId = payload.sub ? parseInt(payload.sub) : null;
    } catch (e) {}
  }

  useEffect(() => {
    if (isMyProfile && !token) {
      // Если пытаемся зайти в свой профиль без токена
      navigate('/login');
      return;
    }
    loadData();
  }, [id]);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // 1. Грузим профиль
      let profileData;
      if (isMyProfile) {
        profileData = await getMyProfile();
      } else {
        profileData = await getUserProfile(id);
      }
      setProfile(profileData);
      setEditForm({ 
        username: profileData.username || '',
        email: profileData.email || '',
        full_name: profileData.full_name || '', 
        bio: profileData.bio || '',
        avatar: profileData.avatar || ''
      });
      
      const targetUserId = profileData.id;

      // 2. Грузим рейтинг и отзывы
      const [ratingData, reviewsData, allEvents] = await Promise.all([
        getUserRating(targetUserId),
        getUserReviews(targetUserId),
        getEvents()
      ]);
      
      setRating(ratingData);
      setReviews(reviewsData);
      
      // 3. Отфильтровываем события, созданные этим пользователем
      const userEvents = allEvents.filter(e => e.creator_id === targetUserId);
      setEvents(userEvents);
      
    } catch (err) {
      console.error(err);
      if (err.response?.status === 404) {
        alert('Пользователь не найден');
        navigate('/');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (!newReviewText.trim()) return;
    
    setSubmitting(true);
    try {
      await createReview({
        to_user_id: profile.id,
        event_id: 1, // Заглушка, так как API требует event_id. Можно позже доделать выбор эвента.
        rating: newReviewRating,
        comment: newReviewText
      });
      
      // Сбрасываем форму и обновляем данные
      setNewReviewText('');
      setNewReviewRating(5);
      await loadData();
      
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка при отправке отзыва');
    } finally {
      setSubmitting(false);
    }
  };

  const handleProfileSave = async () => {
    try {
      setSubmitting(true);
      await updateUserProfile(profile.id, editForm);
      setShowEditModal(false);
      await loadData(); // Перезагружаем профиль
    } catch (err) {
      alert(err.response?.data?.detail || 'Ошибка при сохранении профиля');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="loading">Загрузка профиля...</div>;
  if (!profile) return <div className="loading">Профиль не найден</div>;
  
  const hasLeftReview = reviews.some(r => r.from_user_id === currentUserId);

  return (
    <div className="profile-page">
      <div className="profile-header">
        <Link to="/events" className="back-link">← Назад к активностям</Link>
      </div>

      <div className="profile-content">
        {/* Левая колонка - Карточка пользователя */}
        <div className="profile-sidebar">
          <div className="user-card">
            <div 
              className="avatar avatar-editable"
              onClick={() => {
                if (!isMyProfile) return;
                setTempAvatarUrl(profile.avatar || '');
                setShowAvatarPrompt(true);
              }}
              title={isMyProfile ? "Кликните, чтобы изменить фото" : ""}
            >
              {profile.avatar ? (
                <img src={profile.avatar} alt="Аватар" className="avatar-image" />
              ) : (
                <div className="avatar-placeholder">{profile.username.charAt(0).toUpperCase()}</div>
              )}
              {isMyProfile && (
                <div className="avatar-overlay">
                  <span>Изменить</span>
                </div>
              )}
            </div>
            <h1 className="username">{profile.full_name || profile.username}</h1>
            <p className="email">{isMyProfile ? profile.email : '@' + profile.username}</p>
            
            <div className="rating-block">
              <div className="stars">
                {'★'.repeat(Math.round(rating?.average_rating || 0))}
                {'☆'.repeat(5 - Math.round(rating?.average_rating || 0))}
              </div>
              <div className="rating-text">
                {rating?.average_rating ? rating.average_rating.toFixed(1) : 'Нет оценок'} 
                <span className="reviews-count"> ({rating?.reviews_count || 0} отзывов)</span>
              </div>
            </div>
            
            {profile.bio && (
              <div className="bio-block">
                <h3>О себе</h3>
                <p>{profile.bio}</p>
              </div>
            )}
            
            {isMyProfile && (
              <button className="btn-edit" onClick={() => setShowEditModal(true)}>
                Редактировать профиль
              </button>
            )}
          </div>
        </div>

        {/* Правая колонка - Мероприятия и Отзывы */}
        <div className="profile-main">
          
          <section className="profile-section">
            <h2>Организует активности <span className="badge">{events.length}</span></h2>
            {events.length === 0 ? (
              <p className="empty-text">Пользователь пока не создал ни одной активности.</p>
            ) : (
              <div className="events-grid-mini">
                {events.map(event => (
                  <Link to={`/events/${event.id}`} key={event.id} className="event-card-mini">
                    <h4>{event.title}</h4>
                    <div className="event-meta">
                      <span>📅 {event.date?.split('T')[0]}</span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </section>

          <section className="profile-section">
            <h2>Отзывы</h2>
            
            {/* Форма отправки отзыва (видна только авторизованным на ЧУЖИХ профилях, если еще не оставляли) */}
            {!isMyProfile && token && !hasLeftReview && (
              <form className="review-form" onSubmit={handleReviewSubmit}>
                <h3>Оставить отзыв</h3>
                <div className="form-group">
                  <label>Оценка:</label>
                  <select 
                    value={newReviewRating} 
                    onChange={e => setNewReviewRating(Number(e.target.value))}
                  >
                    <option value={5}>5 - Отлично</option>
                    <option value={4}>4 - Хорошо</option>
                    <option value={3}>3 - Нормально</option>
                    <option value={2}>2 - Плохо</option>
                    <option value={1}>1 - Ужасно</option>
                  </select>
                </div>
                <div className="form-group">
                  <textarea 
                    placeholder="Напишите пару слов об организаторе..." 
                    value={newReviewText}
                    onChange={e => setNewReviewText(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="btn-submit" disabled={submitting}>
                  {submitting ? 'Отправка...' : 'Отправить'}
                </button>
              </form>
            )}
            
            {!isMyProfile && token && hasLeftReview && (
              <div className="auth-prompt" style={{background: '#f0fdf4', color: '#166534'}}>
                ✅ Вы уже оставили отзыв об этом пользователе.
              </div>
            )}

            {!isMyProfile && !token && (
              <div className="auth-prompt">
                <Link to="/login">Войдите</Link>, чтобы оставить отзыв.
              </div>
            )}

            {reviews.length === 0 ? (
              <p className="empty-text">Пока нет отзывов.</p>
            ) : (
              <div className="reviews-list">
                {reviews.map(review => (
                  <div key={review.id} className="review-card">
                    <div className="review-header">
                      <span className="review-author">Пользователь #{review.from_user_id}</span>
                      <span className="review-rating">{'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}</span>
                    </div>
                    <p className="review-text">{review.comment}</p>
                    <div className="review-date">{new Date(review.created_at).toLocaleDateString()}</div>
                  </div>
                ))}
              </div>
            )}
          </section>

        </div>
      </div>

      {/* Модальное окно для смены аватара */}
      {showAvatarPrompt && (
        <div className="modal-overlay" onClick={() => setShowAvatarPrompt(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>Обновить аватар</h3>
            <p>Вставьте прямую ссылку на изображение (URL)</p>
            <input 
              type="url" 
              placeholder="https://example.com/photo.jpg" 
              value={tempAvatarUrl}
              onChange={e => setTempAvatarUrl(e.target.value)}
              className="modal-input"
              autoFocus
            />
            <div className="modal-actions">
              <button 
                className="btn-submit" 
                onClick={() => {
                  setEditForm({...editForm, avatar: tempAvatarUrl});
                  setShowAvatarPrompt(false);
                }}
              >
                Применить
              </button>
              <button 
                className="btn-edit" 
                style={{ marginTop: 0 }}
                onClick={() => setShowAvatarPrompt(false)}
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Модальное окно редактирования профиля */}
      {showEditModal && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal-content edit-profile-modal" onClick={e => e.stopPropagation()}>
            <h3>Настройки профиля</h3>
            <p>Здесь вы можете изменить свою личную информацию.</p>
            
            <div className="edit-form-grid">
              <div className="form-group">
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#475569' }}>Логин (username)</label>
                <input 
                  type="text" 
                  value={editForm.username} 
                  onChange={e => setEditForm({...editForm, username: e.target.value})}
                  className="modal-input"
                  placeholder="ivan_ivanov"
                />
              </div>
              <div className="form-group">
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#475569' }}>Email</label>
                <input 
                  type="email" 
                  value={editForm.email} 
                  onChange={e => setEditForm({...editForm, email: e.target.value})}
                  className="modal-input"
                  placeholder="ivan@example.com"
                />
              </div>
              <div className="form-group full-width">
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#475569' }}>Имя и Фамилия</label>
                <input 
                  type="text" 
                  value={editForm.full_name} 
                  onChange={e => setEditForm({...editForm, full_name: e.target.value})}
                  className="modal-input"
                  placeholder="Иван Иванов"
                />
              </div>
              <div className="form-group full-width">
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#475569' }}>Ссылка на фото (Аватар)</label>
                <input 
                  type="url" 
                  value={editForm.avatar} 
                  onChange={e => setEditForm({...editForm, avatar: e.target.value})}
                  className="modal-input"
                  placeholder="https://example.com/photo.jpg"
                />
              </div>
              <div className="form-group full-width">
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: '#475569' }}>О себе</label>
                <textarea 
                  value={editForm.bio} 
                  onChange={e => setEditForm({...editForm, bio: e.target.value})}
                  className="modal-input"
                  placeholder="Расскажите о своих увлечениях..."
                  style={{ minHeight: '60px', resize: 'vertical' }}
                />
              </div>
            </div>

            <div className="modal-actions">
              <button className="btn-submit" onClick={handleProfileSave} disabled={submitting}>
                {submitting ? 'Сохранение...' : 'Сохранить изменения'}
              </button>
              <button className="btn-edit" style={{ marginTop: 0 }} onClick={() => setShowEditModal(false)} disabled={submitting}>
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProfilePage;
