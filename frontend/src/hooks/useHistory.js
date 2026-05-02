import { useCallback } from 'react'
import { useApp } from '../context/AppContext'
import { fetchHistory, deleteHistoryItem, clearHistory } from '../services/api'

export function useHistory() {
  const { history, setHistory, setResult, showToast } = useApp()

  const loadHistory = useCallback(async () => {
    try {
      const res = await fetchHistory()
      if (res.success) setHistory(res.data)
    } catch {
      // silently fail — history is non-critical
    }
  }, [setHistory])

  const removeItem = useCallback(async (id) => {
    try {
      await deleteHistoryItem(id)
      setHistory(prev => prev.filter(h => h.id !== id))
      showToast('History item deleted')
    } catch {
      showToast('Failed to delete item', 4000)
    }
  }, [setHistory, showToast])

  const clearAll = useCallback(async () => {
    try {
      await clearHistory()
      setHistory([])
      showToast('History cleared')
    } catch {
      showToast('Failed to clear history', 4000)
    }
  }, [setHistory, showToast])

  const loadItem = useCallback((item) => {
    setResult(item.result)
    showToast('✓ Loaded from history')
  }, [setResult, showToast])

  return { history, loadHistory, removeItem, clearAll, loadItem }
}
