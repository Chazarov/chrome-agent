import { Link, Navigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../auth/AuthContext.jsx";

export default function RegisterPage() {
  const { register, isAuthenticated } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
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
      await register({ username, password, email: email || undefined });
    } catch (err) {
      setError(err.message || "Не удалось зарегистрироваться");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="hero-gradient" aria-hidden="true" />
      <div className="auth-shell">
        <div className="auth-intro">
          <span className="hero-badge mono">Новый аккаунт</span>
          <h1>Создайте профиль</h1>
          <p className="auth-lead">Зарегистрируйтесь, чтобы получить доступ к дашборду и метрикам агентов.</p>
        </div>
        <div className="form-card auth-card">
          <div className="auth-tabs">
            <Link to="/login" className="auth-tab">
              Вход
            </Link>
            <span className="auth-tab active">Регистрация</span>
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
              <span className="field-label">Email (необязательно)</span>
              <input
                className="field-input"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>
            <label className="field-span-2">
              <span className="field-label">Пароль</span>
              <input
                className="field-input"
                type="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {error && <p className="form-error">{error}</p>}
            <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
              {submitting ? "Регистрация…" : "Зарегистрироваться"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
