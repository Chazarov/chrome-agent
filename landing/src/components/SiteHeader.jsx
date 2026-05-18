import { Link } from "react-router-dom";
import { MASCOT_FILE, ZIP_NAME } from "../constants.js";

export default function SiteHeader() {
  const zipHref = `${import.meta.env.BASE_URL}${ZIP_NAME}`;
  const mascotSrc = `${import.meta.env.BASE_URL}${MASCOT_FILE}`;

  return (
    <header className="site-header">
      <div className="wrap header-inner">
        <Link to="/" className="logo" aria-label="На главную">
          <img src={mascotSrc} alt="" className="logo-mascot" width={40} height={40} decoding="async" />
          <span>GigaBrowser Agent</span>
        </Link>
        <div className="nav-actions">
          <Link className="btn btn-ghost" to="/" state={{ scrollTo: "features" }}>
            Возможности
          </Link>
          <Link className="btn btn-ghost" to="/" state={{ scrollTo: "contact" }}>
            Контакты
          </Link>
          <a className="btn btn-primary" href={zipHref} download={ZIP_NAME}>
            Скачать архив
          </a>
        </div>
      </div>
    </header>
  );
}
