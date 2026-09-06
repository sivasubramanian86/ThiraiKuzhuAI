/**
 * Thirai Kuzhu AI — Internationalization (i18n) Module
 * 
 * Modular architecture: Loads individual language files from ./locales/
 * Supports 22 Global & Indian Cinema Languages (14 World Cinema + 8 Indian Traditions).
 */

import { en } from './locales/en';
import { fr } from './locales/fr';
import { ja } from './locales/ja';
import { ko } from './locales/ko';
import { es } from './locales/es';
import { de } from './locales/de';
import { it } from './locales/it';
import { zh } from './locales/zh';
import { zh_hk } from './locales/zh_hk';
import { ar } from './locales/ar';
import { pt } from './locales/pt';
import { ru } from './locales/ru';
import { sv } from './locales/sv';
import { tr } from './locales/tr';
import { ta } from './locales/ta';
import { hi } from './locales/hi';
import { te } from './locales/te';
import { ml } from './locales/ml';
import { kn } from './locales/kn';
import { bn } from './locales/bn';
import { mr } from './locales/mr';
import { pa } from './locales/pa';

export const LOCALES = {
  en,
  fr,
  ja,
  ko,
  es,
  de,
  it,
  zh,
  'zh-HK': zh_hk,
  ar,
  pt,
  ru,
  sv,
  tr,
  ta,
  hi,
  te,
  ml,
  kn,
  bn,
  mr,
  pa
};

export const SUPPORTED_LANGUAGES = [
  // Global World Cinema (14)
  { code: 'en', name: 'English (Global SMPTE/DCI)' },
  { code: 'fr', name: 'Français (Cannes / Auteur)' },
  { code: 'ja', name: '日本語 (Anime / Sakuga)' },
  { code: 'ko', name: '한국어 (K-Drama / Chungmuro)' },
  { code: 'es', name: 'Español (Iberoamérica)' },
  { code: 'de', name: 'Deutsch (Berlinale)' },
  { code: 'it', name: 'Italiano (Cinecittà)' },
  { code: 'zh', name: '简体中文 (Mainland VFX)' },
  { code: 'zh-HK', name: '繁體中文 (香港武打動作)' },
  { code: 'ar', name: 'العربية (MENA / RTL)', dir: 'rtl' },
  { code: 'pt', name: 'Português (Brasil/Portugal)' },
  { code: 'ru', name: 'Русский (Авторское кино)' },
  { code: 'sv', name: 'Svenska (Nordisk Noir)' },
  { code: 'tr', name: 'Türkçe (Dizi & Sinema)' },

  // Indian Cinematic Traditions (8)
  { code: 'ta', name: 'தமிழ் (Kollywood / திரை குழு)' },
  { code: 'hi', name: 'हिन्दी (Bollywood / OTT)' },
  { code: 'te', name: 'తెలుగు (Tollywood Epics)' },
  { code: 'ml', name: 'മലയാളം (Mollywood Realism)' },
  { code: 'kn', name: 'ಕನ್ನಡ (Sandalwood)' },
  { code: 'bn', name: 'বাংলা (Tollygunge / Ray)' },
  { code: 'mr', name: 'मराठी (Parallel Cinema)' },
  { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi Cinema)' }
];

/**
 * Retrieves translations dictionary for the given language code.
 * Falls back safely to English if language is not supported.
 * 
 * @param {string} langCode Target ISO language code.
 * @returns {Object} Localized dictionary.
 */
export function getTranslations(langCode) {
  return LOCALES[langCode] || LOCALES.en;
}

/**
 * Determines whether the given language uses Right-to-Left (RTL) writing direction.
 * 
 * @param {string} langCode Target ISO language code.
 * @returns {boolean} True if RTL (e.g. Arabic), false otherwise.
 */
export function isRTL(langCode) {
  return langCode === 'ar';
}
