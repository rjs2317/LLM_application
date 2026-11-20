import { createClient } from '@supabase/supabase-js'

// VITE_로 시작하는 값은 브라우저에 보입니다. publishable key만 넣습니다.
const url = import.meta.env.VITE_SUPABASE_URL
const key = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

// 데이터 조회는 llm 스키마를 사용합니다. Auth API는 그대로 작동합니다.
export const supabase = createClient(url, key, { db: { schema: 'llm' } })
