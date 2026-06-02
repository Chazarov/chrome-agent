import { Link, Navigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../auth/AuthContext.jsx";

export default function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login({ username, password });
    } catch (err) {
      setError(err.message || "Не удалось войти");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="hero-gradient" aria-hidden="true" />
      <div className="auth-shell">
        <div className="auth-intro">
          <span className="hero-badge mono">Личный кабинет</span>
          <h1>Добро пожаловать</h1>
          <p className="auth-lead">Управляйте агентами, сессиями и автоматизацией из единого дашборда.</p>
        </div>
        <div className="form-card auth-card">
          <div className="auth-tabs">
            <span className="auth-tab active">Вход</span>
            <Link to="/register" className="auth-tab">
              Регистрация
            </Link>
          </div>
          <form className="pd-form" onSubmit={handleSubmit}>
            <label className="field-span-2">
              <span className="field-label">Имя пользователя</span>
              <input
                className="field-input"
                type="text"
                autoComplete="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </label>
            <label className="field-span-2">
              <span className="field-label">Пароль</span>
              <input
                className="field-input"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {error && <p className="form-error">{error}</p>}
            <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
              {submitting ? "Вход…" : "Войти"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
