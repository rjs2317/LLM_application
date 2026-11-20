import { useEffect, useState } from 'react'
import './DocumentSources.css'


function DocumentSources() {
  const [documents, setDocuments] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  async function loadDocuments() {
    try {
      const response = await fetch('/api/documents')
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data = await response.json()
      setDocuments(data.documents)
    } catch (error) {
      setMessage(`목록을 읽지 못했습니다: ${error.message}`)
    }
  }

  // 화면이 처음 열릴 때 저장된 문서 목록을 가져옵니다.
  useEffect(() => {
    loadDocuments()
  }, [])

  async function uploadDocument(event) {
    event.preventDefault()
    if (!selectedFile || busy) return

    setBusy(true)
    setMessage('문서를 추가하고 있습니다...')
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      // FormData의 Content-Type은 브라우저가 자동으로 설정합니다.
      const response = await fetch('/api/documents', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || `HTTP ${response.status}`)

      setMessage(`${data.filename} 문서를 추가했습니다.`)
      setSelectedFile(null)
      event.target.reset()
      await loadDocuments()
    } catch (error) {
      setMessage(`추가 실패: ${error.message}`)
    } finally {
      setBusy(false)
    }
  }

  return (
    <aside className="sources" aria-label="문서 소스">
      <h2>문서 소스</h2>
      <p>질문에 사용할 TXT 자료입니다.</p>

      <form onSubmit={uploadDocument}>
        <label htmlFor="document-file">TXT 파일 선택</label>
        <input
          id="document-file"
          type="file"
          accept=".txt,text/plain"
          onChange={(event) => setSelectedFile(event.target.files[0] || null)}
        />
        <button type="submit" disabled={!selectedFile || busy}>
          {busy ? '추가 중...' : '문서 추가'}
        </button>
      </form>

      <p className="source-message" role="status">{message}</p>
      <button type="button" className="refresh" onClick={loadDocuments}>
        목록 새로고침
      </button>
      <ul className="source-list">
        {documents.map((document) => (
          <li key={document.id}>{document.filename}</li>
        ))}
      </ul>
    </aside>
  )
}

export default DocumentSources
