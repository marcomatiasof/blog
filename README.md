# AIMonetiza

Blog sobre Inteligência Artificial, mercado financeiro e monetização.
Construído com **Next.js 16 + Tailwind CSS 4 + Markdown** (sem WordPress).

## Rodar localmente

```bash
npm install      # só na primeira vez
npm run dev      # http://localhost:3000
```

## Publicar um novo artigo

Crie um arquivo `.md` em `content/posts/`. Exemplo:

```markdown
---
title: "Título do artigo"
description: "Resumo que aparece nos cards e no SEO."
date: "2026-07-09"
category: "Monetização"
author: "AIMonetiza"
---

Conteúdo em **Markdown** normal. Suporta tabelas, listas,
código com destaque de sintaxe, citações etc.
```

O artigo aparece automaticamente na home e em `/artigos`,
com URL `/artigos/nome-do-arquivo`.

## Estrutura

```
app/                 Páginas e componentes (App Router)
  page.tsx           Home
  artigos/           Lista + [slug] do artigo
  sobre/             Página institucional
  components/        Header, Footer, PostCard
content/posts/       Seus artigos em Markdown  ← escreva aqui
lib/                 config do site + leitura dos posts
docs/                Plano original do projeto
```

## Configuração do site

Edite `lib/config.ts` para mudar nome, descrição, menu e categorias.

## Deploy

Recomendado: **Vercel** (grátis). Suba o projeto no GitHub e conecte.
Build: `npm run build`.
