import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import "../App.css";
import ContactSection from "../components/ContactSection.jsx";
import { MASCOT_FILE, ZIP_NAME } from "../constants.js";

export default function HomePage() {
  const location = useLocation();
  const zipHref = `${import.meta.env.BASE_URL}${ZIP_NAME}`;
  const mascotSrc = `${import.meta.env.BASE_URL}${MASCOT_FILE}`;

  useEffect(() => {
    const id = location.state?.scrollTo;
    if (typeof id === "string") {
      const el = document.getElementById(id);
      if (el) {
        requestAnimationFrame(() => el.scrollIntoView({ behavior: "smooth", block: "start" }));
      }
    }
  }, [location]);

  return (
    <div className="app">
      <section className="hero">
        <div className="hero-gradient" aria-hidden />
        <div className="wrap hero-inner hero-grid">
          <div className="hero-copy">
            <div className="hero-badge mono">GigaChat · браузер · безопасность</div>
            <h1>ИИ-агент, который оценивает безопасность сайтов, пока вы сёрфите</h1>
            <p className="hero-lead">
              Расширение для браузера на русскоязычной модели GigaChat: от базовых проверок SSL и реестра РКН до
              сложных сценариев — фейковые биржи, инвестиционные ловушки, поддельные магазины и скрытый сбор данных.
            </p>
            <div className="hero-cta">
              <a className="btn btn-primary" href={zipHref} download={ZIP_NAME}>
                Скачать проект (ZIP)
              </a>
              <a className="btn btn-ghost" href="#compare">
                Чем мы отличаемся
              </a>
            </div>
            <p className="hero-note">
              Архив собирается командой <code className="mono">npm run zip</code> и содержит исходники проекта без{" "}
              <code className="mono">node_modules</code>.
            </p>
            <div className="hero-stats">
              <div className="stat">
                <strong>6+</strong>
                <span>базовых классов проверок</span>
              </div>
              <div className="stat">
                <strong>7</strong>
                <span>сложных сценариев анализа</span>
              </div>
              <div className="stat">
                <strong>AI</strong>
                <span>контекст и рассуждения, не шаблоны</span>
              </div>
            </div>
          </div>

          <div className="hero-mascot-col">
            <figure className="hero-mascot-figure">
              <div className="hero-mascot-ring" aria-hidden />
              <img
                src={mascotSrc}
                alt="Маскот GigaBrowser Agent — агент соболь"
                className="hero-mascot-img"
                width={560}
                height={560}
                loading="eager"
                decoding="async"
              />
              <figcaption className="hero-mascot-caption mono">Агент Соболь</figcaption>
            </figure>
          </div>
        </div>
      </section>

      <section className="block alt" id="compare">
        <div className="wrap">
          <div className="section-head">
            <h2>Почему шаблонных фильтров недостаточно</h2>
            <p>
              Классические механизмы смотрят на домен, сертификат, формы и формальные требования. Мошеннический сайт
              может всем этим соответствовать. Наш агент комбинирует сигналы и интерпретирует смысл страницы и
              репутации в сети.
            </p>
          </div>
          <div className="compare">
            <div className="compare-col bad">
              <h3>Типичный «антивред» в браузере</h3>
              <ul>
                <li>Жёсткие правила и сигнатуры</li>
                <li>Мало контекста о бизнесе и отзывах</li>
                <li>Легко обойти копией «легального» шаблона</li>
              </ul>
            </div>
            <div className="compare-col good">
              <h3>GigaBrowser Agent</h3>
              <ul>
                <li>Рассуждение на естественном языке (RU)</li>
                <li>Сбор и сверка данных из открытых источников</li>
                <li>Сложные сценарии: от крипто-разводов до фейковых HR-форм</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="block" id="features">
        <div className="wrap">
          <div className="section-head">
            <h2>Базовые проверки</h2>
            <p>Фундамент, который всё равно важен — но у нас он дополняется ИИ-интерпретацией и связкой сигналов.</p>
          </div>
          <div className="grid-2">
            <article className="card">
              <span className="tag tag-basic">База</span>
              <h3>Фишинг и подозрительные страницы</h3>
              <p>Детекция страниц, имитирующих банки, почту и сервисы, с анализом текстов и структуры.</p>
            </article>
            <article className="card">
              <span className="tag tag-basic">База</span>
              <h3>Домен и репутация</h3>
              <p>Проверка по чёрным спискам и сигналам репутации домена, возраст и аномалии регистрации.</p>
            </article>
            <article className="card">
              <span className="tag tag-basic">База</span>
              <h3>SSL и цепочка доверия</h3>
              <p>Наличие валидного HTTPS, сроки и корректность цепочки — без ложного чувства «всё ок».</p>
            </article>
            <article className="card">
              <span className="tag tag-basic">База</span>
              <h3>Формы ввода</h3>
              <p>Подозрительные поля логина/пароля, отсутствие ожидаемых защит, нетипичные сценарии сбора данных.</p>
            </article>
            <article className="card">
              <span className="tag tag-basic">База</span>
              <h3>Реестр Роскомнадзора</h3>
              <p>Сверка с реестром запрещённых ресурсов и смежные юридические сигналы.</p>
            </article>
            <article className="card">
              <span className="tag tag-basic">База</span>
              <h3>Известный malware</h3>
              <p>Сопоставление URL и артефактов с базами сигнатур вредоносного ПО.</p>
            </article>
          </div>
        </div>
      </section>

      <section className="block alt">
        <div className="wrap">
          <div className="section-head">
            <h2>Сложные сценарии</h2>
            <p>Там, где шаблоны почти бессильны — агент собирает доказательную базу и выявляет противоречия.</p>
          </div>
          <div className="grid-2">
            <article className="card">
              <span className="tag tag-advanced">Сложно</span>
              <h3>Несостоятельная организация / платформа</h3>
              <p>Сводка по открытым данным: юрлица, адреса, упоминания в СМИ и жалобы пользователей.</p>
            </article>
            <article className="card">
              <span className="tag tag-advanced">Сложно</span>
              <h3>Инвестиции и фейковые отзывы</h3>
              <p>Сопоставление отзывов на репутационных площадках с официальной информацией и «слишком ровной» картиной.</p>
            </article>
            <article className="card">
              <span className="tag tag-advanced">Сложно</span>
              <h3>Знакомства и боты</h3>
              <p>Шаблонные фото, поведение в чате, эвристики и проверки на синтетику / deepfake (по мере подключения моделей).</p>
            </article>
            <article className="card">
              <span className="tag tag-advanced">Сложно</span>
              <h3>Фейковая криптобиржа</h3>
              <p>WHOIS, обсуждения на крипто-форумах, нереалистичные обещания доходности и клоны интерфейсов.</p>
            </article>
            <article className="card">
              <span className="tag tag-advanced">Сложно</span>
              <h3>Магазин с подделками и ценами</h3>
              <p>Сравнение с рынком, отзывы, аномалии трафика и fingerprinting устройства (по политике приватности).</p>
            </article>
            <article className="card">
              <span className="tag tag-advanced">Сложно</span>
              <h3>«Работа / опросы» и кража данных</h3>
              <p>Скрытые скрипты, поведение форм, лишние поля и репутация площадки.</p>
            </article>
          </div>

          <div className="cta-band" id="download">
            <div>
              <h3>Готовы попробовать прототип?</h3>
              <p>Скачайте ZIP с исходниками проекта и соберите локально через npm.</p>
            </div>
            <a className="btn btn-primary" href={zipHref} download={ZIP_NAME}>
              Скачать {ZIP_NAME}
            </a>
          </div>
        </div>
      </section>

      <ContactSection />
    </div>
  );
}
