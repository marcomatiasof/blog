import { getCollection } from 'astro:content';
import { SUPPORTED_LOCALES, SITE_URL } from '../i18n/constants';
import { getAlternates } from '../i18n/utils';

export const GET = async () => {
  const allPosts = await getCollection('blog', (post) => !post.data.draft);

  // Group posts by translationKey to build hreflang groups
  const translationKeysSeen = new Set();
  const articleUrlSets = [];

  for (const post of allPosts) {
    if (translationKeysSeen.has(post.data.translationKey)) continue;
    translationKeysSeen.add(post.data.translationKey);

    const alternates = getAlternates(post.data.translationKey, allPosts);
    const urls = SUPPORTED_LOCALES
      .filter((locale) => alternates[locale] !== null)
      .map((locale) => ({
        loc: alternates[locale].url,
        locale,
        lastmod: post.data.date.toISOString().split('T')[0],
      }));

    articleUrlSets.push({ translationKey: post.data.translationKey, urls, alternates });
  }

  // Home pages for each locale
  const homeUrls = SUPPORTED_LOCALES.map((locale) => ({
    loc: `${SITE_URL}/${locale}/`,
    locale,
    alternates: SUPPORTED_LOCALES.map((l) => ({ locale: l, href: `${SITE_URL}/${l}/` })),
  }));

  const xmlUrls = [];

  // Home pages
  for (const home of homeUrls) {
    const xhtmlLinks = home.alternates
      .map((a) => `      <xhtml:link rel="alternate" hreflang="${a.locale}" href="${a.href}"/>`)
      .join('\n');
    const xDefault = `      <xhtml:link rel="alternate" hreflang="x-default" href="${SITE_URL}/en/"/>`;

    xmlUrls.push(`  <url>
    <loc>${home.loc}</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
${xhtmlLinks}
${xDefault}
  </url>`);
  }

  // Article pages
  for (const set of articleUrlSets) {
    for (const urlEntry of set.urls) {
      const xhtmlLinks = set.urls
        .map((u) => `      <xhtml:link rel="alternate" hreflang="${u.locale}" href="${u.loc}"/>`)
        .join('\n');
      const enVersion = set.alternates['en'];
      const xDefault = enVersion
        ? `      <xhtml:link rel="alternate" hreflang="x-default" href="${enVersion.url}"/>`
        : '';

      xmlUrls.push(`  <url>
    <loc>${urlEntry.loc}</loc>
    <lastmod>${urlEntry.lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
${xhtmlLinks}
${xDefault}
  </url>`);
    }
  }

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
>
${xmlUrls.join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
