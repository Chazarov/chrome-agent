import { useState } from "react";
import { Link } from "react-router-dom";

export default function ContactSection() {
  const [fio, setFio] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [message, setMessage] = useState("");
  const [consentPd, setConsentPd] = useState(false);
  const [consentThird, setConsentThird] = useState(false);
  const [sent, setSent] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    if (!consentPd || !consentThird) return;
    setSent(true);
  }

  return (
    <section className="block" id="contact">
      <div className="wrap">
        <div className="section-head">
          <h2>Обратная связь</h2>
        </div>

        <div className="form-card">
          {sent ? (
            <p className="form-success">
              Спасибо. В демонстрационной сборке данные не отправляются на сервер: подключите обработчик (API, почтовый
              сервис) и замените заглушку в коде формы перед промышленной эксплуатацией.
            </p>
          ) : (
            <form className="pd-form" onSubmit={handleSubmit} noValidate>
              <div className="form-grid">
                <label className="field">
                  <span className="field-label">ФИО *</span>
                  <input
                    className="field-input"
                    name="fio"
                    autoComplete="name"
                    value={fio}
                    onChange={(e) => setFio(e.target.value)}
                    required
                  />
                </label>
                <label className="field">
                  <span className="field-label">E-mail *</span>
                  <input
                    className="field-input"
                    name="email"
                    type="email"
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </label>
                <label className="field field-span-2">
                  <span className="field-label">Телефон</span>
                  <input
                    className="field-input"
                    name="phone"
                    type="tel"
                    autoComplete="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                  />
                </label>
                <label className="field field-span-2">
                  <span className="field-label">Текст обращения *</span>
                  <textarea
                    className="field-input field-textarea"
                    name="message"
                    rows={4}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    required
                  />
                </label>
              </div>

              <div className="consent-box">
                <label className="consent-row">
                  <input
                    type="checkbox"
                    checked={consentPd}
                    onChange={(e) => setConsentPd(e.target.checked)}
                    required
                  />
                  <span>
                    Я добровольно, конкретно, информированно и однозначно даю согласие оператору на обработку моих
                    персональных данных: <strong>фамилия, имя, отчество (при наличии)</strong>,{" "}
                    <strong>адрес электронной почты</strong>, <strong>номер телефона (если указан)</strong>,{" "}
                    <strong>текст обращения</strong>, а также автоматически фиксируемые при обращении технические данные
                    (дата и время запроса, IP-адрес, user-agent браузера) — в целях рассмотрения обращения, обратной
                    связи и ведения переписки по теме запроса. Ознакомлен(а) с{" "}
                    <Link to="/privacy">Политикой обработки персональных данных</Link>.
                  </span>
                </label>

                <label className="consent-row">
                  <input
                    type="checkbox"
                    checked={consentThird}
                    onChange={(e) => setConsentThird(e.target.checked)}
                    required
                  />
                  <span>
                    Я даю <strong>отдельное согласие</strong> на передачу моих персональных данных третьим лицам —
                    хостинг-провайдеру и иным подрядчикам, привлекаемым оператором для обработки обращений (в объёме и
                    на условиях, указанных в Политике), в том числе при использовании сервисов доставки электронных
                    сообщений и CRM, если это потребуется для ответа на обращение.
                  </span>
                </label>
              </div>

              <button className="btn btn-primary form-submit" type="submit" disabled={!consentPd || !consentThird}>
                Отправить обращение
              </button>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
