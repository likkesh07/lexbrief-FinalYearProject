import { useState, useRef } from 'react'
import { Upload, FileText, Clock, X } from 'lucide-react'
import styles from './InputPanel.module.css'
import HistoryPanel from './HistoryPanel'

export default function InputPanel({ text, setText, file, setFile }) {
  const [activeTab, setActiveTab] = useState('paste')
  const fileInputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  const charCount = text.length
  const isOverLimit = charCount > 50000

  function handleFileChange(e) {
    const f = e.target.files?.[0]
    if (!f) return
    setFile(f)
    // For TXT preview
    if (f.name.endsWith('.txt')) {
      const reader = new FileReader()
      reader.onload = ev => setText(ev.target.result)
      reader.readAsText(f)
    }
    setActiveTab('paste')
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files?.[0]
    if (f) {
      setFile(f)
      if (f.name.endsWith('.txt')) {
        const reader = new FileReader()
        reader.onload = ev => setText(ev.target.result)
        reader.readAsText(f)
      }
      setActiveTab('paste')
    }
  }

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <h2>Document Input</h2>
        <span className={styles.step}>Step 01</span>
      </div>
      <div className={styles.body}>
        {/* Tabs */}
        <div className={styles.tabs} role="tablist">
          {[
            { id: 'paste',   label: 'Paste Text',  Icon: FileText },
            { id: 'upload',  label: 'Upload File',  Icon: Upload   },
            { id: 'history', label: 'History',      Icon: Clock    },
          ].map(({ id, label, Icon }) => (
            <button
              key={id}
              role="tab"
              aria-selected={activeTab === id}
              className={`${styles.tabBtn} ${activeTab === id ? styles.active : ''}`}
              onClick={() => setActiveTab(id)}
            >
              <Icon size={13} />
              {label}
            </button>
          ))}
        </div>

        {/* Paste Tab */}
        {activeTab === 'paste' && (
          <div className={styles.tabContent}>
            {file && (
              <div className={styles.fileTag}>
                <FileText size={13} />
                <span>{file.name}</span>
                <button onClick={() => { setFile(null); setText('') }} aria-label="Remove file">
                  <X size={13} />
                </button>
              </div>
            )}
            <textarea
              className={styles.textarea}
              value={text}
              onChange={e => setText(e.target.value)}
              placeholder="Paste your legal document, contract, NDA, lease agreement, terms of service, or any legal text here…"
              aria-label="Legal document text"
            />
            <div className={`${styles.charCount} ${isOverLimit ? styles.warning : ''}`}>
              {charCount.toLocaleString()} characters
              {isOverLimit && ' — document will be truncated at 50k chars'}
            </div>
          </div>
        )}

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className={styles.tabContent}>
            <div
              className={`${styles.dropZone} ${dragging ? styles.dragging : ''}`}
              onDragOver={e => { e.preventDefault(); setDragging(true) }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              role="button"
              tabIndex={0}
              onKeyDown={e => e.key === 'Enter' && fileInputRef.current?.click()}
              aria-label="Upload file"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <Upload size={36} strokeWidth={1.2} className={styles.uploadIcon} />
              <p><strong>Click to upload or drag &amp; drop</strong></p>
              <p className={styles.uploadSub}>Supports PDF, DOCX, DOC, TXT · Max 10 MB</p>
            </div>
            {file && (
              <div className={styles.fileInfo}>
                <FileText size={14} />
                <span>{file.name}</span>
                <span className={styles.fileSize}>({(file.size / 1024).toFixed(1)} KB)</span>
                <button onClick={() => setFile(null)} className={styles.removeBtn} aria-label="Remove file">
                  <X size={14} />
                </button>
              </div>
            )}
          </div>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div className={styles.tabContent}>
            <HistoryPanel />
          </div>
        )}
      </div>
    </div>
  )
}
