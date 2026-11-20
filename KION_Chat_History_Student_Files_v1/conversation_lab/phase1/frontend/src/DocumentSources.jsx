import { useEffect, useState } from 'react'
import './DocumentSources.css'

function DocumentSources() {
  const [documents, setDocuments] = useState([])
  const [message, setMessage] = useState('')

  async function loadDocuments() {
    try {
      const response = await fetch('/api/documents')
      const data = await response.json()
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      setDocuments(data.documents)
    } catch (error) {
      setMessage('문서 목록을 읽지 못했습니다: ' + error.message)
    }
  }

  useEffect(() => { loadDocuments() }, [])

  return (
    <aside className="sources" aria-label="공개 샘플 문서">
      <h2>공개 샘플 문서</h2>
      <p>Supabase Table Editor에서 추가한 자료입니다.</p>
      <button type="button" onClick={loadDocuments}>목록 새로고침</button>
      <p role="status">{message}</p>
      <ul>{documents.map((document) => <li key={document.id}>{document.filename}</li>)}</ul>
    </aside>
  )
}

export default DocumentSources
