/**
 * src/pages/rss/[category].xml.ts
 * Category-specific RSS 2.0 Feed Generator.
 */
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE_URL } from '../../i18n/constants';
import { CATEGORIES } from '../[lang]/categoria/[category].astro';

export async function getStaticPaths() {
  return CATEGORIES.map((cat) => ({
    params: { category: cat.slug },
  }));
}

export const GET: APIRoute = async ({ params }) => {
  const category = params.category as string;
  const allPosts = await getCollection('blog', (post) => !post.data.draft);

  const categoryPosts = allPosts.filter((post) => {
    const tags = (post.data.tags || []).map((t) => t.toLowerCase());
    return tags.includes(category.toLowerCase());
  });

  categoryPosts.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

  const rssXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>TechFlow — ${category.toUpperCase()}</title>
    <link>${SITE_URL}</link>
    <description>Notícias e análises atualizadas sobre ${category}</description>
    <language>pt-BR</language>
    ${categoryPosts
      .map((post) => {
        const url = `${SITE_URL}/${post.data.locale}/${post.data.slug}/`;
        const title = post.data.title.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const desc = post.data.description.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return `
    <item>
      <title>${title}</title>
      <link>${url}</link>
      <guid>${url}</guid>
      <pubDate>${post.data.date.toUTCString()}</pubDate>
      <description>${desc}</description>
    </item>`;
      })
      .join('')}
  </channel>
</rss>`;

  return new Response(rssXml.trim(), {
    status: 200,
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
    },
  });
};
