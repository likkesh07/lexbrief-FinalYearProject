import { Routes, Route } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import Home from './pages/Home'
import Toast from './components/Toast'

export default function App() {
  return (
    <AppProvider>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
      <Toast />
    </AppProvider>
  )
}
