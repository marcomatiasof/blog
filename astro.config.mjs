// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://aimonetiza.com', // Coloque seu dominio oficial aqui depois
  integrations: [sitemap()]
});