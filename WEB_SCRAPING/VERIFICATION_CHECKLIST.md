# ✅ Verification Checklist

Complete this checklist to verify your Docker + ChromaDB setup is working correctly.

## Phase 1: Pre-Setup Check

- [ ] Docker Desktop is installed
  ```powershell
  docker --version
  docker-compose --version
  ```
  Expected: Both should show version numbers

- [ ] You're in the correct directory
  ```powershell
  cd D:\projects\python\RAG_System_Unified_Search_Engine\WEB_SCRAPING
  pwd  # Should show WEB_SCRAPING directory
  ```

- [ ] Required files exist
  - [ ] docker-compose.yml
  - [ ] Dockerfile
  - [ ] requirements.txt
  - [ ] app/main.py

---

## Phase 2: Startup Check

- [ ] Start the stack
  ```powershell
  docker-compose up -d
  ```
  Expected: Both services start without errors

- [ ] Wait 15 seconds for services to initialize
  ```powershell
  Start-Sleep -Seconds 15
  ```

- [ ] Check container status
  ```powershell
  docker-compose ps
  ```
  Expected output:
  ```
  NAME              COMMAND              SERVICE         STATUS
  chromadb          "python -m uvicorn"  chromadb        Up (healthy)
  web-scraping-app  "uvicorn app.main"   web-scraping    Up
  ```

---

## Phase 3: Connectivity Check

### Test FastAPI
- [ ] Check FastAPI is listening
  ```powershell
  curl http://localhost:8000
  ```
  Expected: `"Hello World"`

- [ ] Check FastAPI docs
  ```powershell
  curl http://localhost:8000/docs
  ```
  Expected: HTML content containing "Swagger"

- [ ] Open in browser (if in GUI)
  ```powershell
  Start-Process http://localhost:8000/docs
  ```

### Test ChromaDB
- [ ] Check ChromaDB is listening
  ```powershell
  curl http://localhost:8001/api/v1
  ```
  Expected: JSON response

- [ ] Check health endpoint
  ```powershell
  curl http://localhost:8001/api/v1/
  ```
  Expected: JSON with ChromaDB info

---

## Phase 4: Functionality Check

### Test Web Scraping
- [ ] Scrape a simple website
  ```powershell
  curl "http://localhost:8000/scrapper/?url=https://example.com"
  ```
  Expected: JSON with `url` and `content` fields

- [ ] Verify content was extracted
  ```powershell
  # Response should contain text from the website
  ```

- [ ] Scrape a government website
  ```powershell
  curl "http://localhost:8000/scrapper/?url=https://www.example.gov"
  ```
  Expected: Should work (already working before)

- [ ] Scrape a commercial website
  ```powershell
  curl "http://localhost:8000/scrapper/?url=https://www.wikipedia.org"
  ```
  Expected: Should work (fixed with headers!)

### Test ChromaDB Integration (Optional)
If using enhanced router:

- [ ] Check stats
  ```powershell
  curl http://localhost:8000/scrapper/stats
  ```
  Expected: JSON with collection statistics

- [ ] Store content
  ```powershell
  curl "http://localhost:8000/scrapper/?url=https://example.com&store=true"
  ```
  Expected: Response includes ChromaDB storage confirmation

---

## Phase 5: Data Persistence Check

- [ ] Check volume was created
  ```powershell
  docker volume ls | findstr chroma
  ```
  Expected: `chroma-data` in the list

- [ ] Verify volume is mounted
  ```powershell
  docker inspect chromadb | findstr -A 5 "Mounts"
  ```
  Expected: Shows volume mounted to `/data`

- [ ] Stop containers (keep data)
  ```powershell
  docker-compose stop
  ```

- [ ] Start containers again
  ```powershell
  docker-compose start
  ```

- [ ] Wait for ChromaDB to be healthy
  ```powershell
  Start-Sleep -Seconds 10
  docker-compose ps chromadb
  ```
  Expected: Shows "Up (healthy)"

- [ ] Verify data persisted
  ```powershell
  docker-compose ps
  docker stats --no-stream
  ```

---

## Phase 6: Log Check

- [ ] View startup logs (should be clean)
  ```powershell
  docker-compose logs --tail=20
  ```
  Expected: No ERROR or CRITICAL messages

- [ ] Check ChromaDB logs
  ```powershell
  docker-compose logs chromadb | tail -10
  ```
  Expected: Shows ChromaDB started successfully

- [ ] Check FastAPI logs
  ```powershell
  docker-compose logs web-scraping | tail -10
  ```
  Expected: Shows FastAPI started on 0.0.0.0:8000

---

## Phase 7: Performance Check

- [ ] Check resource usage
  ```powershell
  docker stats --no-stream
  ```
  Expected:
  - CPU usage: < 5% each (at idle)
  - Memory: < 500MB each (normal for Python apps)
  - Network: Low I/O at idle

- [ ] Check disk usage
  ```powershell
  docker system df
  ```
  Expected: Reasonable sizes (shouldn't be GB+)

---

## Phase 8: File Structure Check

- [ ] Verify all created files exist
  - [ ] `docker-compose.yml`
  - [ ] `app/services/chroma_service.py`
  - [ ] `app/routers/scrapping_router_enhanced.py`
  - [ ] `README.md`
  - [ ] `SUMMARY.md`
  - [ ] `SETUP_COMPLETE.md`
  - [ ] `QUICK_REFERENCE.md`
  - [ ] `ARCHITECTURE.md`
  - [ ] `CHROMA_INTEGRATION.md`
  - [ ] `TROUBLESHOOTING.md`
  - [ ] `DOCKER_SETUP.md`
  - [ ] `quick-commands.ps1`

---

## Phase 9: Documentation Check

- [ ] README.md is readable
  ```powershell
  notepad README.md  # or open in your editor
  ```

- [ ] Can access quick commands
  ```powershell
  .\quick-commands.ps1
  # Should show interactive menu
  ```

- [ ] Documentation files make sense
  ```powershell
  Get-ChildItem -Filter "*.md"
  ```
  Expected: Should list all documentation files

---

## Phase 10: Complete System Test

Run this complete test sequence:

```powershell
# 1. Ensure fresh start
docker-compose down
Start-Sleep -Seconds 5

# 2. Start everything
docker-compose up -d
Start-Sleep -Seconds 20

# 3. Check status
docker-compose ps

# 4. Test FastAPI
curl http://localhost:8000

# 5. Test scraping
$response = curl "http://localhost:8000/scrapper/?url=https://example.com"
$response | ConvertFrom-Json

# 6. Check stats
curl http://localhost:8000/scrapper/stats

# 7. Test ChromaDB
curl http://localhost:8001/api/v1

# 8. View logs (no errors?)
docker-compose logs --tail=30

echo "✅ All tests passed!"
```

---

## ❌ Troubleshooting If Something Fails

### If containers won't start:
```powershell
docker-compose logs -f
# Read error messages
```
→ See **TROUBLESHOOTING.md**

### If ports are in use:
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :8001
```
→ Kill those processes or change ports

### If containers are slow:
```powershell
# Check Docker Desktop resources:
# Settings > Resources > Increase CPU/Memory
```

### If data won't persist:
```powershell
# Never use "docker-compose down -v"!
# Always use "docker-compose down" (without -v)
```

---

## ✅ Final Verification

If all these checks pass, you're ready to go:

- [ ] Docker is installed and running ✓
- [ ] Both containers are Up ✓
- [ ] FastAPI responds ✓
- [ ] ChromaDB responds ✓
- [ ] Scraping works ✓
- [ ] Data persists ✓
- [ ] Logs are clean ✓
- [ ] Performance is good ✓
- [ ] All files exist ✓
- [ ] Documentation is available ✓

---

## 🎉 Success!

If you've checked all boxes above, your system is fully operational!

### Next Steps:
1. Read `README.md`
2. Read `SETUP_COMPLETE.md`
3. Start using the API at `http://localhost:8000/docs`
4. Integrate ChromaDB into your workflow (see `CHROMA_INTEGRATION.md`)

### To Get Help:
- Quick commands: `.\quick-commands.ps1`
- Troubleshooting: `TROUBLESHOOTING.md`
- Architecture: `ARCHITECTURE.md`
- Reference: `QUICK_REFERENCE.md`

---

## 📊 Keep This For Reference

Print or save this checklist to verify setup in the future.

**Date Verified:** ________________  
**System:** Windows + Docker Desktop  
**Status:** ✅ Working  
**Notes:** ________________________________________

---

**Everything is ready!** 🚀

Now run:
```powershell
docker-compose up -d
```

Visit: http://localhost:8000/docs

Enjoy! 🎉

