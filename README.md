# TechFlow Blog — Multilingual Tech & Productivity Blog

A multilingual (EN/PT/ES) technology and productivity blog built with **Astro** and deployed on **Cloudflare Pages**.

## Features

- 🌐 **Multilingual**: English, Portuguese, Brazilian Portuguese, Spanish
- 🚀 **Astro SSG**: Static site generation for maximum performance
- ☁️ **Cloudflare Pages**: Edge-deployed with automatic language detection
- 🔍 **SEO**: Full hreflang, Open Graph, Twitter Card, and sitemap support
- 💰 **AdSense-ready**: Async placeholder slots that won't block rendering
- ⚡ **Core Web Vitals**: Lazy images, inline critical CSS, font preconnect

## Project Structure

```
src/
├── content/
│   ├── config.ts          ← Zod schema for all blog posts
│   └── blog/
│       ├── en/            ← English articles
│       ├── pt/            ← Portuguese articles
│       └── es/            ← Spanish articles
├── i18n/
│   ├── constants.ts       ← Locales, site URL, locale names/flags
│   ├── ui.ts              ← All UI strings by locale
│   └── utils.ts           ← Helpers: getLangFromUrl, getAlternates, etc.
├── layouts/
│   └── BaseLayout.astro   ← Root layout: SEO, hreflang, AdSense slot
├── components/
│   ├── Header.astro
│   ├── Footer.astro
│   ├── LanguagePicker.astro
│   └── ArticleCard.astro
└── pages/
    ├── index.astro         ← Fallback redirect (Cloudflare Function handles real redirects)
    ├── sitemap.xml.ts      ← Custom multilingual sitemap with xhtml:link
    └── [lang]/
        ├── index.astro     ← Locale home page
        └── [slug].astro    ← Article page

functions/
└── index.js               ← Cloudflare Pages Function: language detection & redirect
```

## Writing Articles

Create a new Markdown file in `src/content/blog/{locale}/your-slug.md`:

```markdown
---
title: "Your Article Title"
description: "A compelling description for SEO"
date: 2026-09-14
locale: en          # en | pt | es
slug: your-slug
translationKey: unique-key-shared-across-translations
author: Your Name
tags: [tag1, tag2]
image: /images/your-image.jpg
---

Your content here...
```

**Important**: All translations of the same article must share the same `translationKey`.

## Commands

| Command | Action |
|---------|--------|
| `npm run dev` | Start local dev server at `localhost:4321` |
| `npm run build` | Build for production to `./dist/` |
| `npm run preview` | Preview build locally |
| `npm run check` | Run TypeScript checks |

## Deployment

1. Push to GitHub
2. Connect repo to [Cloudflare Pages](https://pages.cloudflare.com)
3. Build command: `npm run build`
4. Output directory: `dist`
5. The `functions/index.js` is picked up automatically by Cloudflare Pages

## AdSense Setup

When your AdSense account is approved:

1. Open `src/layouts/BaseLayout.astro`
2. Find the commented-out `<script>` tag
3. Replace `ca-pub-XXXXXXXXXX` with your publisher ID
4. Uncomment the script tag

The script is already configured to load `async` + `crossorigin` to never block rendering.

## Configuration

Update these before going live:

- `src/i18n/constants.ts` → `SITE_URL` (your real domain)
- `astro.config.mjs` → `site` property
- `wrangler.toml` → `name` (your Cloudflare Pages project name)
