import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllSlugs, getPostBySlug, formatDate } from "@/lib/posts";
import { siteConfig } from "@/lib/config";

type Params = { slug: string };

export function generateStaticParams(): Params[] {
  return getAllSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) return { title: "Artigo não encontrado" };

  return {
    title: post.title,
    description: post.description,
    alternates: { canonical: `/artigos/${slug}` },
    openGraph: {
      title: post.title,
      description: post.description,
      type: "article",
      url: `${siteConfig.url}/artigos/${slug}`,
      publishedTime: post.date,
      authors: [post.author],
    },
  };
}

export default async function ArtigoPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) notFound();

  const articleLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    description: post.description,
    inLanguage: "pt-BR",
    datePublished: post.date,
    dateModified: post.date,
    articleSection: post.category,
    author: { "@type": "Person", name: post.author },
    publisher: {
      "@type": "Organization",
      name: siteConfig.name,
      logo: { "@type": "ImageObject", url: `${siteConfig.url}/icon.svg` },
    },
    mainEntityOfPage: `${siteConfig.url}/artigos/${slug}`,
  };

  const breadcrumbLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Início", item: siteConfig.url },
      { "@type": "ListItem", position: 2, name: "Artigos", item: `${siteConfig.url}/artigos` },
      { "@type": "ListItem", position: 3, name: post.title, item: `${siteConfig.url}/artigos/${slug}` },
    ],
  };

  return (
    <article className="mx-auto max-w-3xl px-4 py-12">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbLd) }}
      />
      <Link
        href="/artigos"
        className="mb-8 inline-flex items-center gap-1 text-sm text-muted hover:text-brand-600"
      >
        <span aria-hidden>←</span> Voltar aos artigos
      </Link>

      <header className="mb-8">
        <div className="mb-3 flex items-center gap-3 text-xs text-muted">
          <span className="rounded-full bg-brand-50 px-3 py-1 font-medium text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">
            {post.category}
          </span>
          <time dateTime={post.date}>{formatDate(post.date)}</time>
          <span>· {post.readingTime} min de leitura</span>
        </div>
        <h1 className="text-3xl font-extrabold leading-tight sm:text-4xl">
          {post.title}
        </h1>
        {post.description && (
          <p className="mt-4 text-lg text-muted">{post.description}</p>
        )}
        <p className="mt-4 text-sm text-muted">Por {post.author}</p>
      </header>

      {post.cover && (
        <img
          src={post.cover}
          alt={`Ilustração do artigo: ${post.title}`}
          width={800}
          height={450}
          className="mb-10 aspect-video w-full rounded-2xl border border-app object-cover"
        />
      )}

      <div
        className="prose prose-slate max-w-none dark:prose-invert prose-headings:font-bold prose-a:text-brand-600 prose-pre:rounded-xl prose-pre:border prose-pre:border-app"
        dangerouslySetInnerHTML={{ __html: post.html }}
      />
    </article>
  );
}
