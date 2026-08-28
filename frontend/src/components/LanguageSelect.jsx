import { useLanguage } from "../LanguageContext";
import { LANGUAGES } from "../i18n";

export default function LanguageSelect() {
  const { lang, setLang } = useLanguage();

  return (
    <select
      value={lang}
      onChange={(e) => setLang(e.target.value)}
      title="Language"
      className="bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm h-12
                 focus:outline-none focus:border-neon-cyan/60"
    >
      {LANGUAGES.map((l) => (
        <option key={l.code} value={l.code}>
          {l.label}
        </option>
      ))}
    </select>
  );
}
