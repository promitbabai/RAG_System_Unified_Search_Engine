# 🚀 Web Scraping + ChromaDB Setup Guide

This project sets up a FastAPI-based web scraper with ChromaDB vector database integration using Docker Compose.

## 📋 What's New

✅ **Docker Compose** - Orchestrates both Web Scraping (FastAPI) and ChromaDB services  
✅ **Auto-Health Checks** - Waits for ChromaDB to be healthy before starting the app  
✅ **Persistent Storage** - ChromaDB data persists across container restarts  
✅ **Network Isolation** - Both services communicate on a private Docker network  
✅ **ChromaDB Service** - Integrated service for storing and searching content  
✅ **Enhanced Router** - Optional endpoints for ChromaDB integration  

## 🎯 Quick Start

### 1. **Start the Complete Stack**
```bash
cd D:\projects\python\RAG_System_Unified_Search_Engine\WEB_SCRAPING
docker-compose up -d
```

This single command will:
- ✅ Pull the `chromadb/chroma` image
- ✅ Build your Web Scraping application
- ✅ Start ChromaDB on port 8001
- ✅ Start FastAPI on port 8000
- ✅ Wait for ChromaDB health check
- ✅ Create a persistent `chroma-data` volume

### 2. **Verify Services are Running**
```bash
docker-compose ps
```

Expected output:
```
NAME              COMMAND                  SERVICE         STATUS
chromadb          "python -m uvicorn..."   chromadb        Up
web-scraping-app  "uvicorn app.main..."    web-scraping    Up
```

### 3. **Check Logs**
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f chromadb
docker-compose logs -f web-scraping
```

## 🌐 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **FastAPI API** | http://localhost:8000 | REST API |
| **FastAPI Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| **FastAPI ReDoc** | http://localhost:8000/redoc | Alternative API docs |
| **ChromaDB API** | http://localhost:8001/api/v1 | Vector DB API |

## 📡 API Endpoints

### Basic Scraping
```bash
# Scrape a webpage
curl "http://localhost:8000/scrapper/?url=https://example.com"

# Scrape and store in ChromaDB
curl "http://localhost:8000/scrapper/?url=https://example.com&store=true"
```

### ChromaDB Integration (Optional)
```bash
# Search stored content
curl "http://localhost:8000/scrapper/search?query=your+search+term"

# Get ChromaDB statistics
curl "http://localhost:8000/scrapper/stats"

# Clear all ChromaDB content (⚠️ destructive)
curl -X DELETE "http://localhost:8000/scrapper/clear-chroma"
```

## 🛑 Stopping the Stack

```bash
# Stop containers (data persists)
docker-compose stop

# Stop and remove containers (data persists in volume)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

## 🔧 Configuration

### Change Ports
Edit `docker-compose.yml`:
```yaml
services:
  web-scraping:
    ports:
      - "8080:8000"  # Change from 8000 to 8080
  chromadb:
    ports:
      - "8002:8000"  # Change from 8001 to 8002
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### Environment Variables
Edit `docker-compose.yml` to add more variables:
```yaml
services:
  web-scraping:
    environment:
      - CHROMA_DB_URL=http://chromadb:8000
      - MY_CUSTOM_VAR=value
```

## 📚 Project Structure

```
WEB_SCRAPING/
├── Dockerfile                          # Docker image definition
├── docker-compose.yml                  # Docker Compose orchestration
├── requirements.txt                    # Python dependencies
├── DOCKER_SETUP.md                     # Docker setup guide
├── CHROMA_INTEGRATION.md               # This file
├── app/
│   ├── main.py                         # FastAPI entry point
│   ├── routers/
│   │   ├── scrapping_router.py         # Basic scraping endpoints
│   │   ├── scrapping_router_enhanced.py # With ChromaDB integration
│   │   └── user_router.py              # User management
│   └── services/
│       ├── scrapping_service.py        # Web scraping logic
│       └── chroma_service.py           # ChromaDB integration
└── scrapingenv/                        # Python virtual environment
```

## 💾 Data Persistence

ChromaDB data is stored in the `chroma-data` Docker volume:

```bash
# View volume details
docker volume inspect chroma-data

# List all volumes
docker volume ls

# Remove specific volume
docker volume rm chroma-data
```

## 🔍 Troubleshooting

### Issue: ChromaDB Connection Refused
```bash
# Check if ChromaDB is running
docker-compose logs chromadb

# Verify health check
curl http://localhost:8001/api/v1

# Restart ChromaDB
docker-compose restart chromadb
```

### Issue: Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml
```

### Issue: Container Won't Start
```bash
# Check logs
docker-compose logs web-scraping

# Rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Permission Denied on Volume
```bash
# On Linux, fix permissions
sudo chmod 777 chroma-data

# On Windows, usually not needed
```

## 📊 Monitoring

### View Real-time Metrics
```bash
# Monitor container resources
docker stats

# Monitor specific container
docker stats web-scraping-app
```

### Check Container Health
```bash
# Detailed container info
docker-compose ps --format "table {{.Names}}\t{{.Status}}"

# Inspect a service
docker inspect web-scraping-app
```

## 🚀 Advanced Usage

### Development Mode with Hot Reload
The `docker-compose.yml` includes `--reload` flag for FastAPI, so changes to Python files will automatically reload.

To enable:
1. File changes are detected (if you've bound volumes)
2. FastAPI will auto-reload
3. No need to restart container

### Using ChromaDB from Your Code

```python
from app.services.chroma_service import chroma_service

# Store content
result = chroma_service.store_content(
    url="https://example.com",
    content="Your extracted text here",
    metadata={"category": "news"}
)

# Search content
results = chroma_service.search_content("search query")

# Get stats
stats = chroma_service.get_stats()
```

## 📝 Next Steps

1. **Customize ChromaDB** - Add custom embeddings models in `chroma_service.py`
2. **Add Authentication** - Implement JWT in FastAPI routers
3. **Database Integration** - Add PostgreSQL for metadata storage
4. **Caching** - Add Redis for scraping cache
5. **Monitoring** - Setup Prometheus + Grafana for metrics
6. **CI/CD** - Add GitHub Actions for automated testing

## 📖 Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## ⚠️ Important Notes

- **ChromaDB Port Mapping**: ChromaDB runs on port 8001 (host) to avoid conflicts with FastAPI (port 8000)
- **Data Safety**: Use `docker-compose down` (not `-v`) to keep data persistent
- **Resource Usage**: Both containers run simultaneously; ensure your system has sufficient resources
- **Network**: Containers communicate via `web-scraping-network` - internal DNS resolution works automatically

## 🎉 You're All Set!

Your Web Scraping + ChromaDB stack is ready to use. Start with:

```bash
docker-compose up -d
```

Then visit: **http://localhost:8000/docs** for interactive API documentation!

