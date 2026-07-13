#!/usr/bin/env pwsh
# Quick Commands Reference for Web Scraping + ChromaDB Stack
# For Windows PowerShell

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Web Scraping + ChromaDB - Quick Commands Reference      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

function Show-Menu {
    Write-Host "`n📋 Available Commands:" -ForegroundColor Green
    Write-Host "  1. Start Stack          - Start both Web Scraping and ChromaDB" -ForegroundColor Yellow
    Write-Host "  2. Stop Stack           - Stop all containers" -ForegroundColor Yellow
    Write-Host "  3. View Logs            - View real-time logs" -ForegroundColor Yellow
    Write-Host "  4. Check Status         - Check if containers are running" -ForegroundColor Yellow
    Write-Host "  5. Test Scraper         - Test basic scraping" -ForegroundColor Yellow
    Write-Host "  6. Test ChromaDB        - Test ChromaDB connection" -ForegroundColor Yellow
    Write-Host "  7. View API Docs        - Open Swagger UI in browser" -ForegroundColor Yellow
    Write-Host "  8. Clean Everything     - Remove containers and volumes" -ForegroundColor Red
    Write-Host "  0. Exit                 - Exit this menu" -ForegroundColor Yellow
}

function Start-Stack {
    Write-Host "`n▶️  Starting Web Scraping + ChromaDB stack..." -ForegroundColor Green
    docker-compose up -d
    Write-Host "✅ Stack started! Waiting for services to be ready..." -ForegroundColor Green
    Start-Sleep -Seconds 5
    Write-Host "🌐 FastAPI:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "🌐 ChromaDB: http://localhost:8001/api/v1" -ForegroundColor Cyan
    Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
}

function Stop-Stack {
    Write-Host "`n⏹️  Stopping containers..." -ForegroundColor Green
    docker-compose stop
    Write-Host "✅ Stack stopped!" -ForegroundColor Green
}

function View-Logs {
    Write-Host "`n📜 Showing live logs (Press Ctrl+C to exit)..." -ForegroundColor Green
    docker-compose logs -f
}

function Check-Status {
    Write-Host "`n📊 Container Status:" -ForegroundColor Green
    docker-compose ps
    Write-Host "`n📊 Network Status:" -ForegroundColor Green
    docker network ls | Select-String "web-scraping"
}

function Test-Scraper {
    Write-Host "`n🧪 Testing Web Scraper..." -ForegroundColor Green
    Write-Host "Scraping: https://www.example.com" -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri "http://localhost:8000/scrapper/?url=https://www.example.com" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Scraper is working!" -ForegroundColor Green
        Write-Host "Response Preview:" -ForegroundColor Cyan
        $response.Content | ConvertFrom-Json | Select-Object -Property url, content | Format-List
    } else {
        Write-Host "❌ Scraper test failed!" -ForegroundColor Red
    }
}

function Test-ChromaDB {
    Write-Host "`n🧪 Testing ChromaDB Connection..." -ForegroundColor Green
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8001/api/v1" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ ChromaDB is healthy and running!" -ForegroundColor Green

            # Test stats endpoint
            $statsResponse = Invoke-WebRequest -Uri "http://localhost:8000/scrapper/stats" -UseBasicParsing
            if ($statsResponse.StatusCode -eq 200) {
                Write-Host "`nChromaDB Stats:" -ForegroundColor Cyan
                $statsResponse.Content | ConvertFrom-Json | Format-List
            }
        }
    } catch {
        Write-Host "❌ ChromaDB connection failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Open-APIDocs {
    Write-Host "`n📖 Opening API Documentation..." -ForegroundColor Green
    Start-Process "http://localhost:8000/docs"
    Write-Host "✅ Browser window opened!" -ForegroundColor Green
}

function Clean-Everything {
    Write-Host "`n⚠️  WARNING: This will remove all containers and volumes!" -ForegroundColor Red
    Write-Host "Data will be LOST! Continue? (y/N): " -ForegroundColor Yellow -NoNewline
    $confirm = Read-Host

    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        Write-Host "`n🗑️  Cleaning up..." -ForegroundColor Red
        docker-compose down -v
        Write-Host "✅ Everything cleaned!" -ForegroundColor Green
    } else {
        Write-Host "❌ Cleanup cancelled" -ForegroundColor Yellow
    }
}

# Main Menu Loop
do {
    Show-Menu
    $choice = Read-Host "`nEnter your choice (0-8)"

    switch ($choice) {
        "1" { Start-Stack }
        "2" { Stop-Stack }
        "3" { View-Logs }
        "4" { Check-Status }
        "5" { Test-Scraper }
        "6" { Test-ChromaDB }
        "7" { Open-APIDocs }
        "8" { Clean-Everything }
        "0" {
            Write-Host "`n👋 Goodbye!" -ForegroundColor Green
            exit
        }
        default { Write-Host "❌ Invalid choice! Please try again." -ForegroundColor Red }
    }
} while ($true)

