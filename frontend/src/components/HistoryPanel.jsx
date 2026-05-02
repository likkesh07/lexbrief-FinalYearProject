import { useEffect } from 'react'
import { FileText, Trash2, RefreshCw } from 'lucide-react'
import { useHistory } from '../hooks/useHistory'
import styles from './HistoryPanel.module.css'

export default function HistoryPanel() {
  const { history, loadHistory, removeItem, clearAll, loadItem } = useHistory()

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  if (history.length === 0) {
    return (
      <div className={styles.empty}>
        <FileText size={28} strokeWidth={1} className={styles.emptyIcon} />
        <p>No past analyses yet.</p>
        <p className={styles.emptySub}>Analyze a document to see history here.</p>
      </div>
    )
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.toolbar}>
        <button className={styles.refreshBtn} onClick={loadHistory} title="Refresh">
          <RefreshCw size={13} /> Refresh
        </button>
        <button className={styles.clearBtn} onClick={clearAll} title="Clear all">
          <Trash2 size={13} /> Clear All
        </button>
      </div>

      <ul className={styles.list}>
        {history.map(item => (
          <li key={item.id} className={styles.item}>
            <button
              className={styles.itemBody}
              onClick={() => loadItem(item)}
              title="Load this analysis"
            >
              <FileText size={16} className={styles.itemIcon} />
              <div className={styles.itemInfo}>
                <div className={styles.itemType}>{item.doc_type}</div>
                <div className={styles.itemMeta}>
                  <RiskDot level={item.risk_level} />
                  {item.risk_level} risk ·{' '}
                  {new Date(item.created_at).toLocaleString()}
                </div>
                <div className={styles.itemPreview}>{item.text_preview}</div>
              </div>
            </button>
            <button
              className={styles.deleteBtn}
              onClick={() => removeItem(item.id)}
              aria-label="Delete history item"
              title="Delete"
            >
              <Trash2 size={13} />
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

function RiskDot({ level }) {
  const color = {
    High:   '#8b1a1a',
    Medium: '#7a5c00',
    Low:    '#1a5c3a',
  }[level] || '#6b6560'
  return (
    <span
      style={{
        display: 'inline-block',
        width: 7, height: 7,
        borderRadius: '50%',
        background: color,
        marginRight: 4,
        verticalAlign: 'middle',
      }}
    />
  )
}
