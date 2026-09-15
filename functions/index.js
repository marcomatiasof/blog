/**
 * functions/index.js
 * Cloudflare Pages Function — runs on every request to "/"
 *
 * Logic:
 * 1. Check preferred_locale cookie → redirect immediately if found
 * 2. Parse Accept-Language header → find best matching locale
 * 3. Fallback: map CF-IPCountry → locale
 * 4. Final fallback: "en"
 * 5. Set preferred_locale cookie (1 year) and redirect to /{locale}/
 *
 * IMPORTANT: Only runs on "/" — all other routes (articles) serve normally.
 */

const SUPPORTED_LOCALES = ['en', 'pt', 'es'];
const DEFAULT_LOCALE = 'en';

/**
 * Maps CF-IPCountry (ISO 3166-1 alpha-2) → preferred locale.
 */
const COUNTRY_TO_LOCALE = {
  // Portuguese
  PT: 'pt',
  BR: 'pt',
  AO: 'pt',
  MZ: 'pt',
  CV: 'pt',
  GW: 'pt',
  ST: 'pt',
  TL: 'pt',
  // Spanish
  ES: 'es',
  MX: 'es',
  AR: 'es',
  CO: 'es',
  CL: 'es',
  PE: 'es',
  VE: 'es',
  EC: 'es',
  BO: 'es',
  PY: 'es',
  UY: 'es',
  CR: 'es',
  PA: 'es',
  DO: 'es',
  HN: 'es',
  SV: 'es',
  GT: 'es',
  NI: 'es',
  CU: 'es',
  PR: 'es',
  GQ: 'es',
};

/**
 * Parses the Accept-Language header and returns the best matching locale.
 * Respects q-values (quality factors).
 *
 * Example: "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7" → "pt"
 */
function parseAcceptLanguage(header) {
  if (!header) return null;

  const parts = header
    .split(',')
    .map((part) => {
      const [lang, q] = part.trim().split(';q=');
      return {
        lang: lang.trim().toLowerCase(),
        q: q ? parseFloat(q) : 1.0,
      };
    })
    .sort((a, b) => b.q - a.q);

  for (const { lang } of parts) {
    // Try exact match first (e.g., "pt", "es", "en")
    const exact = lang.split('-')[0]; // strip region code
    if (SUPPORTED_LOCALES.includes(exact)) {
      return exact;
    }
  }

  return null;
}

/**
 * Parses a cookie string and returns the value for a given key.
 */
function getCookie(cookieHeader, key) {
  if (!cookieHeader) return null;
  const match = cookieHeader
    .split(';')
    .map((c) => c.trim())
    .find((c) => c.startsWith(`${key}=`));
  return match ? match.slice(key.length + 1) : null;
}

/**
 * Builds a redirect Response to /{locale}/ and sets the preferred_locale cookie.
 */
function redirectToLocale(locale, secure = true) {
  const cookieFlags = [
    `preferred_locale=${locale}`,
    'Path=/',
    'Max-Age=31536000', // 1 year
    'SameSite=Lax',
    secure ? 'Secure' : '',
  ]
    .filter(Boolean)
    .join('; ');

  return new Response(null, {
    status: 302,
    headers: {
      Location: `/${locale}/`,
      'Set-Cookie': cookieFlags,
      'Cache-Control': 'no-store, no-cache',
      Vary: 'Accept-Language, Cookie',
    },
  });
}

export async function onRequestGet(context) {
  const { request } = context;
  const url = new URL(request.url);

  // Only handle exactly "/"
  if (url.pathname !== '/') {
    return context.next();
  }

  const cookieHeader = request.headers.get('Cookie');
  const acceptLanguage = request.headers.get('Accept-Language');
  const cfCountry = request.headers.get('CF-IPCountry');

  // 1. Check preferred_locale cookie
  const cookieLocale = getCookie(cookieHeader, 'preferred_locale');
  if (cookieLocale && SUPPORTED_LOCALES.includes(cookieLocale)) {
    // Cookie found — redirect without changing the cookie
    return new Response(null, {
      status: 302,
      headers: {
        Location: `/${cookieLocale}/`,
        'Cache-Control': 'no-store',
        Vary: 'Cookie',
      },
    });
  }

  // 2. Parse Accept-Language header
  const langFromHeader = parseAcceptLanguage(acceptLanguage);
  if (langFromHeader) {
    return redirectToLocale(langFromHeader, url.protocol === 'https:');
  }

  // 3. Map country to locale
  const countryLocale = cfCountry ? COUNTRY_TO_LOCALE[cfCountry.toUpperCase()] : null;
  if (countryLocale) {
    return redirectToLocale(countryLocale, url.protocol === 'https:');
  }

  // 4. Final fallback → English
  return redirectToLocale(DEFAULT_LOCALE, url.protocol === 'https:');
}
