# ⚖️ LexBrief — AI Legal Document Summarizer
### Final Year Project | Full-Stack Application

> Instantly analyze contracts, NDAs, leases, and any legal documents using Claude AI.  
> **Backend:** Python (FastAPI) · **Frontend:** React.js + Vite

---

## 📁 Project Structure

```
lexbrief/
├── backend/                  # Python FastAPI server
│   ├── main.py               # App entry point
│   ├── config.py             # Environment & settings
│   ├── requirements.txt      # Python dependencies
│   ├── routes/
│   │   ├── analyze.py        # /api/analyze endpoint
│   │   ├── history.py        # /api/history endpoints
│   │   └── upload.py         # /api/upload endpoint
│   ├── services/
│   │   ├── anthropic_service.py  # Claude AI integration
│   │   ├── pdf_service.py        # PDF text extraction
│   │   └── docx_service.py       # DOCX text extraction
│   ├── models/
│   │   └── schemas.py        # Pydantic request/response models
│   └── utils/
│       └── helpers.py        # Utility functions
│
├── frontend/                 # React.js application
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── components/
│       │   ├── Header.jsx
│       │   ├── Hero.jsx
│       │   ├── InputPanel.jsx
│       │   ├── OptionsPanel.jsx
│       │   ├── ResultPanel.jsx
│       │   ├── HistoryPanel.jsx
│       │   ├── Loader.jsx
│       │   └── Toast.jsx
│       ├── pages/
│       │   └── Home.jsx
│       ├── hooks/
│       │   ├── useAnalyze.js
│       │   └── useHistory.js
│       ├── services/
│       │   └── api.js        # Axios API calls to backend
│       └── context/
│           └── AppContext.jsx
│
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- An Anthropic API key → https://console.anthropic.com

---

### 1. Clone / Extract the project

```bash
cd lexbrief
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# → Edit .env and add your ANTHROPIC_API_KEY

# Start the backend server
uvicorn main:app --reload --port 8000
```

Backend runs at: **http://localhost:8000**  
API Docs (Swagger): **http://localhost:8000/docs**

---

### 3. Frontend Setup

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## 🔑 Environment Variables

Create `backend/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
ALLOWED_ORIGINS=http://localhost:5173
MAX_FILE_SIZE_MB=10
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 Paste Text | Directly paste any legal document |
| 📁 File Upload | Upload PDF, DOCX, TXT files |
| 🤖 AI Analysis | Claude AI extracts key information |
| ⚖️ Risk Detection | High / Medium / Low risk flagging |
| 👥 Parties | Identifies all involved parties |
| 📌 Key Clauses | Extracts critical clauses |
| 📅 Dates | Important deadlines & dates |
| 🚩 Obligations | Duties and obligations listed |
| 📜 History | Past analyses saved locally |
| 📥 Export | Download summary as PDF/TXT |

---

## 🛠 Tech Stack

### Backend
- **FastAPI** — Modern Python web framework
- **Anthropic SDK** — Claude AI integration
- **PyMuPDF** — PDF text extraction
- **python-docx** — Word document parsing
- **Pydantic** — Data validation
- **uvicorn** — ASGI server

### Frontend
- **React 18** — UI framework
- **Vite** — Build tool
- **Axios** — HTTP client
- **React Router** — Navigation
- **Lucide React** — Icons

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Analyze pasted text |
| POST | `/api/upload` | Upload & analyze file |
| GET | `/api/history` | Get analysis history |
| DELETE | `/api/history/{id}` | Delete history item |
| GET | `/api/health` | Health check |

---

## 👨‍💻 Development Notes

- Backend API auto-reloads on code changes (`--reload` flag)
- Frontend HMR enabled via Vite
- CORS configured for local development
- All history stored in `backend/history.json`

---

*LexBrief — Final Year Project*
