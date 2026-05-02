import { useState } from 'react'
import Header from '../components/Header'
import Hero from '../components/Hero'
import InputPanel from '../components/InputPanel'
import OptionsPanel from '../components/OptionsPanel'
import ResultPanel from '../components/ResultPanel'
import styles from './Home.module.css'

const DEFAULT_OPTIONS = {
  doc_type:             'auto',
  depth:                'standard',
  include_summary:      true,
  include_parties:      true,
  include_key_points:   true,
  include_obligations:  true,
  include_risks:        true,
  include_dates:        true,
}

export default function Home() {
  const [text, setText]       = useState('')
  const [file, setFile]       = useState(null)
  const [options, setOptions] = useState(DEFAULT_OPTIONS)

  return (
    <div className={styles.page}>
      <Header />
      <Hero />
      <main className={styles.container}>
        <div className={styles.workspace}>
          {/* LEFT COLUMN */}
          <div className={styles.colLeft}>
            <InputPanel
              text={text}
              setText={setText}
              file={file}
              setFile={setFile}
            />
            <OptionsPanel
              text={text}
              file={file}
              options={options}
              setOptions={setOptions}
            />
          </div>

          {/* RIGHT COLUMN */}
          <div className={styles.colRight}>
            <ResultPanel />
          </div>
        </div>
      </main>
    </div>
  )
}
