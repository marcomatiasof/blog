/**
 * src/pages/news-sitemap.xml.ts
 * Dynamic Google News Sitemap generator.
 * Follows Google News Publisher Guidelines (http://www.google.com/schemas/sitemap-news/0.9).
 */
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE_URL } from '../i18n/constants';

export const GET: APIRoute = async () => {
  const allPosts = await getCollection('blog', (post) => !post.data.draft);

  // Sort by date descending
  allPosts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

  // Filter posts published in the last 48 hours (or fallback to top 20 recent posts for news index)
  const now = new Date();
  const fortyEightHoursAgo = new Date(now.getTime() - 48 * 60 * 60 * 1000);
  
  let newsPosts = allPosts.filter((post) => post.data.date >= fortyEightHoursAgo);
  if (newsPosts.length === 0) {
    newsPosts = allPosts.slice(0, 20);
  }

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  ${newsPosts
    .map((post) => {
      const url = `${SITE_URL}/${post.data.locale}/${post.data.slug}/`;
      const pubDate = post.data.date.toISOString();
      const title = post.data.title.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      const lang = post.data.locale;

      return `
  <url>
    <loc>${url}</loc>
    <news:news>
      <news:publication>
        <news:name>TechFlow News</news:name>
        <news:language>${lang}</news:language>
      </news:publication>
      <news:publication_date>${pubDate}</news:publication_date>
      <news:title>${title}</news:title>
    </news:news>
  </url>`;
    })
    .join('')}
</urlset>`;

  return new Response(sitemapXml.trim(), {
    status: 200,
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
