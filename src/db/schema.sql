-- Database Schema for Newsroom CMS & Editorial Workflow (Supabase / PostgreSQL)

-- 1. Enum Types
CREATE TYPE user_role AS ENUM ('journalist', 'editor', 'admin');
CREATE TYPE article_status AS ENUM ('idea', 'pitch', 'draft', 'review', 'approved', 'scheduled', 'published', 'archived');

-- 2. Users / Editorial Team
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role user_role NOT NULL DEFAULT 'journalist',
  bio TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Articles Table
CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  locale VARCHAR(10) NOT NULL DEFAULT 'pt',
  title TEXT NOT NULL,
  subtitle TEXT,
  description TEXT NOT NULL,
  content TEXT NOT NULL,
  image_url TEXT,
  image_credits TEXT,
  author_id UUID REFERENCES users(id) ON DELETE SET NULL,
  status article_status NOT NULL DEFAULT 'draft',
  is_breaking BOOLEAN DEFAULT FALSE,
  is_featured BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Article Versions / Audit Trail
CREATE TABLE article_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  version_number INT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  modified_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Public Editorial Corrections Log
CREATE TABLE corrections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  correction_text TEXT NOT NULL,
  corrected_at TIMESTAMPTZ DEFAULT NOW(),
  editor_id UUID REFERENCES users(id) ON DELETE SET NULL
);

-- 6. Newsroom Pitch & Assignment Board (Pautas)
CREATE TABLE pautas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  assigned_journalist_id UUID REFERENCES users(id) ON DELETE SET NULL,
  editor_id UUID REFERENCES users(id) ON DELETE SET NULL,
  priority VARCHAR(20) DEFAULT 'normal',
  status VARCHAR(30) DEFAULT 'nova',
  due_date TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Indexes for High-Performance Queries
CREATE INDEX idx_articles_status_locale ON articles(status, locale);
CREATE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);
