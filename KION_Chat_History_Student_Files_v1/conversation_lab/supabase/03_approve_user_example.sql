-- Authentication > Users에서 복사한 정확한 UUID로 바꾼 뒤 프로젝트 소유자가 실행
insert into llm.approved_users (user_id)
values ('00000000-0000-0000-0000-000000000000');

-- 승인을 취소하려면:
-- delete from llm.approved_users
-- where user_id = '00000000-0000-0000-0000-000000000000';
