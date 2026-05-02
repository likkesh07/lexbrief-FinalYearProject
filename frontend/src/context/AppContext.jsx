import { createContext, useContext, useState, useCallback } from 'react'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [toast, setToast]     = useState({ message: '', visible: false })
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])

  const showToast = useCallback((message, duration = 3000) => {
    setToast({ message, visible: true })
    setTimeout(() => setToast({ message: '', visible: false }), duration)
  }, [])

  return (
    <AppContext.Provider value={{
      toast, showToast,
      result, setResult,
      loading, setLoading,
      history, setHistory,
    }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}
