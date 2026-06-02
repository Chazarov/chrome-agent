import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext.jsx";

export default function AppHeader({ showLogout = false }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login", { replace: true });
  }

  return (
    <header className="site-header">
      <div className="wrap header-inner">
        <Link to="/" className="logo" aria-label="На главную">
          <span className="logo-icon" aria-hidden="true">
            ◈
          </span>
          <span>GigaBrowser Agent</span>
        </Link>
        <div className="nav-actions">
          {user && (
            <span className="header-user mono">
              {user.username}
            </span>
          )}
          {showLogout && (
            <button type="button" className="btn btn-ghost" onClick={handleLogout}>
              Выйти
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
