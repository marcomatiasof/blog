export const SITE_NAME = 'TechFlow';
export const SITE_URL = 'https://www.techflow.blog';
export const SITE_DESCRIPTION = 'Notícias, análises e tendências em política, economia, esportes, viagens e tecnologia.';
export const SUPPORTED_LOCALES = ['en', 'pt', 'es'] as const;
export const DEFAULT_LOCALE = 'en' as const;

export type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];

export const LOCALE_NAMES: Record<SupportedLocale, string> = {
  en: 'English',
  pt: 'Português',
  es: 'Español',
};

export const LOCALE_FLAGS: Record<SupportedLocale, string> = {
  en: '🇺🇸',
  pt: '🇧🇷',
  es: '🇪🇸',
};
