import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { translate, LANGUAGES } from "./i18n";

const LanguageContext = createContext(null);

const STORAGE_KEY = "gokle_lang";

function detectInitialLang() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored && LANGUAGES.some((l) => l.code === stored)) return stored;
  const browserLang = navigator.language?.slice(0, 2);
  if (LANGUAGES.some((l) => l.code === browserLang)) return browserLang;
  return "uz";
}

export function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(detectInitialLang);

  const setLang = useCallback((code) => {
    setLangState(code);
    localStorage.setItem(STORAGE_KEY, code);
  }, []);

  const t = useCallback((key) => translate(lang, key), [lang]);

  const value = useMemo(() => ({ lang, setLang, t }), [lang, setLang, t]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage must be used within LanguageProvider");
  return ctx;
}
