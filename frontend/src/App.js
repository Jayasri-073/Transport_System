import './App.css';
import { BrowserRouter as Router, Link, Routes, Route } from 'react-router-dom';
import Home from './Components/Home';
import Dashboard from './Components/Dashboard';
import MapView from './Components/MapView';
import Predictions from './Components/Predictions';
import Reports from './Components/Reports';
import Alerts from './Components/Alerts';
import PowerBIDashboard from './Components/PowerBIDashboard';
import AdminLogin from './AdminPanel/AdminLogin';
import AdminDashboard from './AdminPanel/AdminDashboard';
import AdminUpload from './AdminPanel/AdminUpload';

function App() {
  return (
    <div className="App">
      <Router>
        <nav className="navbar">
          <div className="nav-brand">
            <Link to="/">🚗 Smart Transport</Link>
          </div>
          <ul className="nav-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/mapview">Map View</Link></li>
            <li><Link to="/predictions">Predictions</Link></li>
            <li><Link to="/reports">Reports</Link></li>
            <li><Link to="/alerts">Alerts</Link></li>
            <li><Link to="/powerbi" className="powerbi-link">📊 Power BI</Link></li>
            <li><Link to="/admin" className="admin-link">Admin</Link></li>
          </ul>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/mapview" element={<MapView />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/powerbi" element={<PowerBIDashboard />} />
            <Route path="/admin" element={<AdminLogin />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/upload" element={<AdminUpload />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;

