# Docker Setup Guide for Web Scraping + ChromaDB

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose installed

### Running the Application Stack

1. **Start both services (Web Scraping + ChromaDB):**
   ```bash
   docker-compose up -d
   ```
   
   This will:
   - Pull the chromadb/chroma image
   - Build your Web Scraping application from the Dockerfile
   - Start both containers on the same network
   - Create a persistent volume `chroma-data` for ChromaDB
   - Wait for ChromaDB to be healthy before starting the Web Scraping app

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop all services:**
   ```bash
   docker-compose down
   ```

4. **Stop and remove volumes (clean slate):**
   ```bash
   docker-compose down -v
   ```

## Service Details

### Web Scraping Application
- **Port:** 8000
- **URL:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### ChromaDB
- **Port:** 8001 (host) / 8000 (container)
- **URL:** http://localhost:8001 (from host) or http://chromadb:8000 (from containers)
- **API URL:** http://chromadb:8000/api/v1

## Connecting to ChromaDB from Your Python Code

### From within a Docker container:
```python
import chromadb

# Connect to ChromaDB running on the same network
client = chromadb.HttpClient(host="chromadb", port=8000)
```

### From your local machine:
```python
import chromadb

# Connect to ChromaDB via localhost
client = chromadb.HttpClient(host="localhost", port=8001)
```

## Environment Variables

The `docker-compose.yml` sets:
- `CHROMA_DB_URL=http://chromadb:8000` in the web-scraping service
- `IS_PERSISTENT=TRUE` in the chromadb service (data persists across restarts)

## Port Mapping

| Service | Container Port | Host Port | Purpose |
|---------|---|---|---|
| Web Scraping (FastAPI) | 8000 | 8000 | REST API |
| ChromaDB | 8000 | 8001 | Vector Database |

Note: ChromaDB is mapped to port 8001 on the host to avoid conflicts with FastAPI (port 8000).

## Data Persistence

ChromaDB data is stored in the `chroma-data` Docker volume. This persists even if containers are stopped/removed (unless you use `docker-compose down -v`).

## Next Steps

1. Update your scraping service to store embeddings in ChromaDB
2. Add health check endpoints to verify both services are running
3. Consider adding Redis for caching scraped content (optional enhancement)

## Troubleshooting

**ChromaDB not connecting?**
```bash
# Check if containers are running
docker-compose ps

# Check ChromaDB logs
docker-compose logs chromadb

# Test ChromaDB health
curl http://localhost:8001/api/v1
```

**Port already in use?**
Modify the port mappings in `docker-compose.yml`:
```yaml
services:
  web-scraping:
    ports:
      - "8080:8000"  # Change host port from 8000 to 8080
  chromadb:
    ports:
      - "8002:8000"  # Change host port from 8001 to 8002
```

