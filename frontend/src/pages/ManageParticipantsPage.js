import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './ManageParticipantsPage.css';

function ManageParticipantsPage() {
  const { id } = useParams();
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [modalRating, setModalRating] = useState(null);
  const [modalLoading, setModalLoading] = useState(false);
  const token = localStorage.getItem('token');

  const loadParticipants = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/events/${id}/participants`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setParticipants(response.data);
    } catch (error) {
      console.error('Ошибка загрузки:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadParticipants();
  }, [id]);

  useEffect(() => {
    if (selectedUser) {
      setModalLoading(true);
      axios.get(`http://localhost:8000/reviews/user/${selectedUser.id}/rating`)
        .then((res) => {
          setModalRating(res.data);
          setModalLoading(false);
        })
        .catch(() => {
          setModalRating({ average_rating: 0, reviews_count: 0 });
          setModalLoading(false);
        });
    }
  }, [selectedUser]);

  const handleModerate = async (participantId, newStatus) => {
    try {
      await axios.patch(
        `http://localhost:8000/events/${id}/participants/${participantId}`,
        null,
        {
          params: { new_status: newStatus },
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      loadParticipants();
    } catch (error) {
      alert(error.response?.data?.detail || 'Ошибка при обработке заявки');
    }
  };

  if (loading) return <div className="loading">Загрузка...</div>;

  const pendingParticipants = participants.filter(p => p.status === 'pending');
  const acceptedParticipants = participants.filter(p => p.status === 'accepted');

  return (
    <div className="manage-container">
      <Link to={`/events/${id}`} className="back-link">
        ← Назад к событию
      </Link>
      
      <h1 className="manage-title">Управление участниками</h1>

      <div className="participants-section pending-section">
        <div className="section-header pending-header">
          <span>🕒 Новые заявки</span>
          <span className="badge">{pendingParticipants.length}</span>
        </div>
        
        {pendingParticipants.length === 0 && (
          <div className="empty-state">Нет новых заявок</div>
        )}
        
        {pendingParticipants.map(p => (
          <div key={p.id} className="participant-card pending-card" onClick={() => setSelectedUser(p.user)} style={{ cursor: 'pointer' }}>
            <div className="participant-avatar">
              {p.user?.avatar ? (
                <img src={p.user.avatar} alt="Аватар" className="avatar-image-mini" />
              ) : (
                <div className="avatar-placeholder">{p.user?.username?.charAt(0).toUpperCase() || '👤'}</div>
              )}
            </div>
            <div className="participant-info">
              <div className="participant-name">{p.user?.full_name || p.user?.username || 'Неизвестный'}</div>
              <div className="participant-status status-pending">ожидает подтверждения</div>
            </div>
            <div className="participant-actions">
              <button onClick={() => handleModerate(p.id, 'accepted')} className="btn-accept">
                ✅ Принять
              </button>
              <button onClick={() => handleModerate(p.id, 'rejected')} className="btn-reject">
                ❌ Отклонить
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="participants-section accepted-section">
        <div className="section-header accepted-header">
          <span>✅ Подтверждённые</span>
          <span className="badge">{acceptedParticipants.length}</span>
        </div>
        
        {acceptedParticipants.length === 0 && (
          <div className="empty-state">Нет подтверждённых участников</div>
        )}
        
        {acceptedParticipants.map(p => (
          <div key={p.id} className="participant-card accepted-card" onClick={() => setSelectedUser(p.user)} style={{ cursor: 'pointer' }}>
            <div className="participant-avatar">
              {p.user?.avatar ? (
                <img src={p.user.avatar} alt="Аватар" className="avatar-image-mini" />
              ) : (
                <div className="avatar-placeholder">{p.user?.username?.charAt(0).toUpperCase() || '👤'}</div>
              )}
            </div>
            <div className="participant-info">
              <div className="participant-name">{p.user?.full_name || p.user?.username || 'Неизвестный'}</div>
              <div className="participant-status status-accepted">участвует</div>
            </div>
          </div>
        ))}
      </div>

      {/* Модальное окно профиля участника */}
      {selectedUser && (
        <div className="participant-modal-overlay" onClick={() => setSelectedUser(null)}>
          <div className="participant-modal-content" onClick={e => e.stopPropagation()}>
            <button className="participant-modal-close" onClick={() => setSelectedUser(null)}>✕</button>
            
            <div className="participant-modal-header">
              {selectedUser.avatar ? (
                <img src={selectedUser.avatar} alt="Аватар" className="participant-modal-avatar" />
              ) : (
                <div className="participant-modal-avatar-placeholder">
                  {selectedUser.username.charAt(0).toUpperCase()}
                </div>
              )}
              <div className="participant-modal-titles">
                <h2>{selectedUser.full_name || selectedUser.username}</h2>
                <p className="participant-modal-username">@{selectedUser.username}</p>
                
                <div className="participant-modal-rating">
                  {'★'.repeat(Math.round(modalRating?.average_rating || 0))}
                  {'☆'.repeat(5 - Math.round(modalRating?.average_rating || 0))}
                  <span className="rating-num"> {modalRating?.average_rating ? modalRating.average_rating.toFixed(1) : '0.0'}</span>
                  <span className="rating-count"> ({modalRating?.reviews_count || 0})</span>
                </div>
                
                {selectedUser.email && (
                  <p className="participant-modal-email">📧 {selectedUser.email}</p>
                )}
              </div>
            </div>

            <div className="participant-modal-actions">
              <Link to={`/users/${selectedUser.id}`} className="btn-view-profile">
                Перейти в профиль
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ManageParticipantsPage;