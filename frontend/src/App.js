import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import EventsPage from './pages/EventsPage';
import EventDetailPage from './pages/EventDetailPage';
import CreateEventPage from './pages/CreateEventPage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import ManageParticipantsPage from './pages/ManageParticipantsPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/events/:id" element={<EventDetailPage />} />
        <Route path="/events/:id/manage" element={<ManageParticipantsPage />} />
        <Route path="/create" element={<CreateEventPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;