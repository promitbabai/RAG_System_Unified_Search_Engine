# 📋 Quick Reference Card

## 🚀 Essential Commands

### Starting & Stopping
```powershell
# Start everything
docker-compose up -d

# Stop everything (keep data)
docker-compose stop

# Stop and remove containers (keep data)
docker-compose down

# Stop and DELETE everything
docker-compose down -v

# Restart everything
docker-compose restart
```

### Monitoring
```powershell
# Check status
docker-compose ps

# View logs (real-time)
docker-compose logs -f

# Specific service logs
docker-compose logs -f chromadb
docker-compose logs -f web-scraping

# Resource usage
docker stats
```

### Testing
```powershell
# Test FastAPI
curl http://localhost:8000

# Test ChromaDB
curl http://localhost:8001/api/v1

# Test Swagger docs
curl http://localhost:8000/docs

# Test scraper
curl "http://localhost:8000/scrapper/?url=https://example.com"
```

---

## 🌐 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| FastAPI | http://localhost:8000 | REST API |
| Swagger UI | http://localhost:8000/docs | Interactive API Docs |
| ReDoc | http://localhost:8000/redoc | Alternative API Docs |
| ChromaDB | http://localhost:8001/api/v1 | Vector Database |

---

## 📡 API Endpoints

### Scraping
```bash
# Basic scrape
GET /scrapper/?url=https://example.com

# Scrape and store in ChromaDB
GET /scrapper/?url=https://example.com&store=true
```

### ChromaDB (if using enhanced router)
```bash
# Search stored content
GET /scrapper/search?query=your+search

# Get statistics
GET /scrapper/stats

# Clear all data (⚠️ destructive)
DELETE /scrapper/clear-chroma
```

---

## 🐳 Docker Compose Commands

```powershell
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Create and start
docker-compose up -d

# Stop
docker-compose stop

# Start (when already created)
docker-compose start

# Restart
docker-compose restart

# Remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs chromadb

# View real-time logs
docker-compose logs -f

# Execute command in container
docker-compose exec web-scraping python --version

# Show running containers
docker-compose ps

# Show all containers
docker-compose ps -a
```

---

## 🔧 Troubleshooting Quick Fixes

```powershell
# Connection refused?
docker-compose restart chromadb

# Port already in use?
docker-compose down
# Change ports in docker-compose.yml
docker-compose up -d

# Something broken?
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# View detailed logs
docker-compose logs --tail=100

# Check container health
docker-compose ps chromadb
# Should show "Up (healthy)"

# Clean up unused Docker resources
docker system prune -a
```

---

## 📊 File Locations

```
Your Project Directory:
D:\projects\python\RAG_System_Unified_Search_Engine\WEB_SCRAPING\

Important Files:
├── docker-compose.yml          ⭐ Configuration
├── Dockerfile                  ⭐ Build instructions
├── requirements.txt            ⭐ Python packages
│
├── SETUP_COMPLETE.md           📖 Start here!
├── ARCHITECTURE.md             📊 System diagrams
├── CHROMA_INTEGRATION.md       📚 Full guide
├── TROUBLESHOOTING.md          🔧 Problem solving
├── quick-commands.ps1          ⚡ Interactive menu
│
└── app/
    └── services/
        └── chroma_service.py   💾 ChromaDB integration
```

---

## 🎯 First-Time Setup

```powershell
# 1. Navigate to project
cd D:\projects\python\RAG_System_Unified_Search_Engine\WEB_SCRAPING

# 2. Start the stack
docker-compose up -d

# 3. Wait 10-15 seconds for services to start

# 4. Check status
docker-compose ps

# 5. Open browser
# http://localhost:8000/docs

# 6. Try the API
curl "http://localhost:8000/scrapper/?url=https://example.com"
```

---

## 📦 Port Mappings

```
Host Machine    →  Docker Container  →  Service
localhost:8000  →  FastAPI:8000      →  Web Scraping API
localhost:8001  →  ChromaDB:8000     →  Vector Database
```

---

## 🔐 Environment Variables

In `docker-compose.yml`:

```yaml
environment:
  - CHROMA_DB_URL=http://chromadb:8000
  - IS_PERSISTENT=TRUE
```

Access in Python:
```python
import os
chroma_url = os.getenv("CHROMA_DB_URL")
```

---

## 💾 Data Persistence

```powershell
# Your data is stored in: chroma-data volume
# Created automatically on first run
# Persists when you: docker-compose down
# Deleted only when: docker-compose down -v

# View volume info
docker volume ls
docker volume inspect chroma-data
```

---

## ✅ Health Checks

ChromaDB runs a health check every 10 seconds:
- Healthy: Endpoint responds to `/api/v1`
- Unhealthy: Service not responding
- Starting: Initial startup period

View health in status:
```powershell
docker-compose ps
# Look for: "Up (healthy)" or "Up"
```

---

## 🚀 Performance Tips

### Enable Hot Reload (Already On!)
```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Changes to Python files = automatic reload!

### Increase Resources
Edit Docker Desktop Settings:
- Settings > Resources
- Increase CPU cores allocated
- Increase memory allocation

### Monitor Performance
```powershell
docker stats
```

---

## 📝 Common Patterns

### Check if Services are Ready
```powershell
docker-compose ps
# Both should show "Up"
```

### View Recent Errors
```powershell
docker-compose logs --tail=20
```

### Rebuild After Code Changes
```powershell
# Usually not needed (reload enabled)
# But if needed:
docker-compose down
docker-compose up -d
```

### Reset Everything
```powershell
docker-compose down -v
docker volume rm chroma-data
docker image prune -a
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔗 Useful Links

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **ChromaDB Docs**: https://docs.trychroma.com/
- **Docker Docs**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/

---

## ⚡ Interactive PowerShell Menu

```powershell
cd D:\projects\python\RAG_System_Unified_Search_Engine\WEB_SCRAPING
.\quick-commands.ps1
```

This opens a menu with all common commands!

---

## 🎓 Next Steps

1. ✅ **Read**: `SETUP_COMPLETE.md` - Full setup guide
2. ✅ **Review**: `ARCHITECTURE.md` - Understand the system
3. ✅ **Try**: `docker-compose up -d` - Start the stack
4. ✅ **Test**: `curl http://localhost:8000/docs` - Test API
5. ✅ **Integrate**: Use ChromaDB in your code

---

**Everything is ready!** 🚀

Start with:
```powershell
docker-compose up -d
```

Then visit: **http://localhost:8000/docs**

