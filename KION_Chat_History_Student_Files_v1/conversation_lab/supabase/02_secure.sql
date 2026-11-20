-- 2단계: 수동 승인된 로그인 사용자만 자기 문서를 읽고 추가합니다.
create table if not exists llm.approved_users (
  user_id uuid primary key references auth.users(id) on delete cascade,
  approved_at timestamptz not null default now()
);
alter table llm.approved_users enable row level security;
revoke all on llm.approved_users from anon, authenticated;
grant usage on schema llm to authenticated;
grant select on llm.approved_users to authenticated;
drop policy if exists "read own approval" on llm.approved_users;
create policy "read own approval" on llm.approved_users
for select to authenticated
using ((select auth.uid()) = user_id);

-- 공개 읽기 정책과 익명 권한을 제거합니다.
drop policy if exists "demo read" on llm.documents;
revoke all on llm.documents from anon, authenticated;
revoke usage on schema llm from anon;
grant select, insert on llm.documents to authenticated;

drop policy if exists "read approved own" on llm.documents;
create policy "read approved own" on llm.documents
for select to authenticated using (
  user_id = (select auth.uid()) and exists (
    select 1 from llm.approved_users a
    where a.user_id = (select auth.uid())
  )
);

drop policy if exists "insert approved own" on llm.documents;
create policy "insert approved own" on llm.documents
for insert to authenticated with check (
  user_id = (select auth.uid()) and exists (
    select 1 from llm.approved_users a
    where a.user_id = (select auth.uid())
  )
);

-- 공개 시연용 user_id가 비어 있는 행은 이제 앱에서 보이지 않습니다.
-- 승인한 본인 계정으로 TXT를 다시 업로드합니다.
