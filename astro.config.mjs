// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://techflow.com', // Coloque seu dominio oficial aqui depois
  integrations: [sitemap()]
});