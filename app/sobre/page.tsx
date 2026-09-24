import type { Metadata } from "next";
import { siteConfig } from "@/lib/config";

export const metadata: Metadata = {
  title: "Sobre",
  description: `Sobre o ${siteConfig.name}.`,
  alternates: { canonical: "/sobre" },
};

export default function SobrePage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="text-3xl font-extrabold sm:text-4xl">
        Sobre o {siteConfig.name}
      </h1>

      <div className="prose prose-slate mt-6 max-w-none dark:prose-invert">
        <p>
          O <strong>{siteConfig.name}</strong> é um blog dedicado a mostrar como
          usar <strong>Inteligência Artificial</strong> de forma prática para
          gerar renda no digital — do primeiro passo às estratégias avançadas de
          monetização.
        </p>
        <p>Aqui você encontra conteúdo sobre:</p>
        <ul>
          {siteConfig.categories.map((cat) => (
            <li key={cat}>{cat}</li>
          ))}
        </ul>
        <p>
          Cada artigo é escrito em Markdown, versionado no Git e publicado
          automaticamente — sem WordPress, sem plugins pesados, apenas conteúdo
          rápido e otimizado para SEO.
        </p>
      </div>
    </div>
  );
}
