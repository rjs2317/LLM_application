import { useEffect, useState } from 'react'
import { supabase } from './supabaseClient'
import DocumentSources from './DocumentSources'

function App() {
  const [session, setSession] = useState(null)
  const [authReady, setAuthReady] = useState(false)
  const [approved, setApproved] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [notice, setNotice] = useState('')
  const [sessions, setSessions] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [turns, setTurns] = useState([])
  const [question, setQuestion] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    // 로그인 세션은 Supabase가 보관합니다. 채팅 내용은 DB에서 다시 읽습니다.
    supabase.auth.getSession().then(({ data, error }) => {
      if (error) setNotice(error.message)
      setSession(data.session)
      setAuthReady(true)
    })
    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession)
    })
    return () => data.subscription.unsubscribe()
  }, [])

  useEffect(() => {
    if (session) checkApproval(session)
    if (!session) {
      setApproved(false)
      setSessions([])
      setActiveId(null)
      setTurns([])
    }
  }, [session?.user.id])

  async function apiRequest(path, options = {}, currentSession = session) {
    const headers = { Authorization: 'Bearer ' + currentSession.access_token }
    if (options.body) headers['Content-Type'] = 'application/json'
    const response = await fetch(path, { ...options, headers })
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || `HTTP ${response.status}`)
    return data
  }

  async function checkApproval(currentSession) {
    const { data, error } = await supabase.from('approved_users')
      .select('user_id').eq('user_id', currentSession.user.id).maybeSingle()
    if (error) { setNotice(error.message); return }
    setApproved(Boolean(data))
    if (data) await loadSessions(currentSession)
  }

  async function loadSessions(currentSession) {
    try {
      const data = await apiRequest('/api/chat-sessions', {}, currentSession)
      setSessions(data.sessions)
      // 탭 안에는 채팅 ID만 저장합니다. 대화 본문은 DB에 있습니다.
      const previousId = sessionStorage.getItem('activeChatId')
      let selected = data.sessions.find((item) => item.id === previousId)
      if (!selected) selected = data.sessions[0]
      if (selected) await openChat(selected.id, currentSession)
    } catch (error) {
      setNotice('채팅 목록을 읽지 못했습니다: ' + error.message)
    }
  }

  async function openChat(id, currentSession = session) {
    try {
      const data = await apiRequest(`/api/chat-sessions/${id}/turns`, {}, currentSession)
      setActiveId(id)
      setTurns(data.turns)
      sessionStorage.setItem('activeChatId', id)
    } catch (error) {
      setNotice('대화를 읽지 못했습니다: ' + error.message)
    }
  }

  function newChat() {
    setActiveId(null)
    setTurns([])
    setQuestion('')
    sessionStorage.removeItem('activeChatId')
  }

  async function signUp() {
    const { error } = await supabase.auth.signUp({ email, password })
    setNotice(error ? error.message : '가입했습니다. 관리자 승인을 기다리세요.')
  }

  async function signIn() {
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) setNotice(error.message)
  }

  async function signOut() {
    await supabase.auth.signOut()
    sessionStorage.removeItem('activeChatId')
    setNotice('로그아웃했습니다.')
  }

  async function send(event) {
    event.preventDefault()
    const trimmed = question.trim()
    if (!trimmed || !session || !approved || busy) return

    setBusy(true)
    setNotice('')
    try {
      let chatId = activeId
      if (!chatId) {
        // 첫 질문을 보낼 때 새 채팅방을 만듭니다.
        const data = await apiRequest('/api/chat-sessions', {
          method: 'POST',
          body: JSON.stringify({ title: trimmed.slice(0, 60) }),
        })
        chatId = data.session.id
        setActiveId(chatId)
        sessionStorage.setItem('activeChatId', chatId)
        setSessions((current) => [data.session, ...current])
      }

      const data = await apiRequest('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ session_id: chatId, question: trimmed }),
      })
      // 서버가 질문·답변 한 쌍을 DB에 저장한 뒤 돌려준 행을 표시합니다.
      setTurns((current) => [...current, data.turn])
      setQuestion('')
    } catch (error) {
      setNotice('질문 실패: ' + error.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="app">
      <header className="header">
        <span className="eyebrow">KION LABS · LLM 애플리케이션 개발</span>
        <h1>나의 문서 질문 챗봇</h1>
        <p>로그인한 사용자의 문서와 대화를 저장합니다.</p>
        {session && <button type="button" onClick={signOut}>로그아웃</button>}
        <p role="status">{notice}</p>
      </header>

      {!authReady && <section className="welcome">로그인 상태 확인 중...</section>}
      {authReady && !session && (
        <section className="welcome auth-panel">
          <h2>회원가입 또는 로그인</h2>
          <label htmlFor="email">이메일</label>
          <input id="email" type="email" value={email}
            onChange={(event) => setEmail(event.target.value)} />
          <label htmlFor="password">비밀번호</label>
          <input id="password" type="password" value={password}
            onChange={(event) => setPassword(event.target.value)} />
          <div className="auth-actions">
            <button type="button" onClick={signUp}>회원가입</button>
            <button type="button" onClick={signIn}>로그인</button>
          </div>
        </section>
      )}
      {session && !approved && (
        <section className="welcome">
          <h2>승인 대기 중</h2>
          <button type="button" onClick={() => checkApproval(session)}>승인 상태 새로고침</button>
        </section>
      )}
      {session && approved && (
        <>
          <aside className="left-panel">
            <section className="sessions-panel" aria-label="내 채팅">
              <h2>내 채팅</h2>
              <button type="button" onClick={newChat}>+ 새 채팅</button>
              <ul>
                {sessions.map((item) => (
                  <li key={item.id}>
                    <button type="button" onClick={() => openChat(item.id)}
                      className={item.id === activeId ? 'selected' : ''}>
                      {item.title}
                    </button>
                  </li>
                ))}
              </ul>
            </section>
            <DocumentSources session={session} />
          </aside>
          <section className="chat" aria-label="대화 내용">
            {turns.length === 0 && <p>새 질문을 입력해 대화를 시작하세요.</p>}
            {turns.map((turn) => (
              <div key={turn.id} className="turn">
                <div className="message user"><span className="role">나</span><p>{turn.question}</p></div>
                <div className="message assistant">
                  <span className="role">챗봇</span><p>{turn.answer}</p>
                  {turn.sources?.length > 0 && <small>참고자료: {turn.sources.join(', ')}</small>}
                </div>
              </div>
            ))}
            {busy && <p className="status">답변을 작성하고 있습니다...</p>}
          </section>
          <form className="composer" onSubmit={send}>
            <label htmlFor="question">질문</label>
            <div className="input-row">
              <input id="question" value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="예: Git commit은 무엇인가요?" maxLength={500} />
              <button type="submit" disabled={busy || !question.trim()}>보내기</button>
            </div>
          </form>
        </>
      )}
    </main>
  )
}

export default App
