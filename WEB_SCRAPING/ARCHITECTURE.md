# 🏗️ Architecture & System Diagram

## Complete System Overview

```
╔════════════════════════════════════════════════════════════════════════════╗
║                          YOUR LOCAL MACHINE                                ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  ┌──────────────────────────────────────────────────────────────────────┐  ║
║  │                      DOCKER DESKTOP / ENGINE                         │  ║
║  │  ┌─────────────────────────────────────────────────────────────┐    │  ║
║  │  │           web-scraping-network (Bridge Network)             │    │  ║
║  │  │                                                             │    │  ║
║  │  │  ┌───────────────────────────┐  ┌─────────────────────┐   │    │  ║
║  │  │  │  web-scraping-app        │  │     chromadb        │   │    │  ║
║  │  │  │                           │  │                     │   │    │  ║
║  │  │  │  ┌─────────────────────┐ │  │ ┌─────────────────┐ │   │    │  ║
║  │  │  │  │   FastAPI Server    │ │  │ │  ChromaDB       │ │   │    │  ║
║  │  │  │  │                     │ │  │ │  Vector DB      │ │   │    │  ║
║  │  │  │  │  Port: 8000         │ │  │ │  Port: 8000     │ │   │    │  ║
║  │  │  │  │                     │ │  │ │                 │ │   │    │  ║
║  │  │  │  │ ┌─────────────────┐ │ │  │ │ ┌─────────────┐ │ │   │    │  ║
║  │  │  │  │ │ app/            │ │ │  │ │ │ /api/v1     │ │ │   │    │  ║
║  │  │  │  │ │ ├─main.py        │ │ │  │ │ │ (REST API) │ │ │   │    │  ║
║  │  │  │  │ │ ├─routers/       │ │ │  │ │ │            │ │ │   │    │  ║
║  │  │  │  │ │ │ ├─scrapping_   │ │ │  │ │ └─────────────┘ │ │   │    │  ║
║  │  │  │  │ │ │ │  router.py   │ │ │  │ │                 │ │   │    │  ║
║  │  │  │  │ │ │ └─user_router  │ │ │  │ │ ◄───Connects───► │   │    │  ║
║  │  │  │  │ │ └─services/      │ │ │  │ │  (if enabled)   │   │    │  ║
║  │  │  │  │ │   ├─scrapping_   │ │ │  │ │                 │   │    │  ║
║  │  │  │  │ │   │ service.py   │ │ │  │ │                 │   │    │  ║
║  │  │  │  │ │   └─chroma_      │ │ │  │ └─────────────────┘   │    │  ║
║  │  │  │  │ │     service.py   │ │ │  │                       │    │  ║
║  │  │  │  │ └─────────────────┘ │ │  └─────────────────────────┘    │    │  ║
║  │  │  │  │                     │ │                                  │    │  ║
║  │  │  │  └─────────────────────┘ │                                  │    │  ║
║  │  │  │                           │  Persistent Storage:             │    │  ║
║  │  │  └───────────────────────────┘  └──► chroma-data (Docker Volume) ────┼────┘  ║
║  │  │                                                             │    │
║  │  └─────────────────────────────────────────────────────────────┘    │
║  └──────────────────────────────────────────────────────────────────────┘
║
║  HOST PORT MAPPING:
║  ┌─────────────────────────────────────┐
║  │ :8000 ◄───► FastAPI Container        │
║  │ :8001 ◄───► ChromaDB Container       │
║  └─────────────────────────────────────┘
║
║  BROWSER / CLIENT:
║  ┌─────────────────────────────────────┐
║  │ http://localhost:8000                │ ◄─── FastAPI API
║  │ http://localhost:8000/docs           │ ◄─── Swagger UI
║  │ http://localhost:8001/api/v1         │ ◄─── ChromaDB API
║  └─────────────────────────────────────┘
║
╚════════════════════════════════════════════════════════════════════════════╝
```

## Data Flow Diagram

```
USER REQUEST
     │
     ▼
┌─────────────────────────────┐
│  Browser/Client             │
│  (http://localhost:8000)    │
└──────────┬──────────────────┘
           │
           │ HTTP Request
           │ /scrapper/?url=...
           ▼
┌─────────────────────────────────────────────────────┐
│ FastAPI (Web Scraping App)                          │
│ ┌───────────────────────────────────────────────┐   │
│ │ scrapping_router.py                           │   │
│ │ GET /scrapper/?url=<URL>                      │   │
│ │ (Optional) GET /scrapper/?url=<URL>&store=true│   │
│ └──────────┬──────────────────────────────────┘   │
│            │                                       │
│            ▼                                       │
│ ┌───────────────────────────────────────────────┐   │
│ │ scrapping_service.py                          │   │
│ │ • Fetch webpage (with User-Agent headers)     │   │
│ │ • Parse HTML with BeautifulSoup               │   │
│ │ • Extract text content                        │   │
│ └──────────┬──────────────────────────────────┘   │
│            │                                       │
│            ▼ (If store=true)                      │
│ ┌───────────────────────────────────────────────┐   │
│ │ chroma_service.py                             │   │
│ │ • Connect to ChromaDB                         │   │
│ │ • Store content with metadata                 │   │
│ │ • Generate embeddings (optional)              │   │
│ └──────────┬──────────────────────────────────┘   │
└───────────┼────────────────────────────────────────┘
            │
            │ HTTP to Container Network
            │ http://chromadb:8000/api/v1
            ▼
┌─────────────────────────────────────────────────────┐
│ ChromaDB Container                                  │
│ ┌───────────────────────────────────────────────┐   │
│ │ Vector Database                               │   │
│ │ • Store embeddings                            │   │
│ │ • Index for similarity search                 │   │
│ │ • Persist to /data volume                     │   │
│ └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
            │
            │ Persistent Storage
            ▼
┌──────────────────────────────┐
│ chroma-data Volume           │
│ (Docker Managed Storage)     │
└──────────────────────────────┘

RESPONSE FLOW:
           ◄─── JSON Response with scraped content
           ◄─── (Optional) ChromaDB storage confirmation
Browser ◄──────── HTTP 200 + {url, content, ...}
```

## Container Interaction Sequence

```
┌─────────────────┐           ┌─────────────────────┐           ┌───────────────┐
│    Developer    │           │   Docker Compose    │           │   Docker      │
│    Terminal     │           │                     │           │   Containers  │
└────────┬────────┘           └─────────────────────┘           └───────┬───────┘
         │                                                               │
         │  docker-compose up -d                                       │
         ├──────────────────────────────────────────────────────────►  │
         │                                                               │
         │                     ┌──────────────────────────────────────┐  │
         │                     │ 1. Start ChromaDB                    │  │
         │                     │    - Pull image                      │  │
         │                     │    - Create container                │  │
         │                     │    - Start service                   │  │
         │                     │    - Run health check                │  │
         │                     └────────────┬───────────────────────┘  │
         │                                   │                          │
         │                                   │ ChromaDB Ready          │
         │                                   │ (port 8001)             │
         │                     ┌─────────────▼───────────────────────┐  │
         │                     │ 2. Build Web Scraping App           │  │
         │                     │    - Run Dockerfile                 │  │
         │                     │    - Install requirements            │  │
         │                     │    - Copy app code                  │  │
         │                     └────────────┬───────────────────────┘  │
         │                                   │                          │
         │                     ┌─────────────▼───────────────────────┐  │
         │                     │ 3. Start FastAPI Service            │  │
         │                     │    - Wait for ChromaDB health       │  │
         │                     │    - Start uvicorn server           │  │
         │                     │    - Listen on port 8000            │  │
         │                     └─────────────┬───────────────────────┘  │
         │                                   │                          │
         │  ◄──────────────────────────────┐ │                         │
         │  docker-compose ps               │ │                        │
         │                                  │ │                        │
         │  NAME              STATUS         │ │                        │
         │  chromadb          Up (healthy)   │ │                        │
         │  web-scraping-app  Up             │ │                        │
         │ ◄─────────────────────────────────┘ │                        │
         │                                      │                        │
         │ curl http://localhost:8000/docs      │                        │
         ├──────────────────────────────────────────────────────────►  │
         │                                      │                        │
         │                                      │ Route to FastAPI      │
         │                                      │ Service (port 8000)   │
         │                                      │                        │
         │  ◄──────────────────────────────────────────────────────────┤
         │  Swagger UI (JSON response)         │                        │
         │                                      │                        │
         └──────────────────────────────────────────────────────────────┘
```

## File Structure Overview

```
WEB_SCRAPING/
│
├── 📦 Configuration Files
│   ├── docker-compose.yml           ⭐ Main configuration (Orchestrates both services)
│   ├── Dockerfile                   ⭐ Build definition for Web Scraping app
│   ├── requirements.txt             ⭐ Python dependencies (includes chromadb)
│   └── .dockerignore                Optimize Docker builds
│
├── 📚 Documentation (New!)
│   ├── SETUP_COMPLETE.md            ⭐ This setup guide
│   ├── CHROMA_INTEGRATION.md        Full integration instructions
│   ├── DOCKER_SETUP.md              Docker-specific details
│   └── ARCHITECTURE.md              (This file) System diagrams
│
├── 🚀 Quick Commands (New!)
│   └── quick-commands.ps1           ⭐ Interactive PowerShell menu
│
└── 📂 Application Code
    └── app/
        ├── main.py                  FastAPI entry point
        │
        ├── routers/
        │   ├── scrapping_router.py          Basic scraping endpoints
        │   ├── scrapping_router_enhanced.py (New!) With ChromaDB integration
        │   └── user_router.py               User management
        │
        ├── services/
        │   ├── scrapping_service.py         Web scraping logic
        │   ├── chroma_service.py            (New!) ChromaDB integration
        │   └── user_service.py              User management
        │
        └── models/
            └── __init__.py                  Data models
```

## Key Components Explained

### 1. docker-compose.yml
```yaml
✅ ChromaDB Service (Port 8001)
   - Image: chromadb/chroma:latest
   - Persistent volume: chroma-data
   - Health check: Every 10 seconds
   - Environment: IS_PERSISTENT=TRUE

✅ Web Scraping Service (Port 8000)
   - Built from: Dockerfile
   - Depends on: ChromaDB (waits for health check)
   - Network: web-scraping-network
   - Command: uvicorn with --reload

✅ Shared Network
   - Type: Bridge network
   - Allows container-to-container DNS resolution
   - Name: web-scraping-network

✅ Persistent Storage
   - Volume: chroma-data
   - Driver: local
   - Auto-created and managed by Docker
```

### 2. Services Communication
```
FastAPI Container                ChromaDB Container
      │                                │
      │ CHROMA_DB_URL=                │
      │ http://chromadb:8000          │
      │◄──────────────────────────────►
      │  (Container DNS resolves       │
      │   "chromadb" automatically)    │
```

### 3. Port Mapping
```
Host Machine               Docker Container
  :8000       ────────►    FastAPI :8000
  :8001       ────────►    ChromaDB :8000

Why 8001 for ChromaDB?
- Avoid conflict with FastAPI (:8000)
- Makes it clear which service is which
- Allows both to run independently
```

## Network Connectivity

```
┌──────────────────────────────────────────────────────┐
│  Browser on Host Machine                             │
│  localhost:8000/docs  ◄──────┐                       │
│  localhost:8001/api/v1  ◄────┐│                      │
└──────────────────────────────┼┼──────────────────────┘
                               ││
                    ┌──────────┘│
                    │           │ Host Network
       ┌────────────┼───────────┘
       │            │
       ▼            ▼
   localhost:8000  localhost:8001
    (port map)     (port map)
       │                │
       ▼                ▼
  ┌────────────────────────────────┐
  │   Docker Network Bridge         │
  │  (web-scraping-network)        │
  │                                │
  │  ┌──────────────┐  ┌─────────┐ │
  │  │  fastapi:    │  │ chromadb│ │
  │  │  8000        │  │ :8000   │ │
  │  └──────┬───────┘  └────┬────┘ │
  │         │                │      │
  │         │ chromadb:8000  │      │
  │         │ (DNS name)     │      │
  │         └────────────────┘      │
  │                                │
  └────────────────────────────────┘
```

## Data Persistence

```
┌─────────────────────────────────────┐
│  Docker Volume: chroma-data         │
│                                     │
│  Location:                          │
│  Windows: Docker Desktop VM         │
│  Linux:   /var/lib/docker/volumes  │
│  Mac:     Docker Desktop VM         │
│                                     │
│  Contents:                          │
│  ├── ChromaDB database files        │
│  ├── Embeddings                     │
│  ├── Metadata                       │
│  └── Indices                        │
│                                     │
│  Lifecycle:                         │
│  • Created: First docker-compose up │
│  • Persists: docker-compose down    │
│  • Deleted: docker-compose down -v  │
└─────────────────────────────────────┘
```

---

**Now you understand the complete architecture!** 🎉

See **SETUP_COMPLETE.md** for quick start instructions.

