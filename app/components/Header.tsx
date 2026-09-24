import Link from "next/link";
import { siteConfig } from "@/lib/config";
import Logo from "./Logo";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-app bg-card/80 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
        <Link href="/" aria-label={`${siteConfig.name} — página inicial`}>
          <Logo className="h-8 w-auto" />
        </Link>

        <nav className="flex items-center gap-2 text-sm sm:gap-4">
          {siteConfig.nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex min-h-[44px] items-center rounded-lg px-3 text-muted transition-colors hover:text-brand-600"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
