import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// ── Analyze text ────────────────────────────────────────────────────
export async function analyzeText(text, options) {
  const { data } = await api.post('/analyze', { text, options })
  return data
}

// ── Upload file ─────────────────────────────────────────────────────
export async function uploadFile(file, options) {
  const form = new FormData()
  form.append('file', file)
  form.append('doc_type',           options.doc_type           ?? 'auto')
  form.append('depth',              options.depth              ?? 'standard')
  form.append('include_summary',    options.include_summary    ?? true)
  form.append('include_parties',    options.include_parties    ?? true)
  form.append('include_key_points', options.include_key_points ?? true)
  form.append('include_obligations',options.include_obligations ?? true)
  form.append('include_risks',      options.include_risks      ?? true)
  form.append('include_dates',      options.include_dates      ?? true)

  const { data } = await api.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

// ── History ─────────────────────────────────────────────────────────
export async function fetchHistory() {
  const { data } = await api.get('/history')
  return data
}

export async function deleteHistoryItem(id) {
  const { data } = await api.delete(`/history/${id}`)
  return data
}

export async function clearHistory() {
  const { data } = await api.delete('/history')
  return data
}

// ── Health ───────────────────────────────────────────────────────────
export async function healthCheck() {
  const { data } = await api.get('/health')
  return data
}
