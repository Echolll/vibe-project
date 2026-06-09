import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import EventsPage from './pages/EventsPage';
import EventDetailPage from './pages/EventDetailPage';
import CreateEventPage from './pages/CreateEventPage';
import ManageParticipantsPage from './pages/ManageParticipantsPage';
import ProfilePage from './pages/ProfilePage';
import { AuthProvider } from './context/AuthContext';
import AuthModal from './components/AuthModal';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AuthModal />
        <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/events/:id" element={<EventDetailPage />} />
        <Route path="/events/:id/manage" element={<ManageParticipantsPage />} />
        <Route path="/create" element={<CreateEventPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/users/:id" element={<ProfilePage />} />
      </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;