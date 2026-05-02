import { useState } from 'react'
import { useApp } from '../context/AppContext'
import { analyzeText, uploadFile } from '../services/api'

const LOADER_MESSAGES = [
  'Reading document structure…',
  'Identifying parties & clauses…',
  'Extracting obligations…',
  'Flagging risk areas…',
  'Generating plain-language summary…',
  'Finalising analysis…',
]

export function useAnalyze() {
  const { setResult, setLoading, showToast } = useApp()
  const [progress, setProgress]     = useState(0)
  const [loaderMsg, setLoaderMsg]   = useState('')
  const [loaderTimer, setLoaderTimer] = useState(null)

  function startLoader() {
    let i = 0
    setLoaderMsg(LOADER_MESSAGES[0])
    const t = setInterval(() => {
      i = (i + 1) % LOADER_MESSAGES.length
      setLoaderMsg(LOADER_MESSAGES[i])
    }, 2200)
    setLoaderTimer(t)
  }

  function stopLoader() {
    if (loaderTimer) clearInterval(loaderTimer)
    setLoaderTimer(null)
  }

  async function runAnalysis({ text, file, options }) {
    setLoading(true)
    setProgress(10)
    startLoader()

    try {
      setProgress(30)
      let response

      if (file) {
        response = await uploadFile(file, options)
      } else {
        response = await analyzeText(text, options)
      }

      setProgress(90)

      if (!response.success) throw new Error(response.error || 'Analysis failed')

      setResult(response.data)
      setProgress(100)
      showToast('✓ Analysis complete')
    } catch (err) {
      const msg = err?.response?.data?.detail || err.message || 'Something went wrong'
      showToast(`Error: ${msg}`, 5000)
    } finally {
      stopLoader()
      setLoading(false)
      setTimeout(() => setProgress(0), 700)
    }
  }

  return { runAnalysis, progress, loaderMsg }
}
