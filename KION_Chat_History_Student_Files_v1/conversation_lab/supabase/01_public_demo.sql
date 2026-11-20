-- 1단계: 교실에서만 잠깐 사용하는 공개 읽기 시연
-- 민감한 자료는 넣지 않습니다. 02_secure.sql을 반드시 이어서 실행합니다.
-- 실행 전에 Data API 설정의 Exposed schemas에 llm을 추가해야 합니다.
create schema if not exists llm;

create table if not exists llm.documents (
  id uuid primary key default gen_random_uuid(),
  filename text not null,
  content text not null,
  user_id uuid references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  constraint documents_owner_filename_unique unique (user_id, filename)
);

alter table llm.documents enable row level security;
revoke all on llm.documents from anon, authenticated;
grant usage on schema llm to anon;
grant select on llm.documents to anon;

drop policy if exists "demo read" on llm.documents;
create policy "demo read" on llm.documents
for select to anon using (true);

-- Table Editor에서 공개 샘플 문서를 추가합니다. user_id는 비워 둡니다.
