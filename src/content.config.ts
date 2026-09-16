import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: ({ image }) => z.object({
    title: z.string(),
    subtitle: z.string().optional(),
    description: z.string(),
    date: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    locale: z.enum(['en', 'pt', 'es']),
    slug: z.string(),
    translationKey: z.string(),
    image: image().optional(),
    imageCredits: z.string().optional(),
    author: z.string().default('TechFlow Team'),
    authorRole: z.string().optional(),
    authorAvatar: z.string().optional(),
    tags: z.array(z.string()).default([]),
    isBreaking: z.boolean().default(false),
    isFeatured: z.boolean().default(false),
    sources: z.array(z.object({ name: z.string(), url: z.string().optional() })).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
