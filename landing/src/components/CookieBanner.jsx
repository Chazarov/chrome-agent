import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useCookieConsent } from "../context/CookieConsentContext.jsx";

export default function CookieBanner() {
  const { prefs, acceptAll, acceptNecessaryOnly, saveCustom, editorOpen, closeCookiePreferences } =
    useCookieConsent();
  const [step, setStep] = useState("main");
  const [draft, setDraft] = useState({
    functional: prefs.functional,
    analytics: prefs.analytics,
    marketing: prefs.marketing,
  });

  useEffect(() => {
    if (editorOpen) {
      setStep("settings");
    }
  }, [editorOpen]);

  useEffect(() => {
    if (editorOpen) {
      setDraft({
        functional: prefs.functional,
        analytics: prefs.analytics,
        marketing: prefs.marketing,
      });
    }
  }, [editorOpen, prefs.functional, prefs.analytics, prefs.marketing]);

  const visible = !prefs.choiceMade || editorOpen;
  const showSettings = step === "settings";

  if (!visible) return null;

  return (
    <div className="cookie-banner" role="dialog" aria-modal="true" aria-labelledby="cookie-banner-title">
      <div className="cookie-banner-panel">
        <h2 id="cookie-banner-title" className="cookie-banner-title">
          Файлы cookie и обработка данных
        </h2>
        <p className="cookie-banner-text">
          Мы используем файлы cookie и сходные технологии:{" "}
          <strong>строго необходимые</strong> — для сохранения ваших настроек и безопасности;{" "}
          <strong>функциональные</strong> — для подключения шрифтов и удобства сайта;{" "}
          <strong>аналитические</strong> и <strong>маркетинговые</strong> — только если вы дали согласие. Подробнее — в{" "}
          <Link to="/cookies" className="cookie-banner-link" onClick={closeCookiePreferences}>
            Политике в отношении cookie
          </Link>{" "}
          и в{" "}
          <Link to="/privacy" className="cookie-banner-link" onClick={closeCookiePreferences}>
            Политике обработки персональных данных
          </Link>
          .
        </p>

        {!showSettings ? (
          <div className="cookie-banner-actions">
            <button type="button" className="btn btn-ghost" onClick={acceptNecessaryOnly}>
              Только необходимые
            </button>
            <button type="button" className="btn btn-ghost" onClick={() => setStep("settings")}>
              Настроить
            </button>
            <button type="button" className="btn btn-primary" onClick={acceptAll}>
              Принять все
            </button>
          </div>
        ) : (
          <div className="cookie-settings">
            <label className="cookie-toggle-row">
              <input type="checkbox" checked disabled />
              <span>
                <strong>Строго необходимые</strong> — хранение выбора cookie, базовая работа сайта (отключить нельзя).
              </span>
            </label>
            <label className="cookie-toggle-row">
              <input
                type="checkbox"
                checked={draft.functional}
                onChange={(e) => setDraft((d) => ({ ...d, functional: e.target.checked }))}
              />
              <span>
                <strong>Функциональные</strong> — подключение шрифтов с CDN Google (без целей аналитики на стороне
                сайта).
              </span>
            </label>
            <label className="cookie-toggle-row">
              <input
                type="checkbox"
                checked={draft.analytics}
                onChange={(e) => setDraft((d) => ({ ...d, analytics: e.target.checked }))}
              />
              <span>
                <strong>Аналитические</strong> — в текущей версии сайта не активируют сторонние счётчики; опция
                зарезервирована на будущее.
              </span>
            </label>
            <label className="cookie-toggle-row">
              <input
                type="checkbox"
                checked={draft.marketing}
                onChange={(e) => setDraft((d) => ({ ...d, marketing: e.target.checked }))}
              />
              <span>
                <strong>Маркетинговые</strong> — в текущей версии не используются; включение означает согласие на
                возможное будущее использование после обновления Политики.
              </span>
            </label>
            <div className="cookie-banner-actions">
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => {
                  if (prefs.choiceMade) {
                    closeCookiePreferences();
                  } else {
                    setStep("main");
                  }
                }}
              >
                {prefs.choiceMade ? "Закрыть" : "Назад"}
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  saveCustom(draft);
                  setStep("main");
                }}
              >
                Сохранить выбор
              </button>
            </div>
          </div>
        )}

        <p className="cookie-banner-foot">
          Изменить выбор можно через ссылку «Настройки cookie» в подвале сайта
          {editorOpen ? (
            <>
              {" "}
              или{" "}
              <button type="button" className="cookie-banner-inline-btn" onClick={closeCookiePreferences}>
                закрыть панель
              </button>
            </>
          ) : null}
          .
        </p>
      </div>
    </div>
  );
}
