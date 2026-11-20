-- 02_secure.sql을 적용한 뒤 실행합니다.
-- 한 사용자에게 여러 채팅방을 만들고, 질문·답변을 채팅방별로 저장합니다.

create table if not exists llm.chat_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  title text not null,
  created_at timestamptz not null default now(),
  constraint chat_title_length check (char_length(title) between 1 and 80)
);

create index if not exists chat_sessions_owner_order_idx
  on llm.chat_sessions (user_id, created_at desc);

create table if not exists llm.chat_turns (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references llm.chat_sessions(id) on delete cascade,
  question text not null,
  answer text not null,
  sources jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  constraint chat_question_length check (char_length(question) between 1 and 500),
  constraint chat_answer_length check (char_length(answer) between 1 and 50000)
);

create index if not exists chat_turns_session_order_idx
  on llm.chat_turns (session_id, created_at, id);

alter table llm.chat_sessions enable row level security;
alter table llm.chat_turns enable row level security;

revoke all on llm.chat_sessions from anon, authenticated;
revoke all on llm.chat_turns from anon, authenticated;
grant usage on schema llm to authenticated;
grant select, insert on llm.chat_sessions to authenticated;
grant select, insert on llm.chat_turns to authenticated;

-- 승인된 사용자는 자기 채팅방만 읽고 만들 수 있습니다.
drop policy if exists "read own approved chats" on llm.chat_sessions;
create policy "read own approved chats" on llm.chat_sessions
for select to authenticated using (
  user_id = (select auth.uid()) and exists (
    select 1 from llm.approved_users a
    where a.user_id = (select auth.uid())
  )
);

drop policy if exists "create own approved chats" on llm.chat_sessions;
create policy "create own approved chats" on llm.chat_sessions
for insert to authenticated with check (
  user_id = (select auth.uid()) and exists (
    select 1 from llm.approved_users a
    where a.user_id = (select auth.uid())
  )
);

-- 채팅방의 소유자에게만 질문·답변을 보여 주고 저장하게 합니다.
drop policy if exists "read own chat turns" on llm.chat_turns;
create policy "read own chat turns" on llm.chat_turns
for select to authenticated using (
  exists (
    select 1 from llm.chat_sessions s
    where s.id = session_id and s.user_id = (select auth.uid())
  )
);

drop policy if exists "create own chat turns" on llm.chat_turns;
create policy "create own chat turns" on llm.chat_turns
for insert to authenticated with check (
  exists (
    select 1 from llm.chat_sessions s
    where s.id = session_id and s.user_id = (select auth.uid())
  )
);

-- 이번 수업에서는 수정·삭제 권한을 열지 않습니다.
