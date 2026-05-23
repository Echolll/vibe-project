import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './ManageParticipantsPage.css';

function ManageParticipantsPage() {
  const { id } = useParams();
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);
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

      <div className="participants-section">
        <div className="section-header pending-header">
          <span>🕒 Новые заявки</span>
          <span className="badge">{pendingParticipants.length}</span>
        </div>
        
        {pendingParticipants.length === 0 && (
          <div className="empty-state">Нет новых заявок</div>
        )}
        
        {pendingParticipants.map(p => (
          <div key={p.id} className="participant-card pending-card">
            <div className="participant-avatar">
              <div className="avatar-placeholder">👤</div>
            </div>
            <div className="participant-info">
              <div className="participant-name">{p.username}</div>
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

      <div className="participants-section">
        <div className="section-header accepted-header">
          <span>✅ Подтверждённые</span>
          <span className="badge">{acceptedParticipants.length}</span>
        </div>
        
        {acceptedParticipants.length === 0 && (
          <div className="empty-state">Нет подтверждённых участников</div>
        )}
        
        {acceptedParticipants.map(p => (
          <div key={p.id} className="participant-card accepted-card">
            <div className="participant-avatar">
              <div className="avatar-placeholder">👤</div>
            </div>
            <div className="participant-info">
              <div className="participant-name">{p.username}</div>
              <div className="participant-status status-accepted">участвует</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ManageParticipantsPage;