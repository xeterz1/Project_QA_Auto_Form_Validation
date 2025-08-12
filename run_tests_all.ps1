# tools\run_tests_all.ps1  (minimal & friendly)

# 0) Clean Allure results
Write-Host "Cleaning allure-results..."
Remove-Item -Recurse -Force "allure-results" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "allure-results" | Out-Null

# 1) Start backend (FastAPI) on 127.0.0.1:8000
Write-Host "`nStarting backend..."
$server = Start-Process python -ArgumentList "-m","uvicorn","app:app","--host","127.0.0.1","--port","8000" -PassThru
Start-Sleep -Seconds 2   # small grace time

# 2) Tell tests where to go (optional; they already default to this)
$env:FORM_URL = "http://127.0.0.1:8000/"

# 3) Run tests
Write-Host "`n=== Unit (pytest) ==="
pytest tests --alluredir=allure-results

Write-Host "`n=== Selenium (pytest) ==="
pytest selenium_test --alluredir=allure-results

Write-Host "`n=== Robot (acceptance) ==="
robot --listener "allure_robotframework;allure-results" robot_tests\form_tests.robot

# 4) Stop backend
Write-Host "`nStopping backend..."
try { Stop-Process -Id $server.Id -Force } catch {}

# 5) Open Allure
Write-Host "`nOpening Allure report..."
allure serve allure-results
