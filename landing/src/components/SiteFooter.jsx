import { useState } from "react";
import { Link } from "react-router-dom";
import { useCookieConsent } from "../context/CookieConsentContext.jsx";
import { OPERATOR } from "../legal/operatorInfo.js";
import { MASCOT_FILE } from "../constants.js";

export default function SiteFooter() {
  const { openCookiePreferences } = useCookieConsent();
  const mascotSrc = `${import.meta.env.BASE_URL}${MASCOT_FILE}`;
  const [email, setEmail] = useState("");
  const [consentPd, setConsentPd] = useState(false);
  const [consentThird, setConsentThird] = useState(false);
  const [done, setDone] = useState(false);

  function submitNewsletter(e) {
    e.preventDefault();
    if (!consentPd || !consentThird) return;
    setDone(true);
  }

  return (
    <footer className="site-footer">
      <div className="wrap footer-grid">
        <div className="footer-col footer-brand">
          <div className="logo footer-logo">
            <img src={mascotSrc} alt="" className="logo-mascot logo-mascot--footer" width={32} height={32} decoding="async" />
            <span>GigaBrowser Agent</span>
          </div>
          <p className="footer-tagline">Проектный практикум · ИИ-безопасность в браузере</p>
        </div>

        <div className="footer-col">
          <h3 className="footer-heading">Документы</h3>
          <nav className="footer-nav" aria-label="Юридическая информация">
            <Link to="/privacy">Политика обработки персональных данных</Link>
            <Link to="/cookies">Политика в отношении cookie</Link>
            <button type="button" className="footer-link-btn" onClick={openCookiePreferences}>
              Настройки cookie
            </button>
            <Link to="/" state={{ scrollTo: "contact" }}>
              Форма обратной связи
            </Link>
          </nav>
        </div>

        <div className="footer-col footer-newsletter">
          <h3 className="footer-heading">Подписка на новости</h3>
          {done ? (
            <p className="footer-note">Запрос учтён (демо: фактическая рассылка требует подключения сервиса отправки).</p>
          ) : (
            <form className="newsletter-form" onSubmit={submitNewsletter}>
              <label className="field footer-field">
                <span className="visually-hidden">E-mail</span>
                <input
                  className="field-input"
                  type="email"
                  name="newsletter_email"
                  autoComplete="email"
                  placeholder="E-mail"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </label>
              <label className="consent-row consent-row-compact">
                <input
                  type="checkbox"
                  checked={consentPd}
                  onChange={(e) => setConsentPd(e.target.checked)}
                  required
                />
                <span>
                  Согласен(на) на обработку e-mail в целях направления информационных и новостных материалов, срок — до
                  отзыва; ознакомлен(а) с <Link to="/privacy">Политикой</Link>.
                </span>
              </label>
              <label className="consent-row consent-row-compact">
                <input
                  type="checkbox"
                  checked={consentThird}
                  onChange={(e) => setConsentThird(e.target.checked)}
                  required
                />
                <span>
                  Отдельное согласие на передачу e-mail оператору рассылки / ESP при подключении соответствующего
                  сервиса (перечень в Политике).
                </span>
              </label>
              <button type="submit" className="btn btn-ghost btn-block" disabled={!consentPd || !consentThird}>
                Подписаться
              </button>
            </form>
          )}
        </div>
      </div>

      <div className="wrap footer-requisites" aria-label="Сведения о владельце сайта по ФЗ № 149">
        <h3 className="footer-requisites-title">Владелец сайта</h3>
        <p className="footer-requisites-note">
          Сведения в соответствии с частью 2 статьи 10 Федерального закона от 27.07.2006 № 149-ФЗ «Об информации,
          информационных технологиях и о защите информации».
        </p>
        <dl className="footer-requisites-list">
          <div className="footer-req-row">
            <dt>Полное наименование</dt>
            <dd>{OPERATOR.name}</dd>
          </div>
          <div className="footer-req-row">
            <dt>Адрес места нахождения</dt>
            <dd>{OPERATOR.address}</dd>
          </div>
          <div className="footer-req-row">
            <dt>ИНН</dt>
            <dd>{OPERATOR.inn}</dd>
          </div>
          <div className="footer-req-row">
            <dt>Контактный телефон</dt>
            <dd>
              <a href={`tel:${OPERATOR.phone.replace(/[^\d+]/g, "")}`}>{OPERATOR.phone}</a>
            </dd>
          </div>
          <div className="footer-req-row">
            <dt>E-mail</dt>
            <dd>
              <a href={`mailto:${OPERATOR.emailPd}`}>{OPERATOR.emailPd}</a>
            </dd>
          </div>
        </dl>
      </div>

      <div className="wrap footer-bottom">
        <span>© {new Date().getFullYear()} GigaBrowser Agent</span>
        <span className="mono">GigaChat</span>
      </div>
    </footer>
  );
}
