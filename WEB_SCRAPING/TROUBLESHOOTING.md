# 🔧 Troubleshooting Guide

## Quick Diagnostics

### Check Everything is Running
```powershell
docker-compose ps
```

Expected:
```
NAME              COMMAND              SERVICE         STATUS
chromadb          "python -m uvicorn"  chromadb        Up (healthy)
web-scraping-app  "uvicorn app.main"   web-scraping    Up
```

### Check Logs
```powershell
# All logs
docker-compose logs

# Real-time logs
docker-compose logs -f

# Specific service
docker-compose logs -f chromadb
docker-compose logs -f web-scraping
```

### Verify Connectivity
```powershell
# Test FastAPI
curl http://localhost:8000

# Test ChromaDB
curl http://localhost:8001/api/v1

# Test Swagger UI
curl http://localhost:8000/docs
```

---

## Common Issues & Solutions

### 1. ❌ "Port 8000 is already in use"

**Error Message:**
```
Error: bind: address already in use
Error response from daemon: driver failed programming external connectivity
```

**Causes:**
- Another Docker container using port 8000
- Local service listening on port 8000
- Previous Docker container not properly cleaned

**Solutions:**

Option A: Kill the process using the port
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F
```

Option B: Change ports in docker-compose.yml
```yaml
services:
  web-scraping:
    ports:
      - "8080:8000"  # Change 8000 to 8080
  chromadb:
    ports:
      - "8002:8000"  # Change 8001 to 8002
```

Then restart:
```powershell
docker-compose restart
```

Option C: Clean up and restart
```powershell
docker-compose down
docker container prune
docker-compose up -d
```

---

### 2. ❌ "ChromaDB connection refused"

**Error Message:**
```
ConnectionRefusedError: [Errno 111] Connection refused
http.client.RemoteDisconnected: Remote end closed connection without response
```

**Causes:**
- ChromaDB didn't start
- Health check failed
- Port mapping incorrect

**Diagnosis:**
```powershell
# Check if chromadb container is running
docker-compose ps chromadb

# Check ChromaDB logs
docker-compose logs chromadb

# Test ChromaDB connectivity
curl http://localhost:8001/api/v1
```

**Solutions:**

If ChromaDB is not running:
```powershell
# Restart ChromaDB
docker-compose restart chromadb

# Or rebuild from scratch
docker-compose down
docker volume rm chroma-data
docker-compose up -d
```

If health check is failing:
```powershell
# Check health check logs
docker-compose logs chromadb | tail -20

# Increase health check timeout in docker-compose.yml:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1"]
  interval: 10s
  timeout: 10s  # Increase from 5s to 10s
  retries: 10   # Increase from 5 to 10
```

---

### 3. ❌ "Web scraping app fails to start"

**Error Message:**
```
fastapi.exceptions.FastAPISetupError
ImportError: No module named 'chromadb'
ModuleNotFoundError: No module named 'app.services'
```

**Causes:**
- requirements.txt not installed
- Python path issue
- Docker build failed

**Diagnosis:**
```powershell
# Check app logs
docker-compose logs web-scraping

# Check if requirements installed
docker exec web-scraping-app pip list | findstr chromadb
```

**Solutions:**

Rebuild the Docker image:
```powershell
docker-compose build --no-cache web-scraping
docker-compose up -d
```

If still failing, check Dockerfile:
```powershell
# Make sure your Dockerfile has:
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# And verify requirements.txt exists in root directory
dir requirements.txt
```

---

### 4. ❌ "Cannot connect to Docker daemon"

**Error Message:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. 
Is the docker daemon running?

error during connect: this error may indicate the daemon is not running
```

**Causes:**
- Docker Desktop not running
- Docker daemon stopped
- Docker not installed

**Solutions:**

Windows:
```powershell
# Start Docker Desktop from Start Menu
# Or start the service
Start-Service Docker

# Check status
docker --version
docker ps
```

Verify Docker is running:
```powershell
docker ps
# Should show running containers (or empty list)
```

If not installed:
- Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Install and restart your machine

---

### 5. ❌ "ChromaDB volume permission denied"

**Error Message:**
```
Error response from daemon: mkdir /var/lib/docker/volumes/chroma-data: permission denied
```

**Note:** This is a Linux-specific issue. Windows usually doesn't have this problem.

**Solution (Linux only):**
```bash
# Check volume permissions
sudo ls -la /var/lib/docker/volumes/

# Fix permissions
sudo chown -R 1000:1000 /var/lib/docker/volumes/chroma-data/

# Or make it world-readable
sudo chmod 777 /var/lib/docker/volumes/chroma-data/
```

---

### 6. ❌ "Out of disk space"

**Error Message:**
```
Error response from daemon: write /var/lib/docker/containers/.../log-file.log: 
no space left on device
```

**Solutions:**

Check disk space:
```powershell
# Windows
dir C:\

# View Docker disk usage
docker system df
```

Clean up Docker:
```powershell
# Remove dangling images
docker image prune -f

# Remove stopped containers
docker container prune -f

# Remove unused volumes
docker volume prune -f

# Full cleanup (be careful!)
docker system prune -a
```

---

### 7. ❌ "Timeout waiting for ChromaDB"

**Error Message:**
```
TimeoutError: [Errno 110] Connection timed out
```

**Causes:**
- System too slow
- Insufficient resources
- ChromaDB taking too long to start

**Solutions:**

Increase timeout in docker-compose.yml:
```yaml
chromadb:
  healthcheck:
    timeout: 10s  # Increase from 5s
    retries: 10   # Increase from 5
```

Check system resources:
```powershell
# View Docker resource limits
docker stats

# On Windows, check Docker Desktop settings:
# Settings > Resources > Adjust CPU/Memory allocation
```

Wait longer before testing:
```powershell
# Start containers
docker-compose up -d

# Wait 30 seconds
Start-Sleep -Seconds 30

# Then test
curl http://localhost:8001/api/v1
```

---

### 8. ❌ "Scraper getting 400 Bad Request"

**Error Message:**
```
"detail": "Failed to fetch URL. Status: 400"
```

**This is not a Docker issue!** This means the website is rejecting your request.

**Solutions:** 
(Already fixed in your scrapping_service.py!)

The User-Agent headers are already added:
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Accept": "text/html,application/xhtml+xml,...",
    # ... more headers
}
response = requests.get(str(userUrl), timeout=10, headers=headers)
```

If still failing:
- Check if website is up: `curl https://example.com`
- Try in browser: `https://example.com`
- Some websites may have rate limiting
- Some websites may require JavaScript rendering (use Selenium)

---

### 9. ❌ "docker-compose command not found"

**Error Message:**
```
docker-compose: The term 'docker-compose' is not recognized
```

**Causes:**
- Docker Compose not installed
- Using old version (docker-compose instead of docker compose)

**Solutions:**

Check if installed:
```powershell
docker compose version

# Or old syntax
docker-compose version
```

If not found, install Docker Compose:
```powershell
# Windows: Already included with Docker Desktop 4.0+
# Just update Docker Desktop to latest version

# Or manually:
# Download from https://github.com/docker/compose/releases
```

---

### 10. ❌ "Health check keeps failing"

**Error Message:**
```
chromadb is unhealthy: health_status: starting -> health_status: unhealthy
```

**Causes:**
- ChromaDB port is blocked
- ChromaDB not responding on localhost:8000
- Health check endpoint incorrect

**Diagnosis:**
```powershell
# Check what the health check is doing
docker-compose logs chromadb | grep -i "health"

# Manually test the endpoint
docker exec chromadb curl -f http://localhost:8000/api/v1

# Check if port is listening
docker exec chromadb netstat -tuln | grep 8000
```

**Solutions:**

If endpoint not responding:
```powershell
# Restart chromadb
docker-compose down chromadb
docker-compose up -d chromadb

# Wait 30 seconds
Start-Sleep -Seconds 30

# Check again
docker-compose ps chromadb
```

If still failing, check ChromaDB image:
```powershell
# Pull latest image
docker pull chromadb/chroma:latest

# Rebuild
docker-compose build --no-cache chromadb
docker-compose up -d chromadb
```

---

## Advanced Debugging

### View Docker Daemon Logs
```powershell
# Windows Event Viewer (Docker logs)
Get-EventLog -LogName Application | Where-Object {$_.Source -like "*docker*"} | Tail -20
```

### Inspect Container Details
```powershell
# Get full container info
docker inspect web-scraping-app

# Get specific info
docker inspect web-scraping-app | findstr "State.*Running"
docker inspect web-scraping-app | findstr "Volumes"
docker inspect web-scraping-app | findstr "NetworkSettings"
```

### Manual Container Testing
```powershell
# Execute command inside running container
docker exec web-scraping-app python -c "import requests; print(requests.__version__)"

# Interactive shell
docker exec -it web-scraping-app /bin/sh
# Then you can run commands inside: pip list, python, etc.
```

### View Resource Usage
```powershell
# Detailed stats
docker stats --no-stream

# Continuous monitoring
docker stats

# For specific container
docker stats web-scraping-app --no-stream
```

---

## Prevention Tips

✅ **Always use `docker-compose down` (not `-v`) when stopping**
- This preserves your ChromaDB data

✅ **Monitor logs regularly**
```powershell
docker-compose logs -f
```

✅ **Keep Docker updated**
```powershell
# Windows: Use Docker Desktop Updates menu
# Or download latest from docker.com
```

✅ **Check disk space**
```powershell
docker system df
```

✅ **Backup ChromaDB data**
```powershell
# Your data is in the chroma-data volume
# Automatically persisted - no manual backup needed!
```

✅ **Test health checks**
```powershell
docker-compose ps
# Look for "Up (healthy)" or "Up"
```

---

## Getting Help

If you're still stuck:

1. **Check logs first**
   ```powershell
   docker-compose logs -f
   ```

2. **Check official docs**
   - FastAPI: https://fastapi.tiangolo.com/
   - ChromaDB: https://docs.trychroma.com/
   - Docker: https://docs.docker.com/

3. **Rebuild from scratch** (nuclear option)
   ```powershell
   docker-compose down -v
   docker image prune -a
   docker-compose build --no-cache
   docker-compose up -d
   ```

4. **Check logs again**
   ```powershell
   docker-compose logs --tail=50
   ```

---

**Most issues resolve with one of these:**
1. `docker-compose restart`
2. `docker-compose down && docker-compose up -d`
3. `docker-compose build --no-cache && docker-compose up -d`

Good luck! 🚀

