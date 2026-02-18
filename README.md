# 📊 Live Data Dashboard

A real-time sensor data monitoring dashboard with FastAPI WebSocket backend and React frontend.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Node](https://img.shields.io/badge/node-24+-green.svg)

## ✨ Features

- 🔄 Real-time WebSocket data streaming
- 💾 SQLite database persistence
- 📈 Live interactive charts
- 🐳 Docker & Docker Compose support

## 🛠️ Tech Stack

**Backend:** FastAPI, WebSocket, SQLModel, SQLite  
**Frontend:** React, TypeScript, Vite, Recharts

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

### Local Development

**Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.template .env  # Edit as needed
fastapi dev
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🔌 API Endpoints

- `GET /health` - Health check
- `GET /history?limit=200` - Get historical sensor data
- `WS /ws` - WebSocket for real-time updates

## ⚙️ Configuration

Backend configuration via `.env` file:

```env
DATABASE_URL=sqlite+aiosqlite:///data.db
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
BROADCAST_INTERVAL_SECONDS=1.0
DEFAULT_SNAPSHOT_SIZE=120
```

See `.env.template` for all options.

## 📁 Project Structure

```
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py          # Routes & WebSocket
│   │   ├── service.py       # Business logic
│   │   ├── models.py        # Database models
│   │   └── ...
│   └── Dockerfile
├── frontend/         # React application
│   ├── src/
│   │   ├── components/
│   │   └── lib/
│   └── Dockerfile
└── docker-compose.yml
```

##  License

MIT

## 👨‍💻 Author

[@mouakos](https://github.com/mouakos)

---

⭐ Star this repo if you find it helpful!