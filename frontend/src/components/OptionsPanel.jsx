import { useApp } from '../context/AppContext'
import { useAnalyze } from '../hooks/useAnalyze'
import Loader from './Loader'
import styles from './OptionsPanel.module.css'

const DOC_TYPES = [
  { value: 'auto',       label: 'Auto-detect' },
  { value: 'contract',   label: 'Contract / Agreement' },
  { value: 'nda',        label: 'NDA' },
  { value: 'lease',      label: 'Lease Agreement' },
  { value: 'tos',        label: 'Terms of Service' },
  { value: 'privacy',    label: 'Privacy Policy' },
  { value: 'employment', label: 'Employment Agreement' },
  { value: 'settlement', label: 'Settlement Agreement' },
  { value: 'ip',         label: 'IP / Patent' },
]

const DEPTHS = [
  { value: 'brief',    label: 'Brief — Key points only' },
  { value: 'standard', label: 'Standard — Recommended' },
  { value: 'detailed', label: 'Detailed — Full analysis' },
]

const SECTION_CHECKBOXES = [
  { key: 'include_summary',     label: 'Executive Summary' },
  { key: 'include_parties',     label: 'Parties Involved' },
  { key: 'include_key_points',  label: 'Key Clauses & Points' },
  { key: 'include_obligations', label: 'Obligations & Duties' },
  { key: 'include_risks',       label: 'Risk Flags' },
  { key: 'include_dates',       label: 'Important Dates & Deadlines' },
]

export default function OptionsPanel({ text, file, options, setOptions }) {
  const { loading } = useApp()
  const { runAnalysis, progress, loaderMsg } = useAnalyze()

  function handleChange(key, value) {
    setOptions(prev => ({ ...prev, [key]: value }))
  }

  function handleAnalyze() {
    if (!text.trim() && !file) return
    runAnalysis({ text, file, options })
  }

  const canAnalyze = (text.trim().length >= 50 || !!file) && !loading

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <h2>Analysis Options</h2>
        <span className={styles.step}>Step 02</span>
      </div>
      <div className={styles.body}>
        {/* Two-col selects */}
        <div className={styles.grid}>
          <div className={styles.group}>
            <label htmlFor="doc-type">Document Type</label>
            <select
              id="doc-type"
              value={options.doc_type}
              onChange={e => handleChange('doc_type', e.target.value)}
            >
              {DOC_TYPES.map(d => (
                <option key={d.value} value={d.value}>{d.label}</option>
              ))}
            </select>
          </div>
          <div className={styles.group}>
            <label htmlFor="depth">Summary Depth</label>
            <select
              id="depth"
              value={options.depth}
              onChange={e => handleChange('depth', e.target.value)}
            >
              {DEPTHS.map(d => (
                <option key={d.value} value={d.value}>{d.label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Sections checkboxes */}
        <div className={styles.group}>
          <label>Include Sections</label>
          <div className={styles.checks}>
            {SECTION_CHECKBOXES.map(({ key, label }) => (
              <label key={key} className={styles.checkLabel}>
                <input
                  type="checkbox"
                  checked={options[key]}
                  onChange={e => handleChange(key, e.target.checked)}
                />
                {label}
              </label>
            ))}
          </div>
        </div>

        {/* Analyze button */}
        <button
          className={styles.analyzeBtn}
          onClick={handleAnalyze}
          disabled={!canAnalyze}
        >
          <span>⚖</span>
          {loading ? 'Analyzing…' : 'Analyze Document'}
        </button>

        {/* Loader */}
        {loading && <Loader message={loaderMsg} progress={progress} />}
      </div>
    </div>
  )
}
