import Link from "next/link";
import type { PostMeta } from "@/lib/posts";
import { formatDate } from "@/lib/posts";

export default function PostCard({ post }: { post: PostMeta }) {
  return (
    <article className="group overflow-hidden rounded-2xl border border-app bg-card transition-shadow hover:shadow-lg">
      {post.cover && (
        <a href={`/artigos/${post.slug}`} aria-label={post.title}>
          <img
            src={post.cover}
            alt={`Capa do artigo: ${post.title}`}
            width={800}
            height={450}
            loading="lazy"
            className="aspect-video w-full object-cover"
          />
        </a>
      )}
      <div className="p-6">
      <div className="mb-3 flex items-center gap-3 text-xs text-muted">
        <span className="rounded-full bg-brand-50 px-3 py-1 font-medium text-brand-700 dark:bg-brand-900/40 dark:text-brand-300">
          {post.category}
        </span>
        <time dateTime={post.date}>{formatDate(post.date)}</time>
        <span>· {post.readingTime} min de leitura</span>
      </div>

      <h2 className="mb-2 text-xl font-bold leading-snug">
        <Link
          href={`/artigos/${post.slug}`}
          className="transition-colors group-hover:text-brand-600"
        >
          {post.title}
        </Link>
      </h2>

      <p className="mb-4 text-sm text-muted">{post.description}</p>

      <Link
        href={`/artigos/${post.slug}`}
        className="inline-flex items-center gap-1 text-sm font-medium text-brand-600 hover:gap-2 transition-all"
      >
        Ler artigo <span aria-hidden>→</span>
      </Link>
      </div>
    </article>
  );
}
