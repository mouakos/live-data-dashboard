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

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)** - Real-time bidirectional communication
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation and settings management
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - SQL databases with Python type annotations
- **[SQLite](https://www.sqlite.org/)** - Lightweight embedded database

### Frontend
- **[React 19](https://react.dev/)** - UI component library
- **[Recharts](https://recharts.org/)** - Composable charting library for React
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe JavaScript
- **[Vite](https://vitejs.dev/)** - Fast build tool and dev server

### DevOps
- **[Docker](https://www.docker.com/)** - Containerization platform
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container orchestration
- **[Nginx](https://nginx.org/)** - Web server for production frontend

## 📋 Prerequisites

- **Python 3.13+**
- **Node.js 24+** and npm
- **Docker & Docker Compose** (for containerized deployment)
- **Git**

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mouakos/live-data-dashboard.git
cd live-data-dashboard
```

### 2️⃣ Using Docker (Recommended)

**Configure environment:**
```bash
cp backend/.env.template backend/.env  # Edit as needed
```

**Start services:**
```bash
docker-compose up -d
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Manage services:**
```bash
docker-compose logs -f      # View logs
docker-compose down         # Stop services
docker-compose up --build   # Rebuild and start
```

### 3️⃣ Local Development Setup

**Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate              # Windows
# source .venv/bin/activate         # macOS/Linux
pip install -r requirements.txt
cp .env.template .env               # Configure settings
fastapi dev                         # Runs on http://localhost:8000
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm run dev                         # Runs on http://localhost:5173
```

## 🔌 API Endpoints
  
- `GET /` - API welcome message & health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `WS /ws` - WebSocket for real-time updates


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

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Stephane Mouako**
- GitHub: [@mouakos](https://github.com/mouakos)

---

⭐ Star this repo if you find it helpful!