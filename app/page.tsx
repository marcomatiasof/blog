import Link from "next/link";
import { getAllPosts } from "@/lib/posts";
import { siteConfig } from "@/lib/config";
import PostCard from "./components/PostCard";

export default function HomePage() {
  const posts = getAllPosts();
  const [featured, ...rest] = posts;

  return (
    <div className="mx-auto max-w-5xl px-4">
      {/* Hero */}
      <section className="py-16 text-center sm:py-24">
        <span className="mb-4 inline-block rounded-full border border-app px-4 py-1 text-xs font-medium text-muted">
          Inteligência Artificial · Finanças · Renda no digital
        </span>
        <h1 className="mx-auto max-w-3xl text-4xl font-extrabold leading-tight tracking-tight sm:text-5xl">
          Transforme{" "}
          <span className="text-brand-600">Inteligência Artificial</span> em
          renda de verdade
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg text-muted">
          {siteConfig.description}
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Link
            href="/artigos"
            className="rounded-xl bg-brand-600 px-6 py-3 font-medium text-white transition-colors hover:bg-brand-700"
          >
            Ver artigos
          </Link>
          <Link
            href="/sobre"
            className="rounded-xl border border-app px-6 py-3 font-medium transition-colors hover:border-brand-600 hover:text-brand-600"
          >
            Sobre o projeto
          </Link>
        </div>
      </section>

      {/* Categorias */}
      <section className="mb-14 flex flex-wrap justify-center gap-2">
        {siteConfig.categories.map((cat) => (
          <span
            key={cat}
            className="rounded-full border border-app px-4 py-1.5 text-sm text-muted"
          >
            {cat}
          </span>
        ))}
      </section>

      {/* Posts */}
      {posts.length === 0 ? (
        <p className="py-10 text-center text-muted">
          Nenhum artigo publicado ainda. Adicione arquivos <code>.md</code> em{" "}
          <code>content/posts</code>.
        </p>
      ) : (
        <section className="pb-10">
          <h2 className="mb-6 text-2xl font-bold">Últimos artigos</h2>

          {featured && (
            <div className="mb-6">
              <PostCard post={featured} />
            </div>
          )}

          <div className="grid gap-6 sm:grid-cols-2">
            {rest.map((post) => (
              <PostCard key={post.slug} post={post} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
