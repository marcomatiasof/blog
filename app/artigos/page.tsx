import type { Metadata } from "next";
import { getAllPosts } from "@/lib/posts";
import PostCard from "../components/PostCard";

export const metadata: Metadata = {
  title: "Artigos",
  description: "Todos os artigos sobre IA, finanças e monetização.",
  alternates: { canonical: "/artigos" },
};

export default function ArtigosPage() {
  const posts = getAllPosts();

  return (
    <div className="mx-auto max-w-5xl px-4 py-12">
      <header className="mb-10">
        <h1 className="text-3xl font-extrabold sm:text-4xl">Artigos</h1>
        <p className="mt-2 text-muted">
          {posts.length} {posts.length === 1 ? "artigo publicado" : "artigos publicados"}.
        </p>
      </header>

      {posts.length === 0 ? (
        <p className="text-muted">Nenhum artigo publicado ainda.</p>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2">
          {posts.map((post) => (
            <PostCard key={post.slug} post={post} />
          ))}
        </div>
      )}
    </div>
  );
}
