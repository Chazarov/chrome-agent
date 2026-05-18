import { useEffect } from "react";
import { useCookieConsent } from "../context/CookieConsentContext.jsx";

export default function ExternalFontsLoader() {
  const { prefs } = useCookieConsent();

  useEffect(() => {
    const ids = ["gba-fonts-preconnect-google", "gba-fonts-preconnect-gstatic", "gba-fonts-stylesheet"];
    for (const id of ids) {
      const el = document.getElementById(id);
      if (el) el.remove();
    }
    if (!prefs.functional) return;

    const pre1 = document.createElement("link");
    pre1.id = "gba-fonts-preconnect-google";
    pre1.rel = "preconnect";
    pre1.href = "https://fonts.googleapis.com";

    const pre2 = document.createElement("link");
    pre2.id = "gba-fonts-preconnect-gstatic";
    pre2.rel = "preconnect";
    pre2.href = "https://fonts.gstatic.com";
    pre2.crossOrigin = "anonymous";

    const css = document.createElement("link");
    css.id = "gba-fonts-stylesheet";
    css.rel = "stylesheet";
    css.href =
      "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Manrope:wght@400;500;600;700;800&display=swap";

    document.head.append(pre1, pre2, css);
  }, [prefs.functional]);

  return null;
}
