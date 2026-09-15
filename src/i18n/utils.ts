import { ui, type UIKey } from './ui';
import {
  SUPPORTED_LOCALES,
  DEFAULT_LOCALE,
  SITE_URL,
  type SupportedLocale,
} from './constants';
import type { CollectionEntry } from 'astro:content';

/**
 * Extracts the locale from an Astro URL object.
 * Expects URLs like /en/slug, /pt/slug, /es/slug
 */
export function getLangFromUrl(url: URL): SupportedLocale {
  const [, lang] = url.pathname.split('/');
  if (SUPPORTED_LOCALES.includes(lang as SupportedLocale)) {
    return lang as SupportedLocale;
  }
  return DEFAULT_LOCALE;
}

/**
 * Returns a translation function `t(key)` for the given locale.
 * Falls back to the default locale if a key is missing.
 */
export function useTranslations(lang: SupportedLocale) {
  return function t(key: UIKey): string {
    const localeStrings = ui[lang] as Record<string, string>;
    const defaultStrings = ui[DEFAULT_LOCALE] as Record<string, string>;
    return localeStrings[key] ?? defaultStrings[key] ?? key;
  };
}

/**
 * Given a translationKey and all blog posts, returns a map of
 * { locale -> { slug, url } } for every translation that exists.
 */
export function getAlternates(
  translationKey: string,
  allPosts: CollectionEntry<'blog'>[],
): Record<SupportedLocale, { slug: string; url: string } | null> {
  const result = {} as Record<SupportedLocale, { slug: string; url: string } | null>;

  for (const locale of SUPPORTED_LOCALES) {
    const match = allPosts.find(
      (p) => p.data.translationKey === translationKey && p.data.locale === locale,
    );
    if (match) {
      result[locale] = {
        slug: match.data.slug,
        url: `${SITE_URL}/${locale}/${match.data.slug}/`,
      };
    } else {
      result[locale] = null;
    }
  }

  return result;
}

/**
 * Returns an array of hreflang alternate objects suitable for <head> tags.
 * Includes x-default pointing to the EN version.
 */
export function getHreflangAlternates(
  translationKey: string,
  allPosts: CollectionEntry<'blog'>[],
) {
  const alternates = getAlternates(translationKey, allPosts);
  const hreflang: Array<{ hreflang: string; href: string }> = [];

  for (const [locale, data] of Object.entries(alternates)) {
    if (data) {
      hreflang.push({ hreflang: locale, href: data.url });
    }
  }

  // x-default points to English version
  const enVersion = alternates[DEFAULT_LOCALE];
  if (enVersion) {
    hreflang.push({ hreflang: 'x-default', href: enVersion.url });
  }

  return hreflang;
}

/**
 * Returns the locale home URL for a given locale.
 */
export function getLocaleHome(locale: SupportedLocale): string {
  return `/${locale}/`;
}

/**
 * Formats a date for display in a given locale.
 */
export function formatDate(date: Date, locale: SupportedLocale): string {
  const localeMap: Record<SupportedLocale, string> = {
    en: 'en-US',
    pt: 'pt-BR',
    es: 'es-ES',
  };
  return date.toLocaleDateString(localeMap[locale], {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
