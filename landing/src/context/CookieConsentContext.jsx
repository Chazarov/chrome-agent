import { createContext, useCallback, useContext, useMemo, useState } from "react";

const STORAGE_KEY = "gba_cookie_consent_v1";

const defaultPrefs = {
  necessary: true,
  functional: false,
  analytics: false,
  marketing: false,
  choiceMade: false,
};

function readStored() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return { ...defaultPrefs, ...parsed, necessary: true };
  } catch {
    return null;
  }
}

const CookieConsentContext = createContext(null);

export function CookieConsentProvider({ children }) {
  const [prefs, setPrefs] = useState(() => {
    if (typeof window === "undefined") return defaultPrefs;
    return readStored() ?? defaultPrefs;
  });
  const [editorOpen, setEditorOpen] = useState(false);

  const persist = useCallback((next) => {
    setPrefs(next);
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      /* ignore quota */
    }
  }, []);

  const acceptAll = useCallback(() => {
    persist({
      necessary: true,
      functional: true,
      analytics: true,
      marketing: true,
      choiceMade: true,
    });
    setEditorOpen(false);
  }, [persist]);

  const acceptNecessaryOnly = useCallback(() => {
    persist({
      necessary: true,
      functional: false,
      analytics: false,
      marketing: false,
      choiceMade: true,
    });
    setEditorOpen(false);
  }, [persist]);

  const saveCustom = useCallback((partial) => {
    persist({
      necessary: true,
      functional: Boolean(partial.functional),
      analytics: Boolean(partial.analytics),
      marketing: Boolean(partial.marketing),
      choiceMade: true,
    });
    setEditorOpen(false);
  }, [persist]);

  const openCookiePreferences = useCallback(() => {
    setEditorOpen(true);
  }, []);

  const closeCookiePreferences = useCallback(() => {
    setEditorOpen(false);
  }, []);

  const value = useMemo(
    () => ({
      prefs,
      acceptAll,
      acceptNecessaryOnly,
      saveCustom,
      editorOpen,
      openCookiePreferences,
      closeCookiePreferences,
    }),
    [prefs, acceptAll, acceptNecessaryOnly, saveCustom, editorOpen, openCookiePreferences, closeCookiePreferences]
  );

  return <CookieConsentContext.Provider value={value}>{children}</CookieConsentContext.Provider>;
}

export function useCookieConsent() {
  const ctx = useContext(CookieConsentContext);
  if (!ctx) throw new Error("useCookieConsent must be used within CookieConsentProvider");
  return ctx;
}
