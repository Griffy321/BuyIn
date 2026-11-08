# Starts everything needed to test BuyIn on your phone:
#   1. the Python server, in its own window, reachable over Wi-Fi (restarts itself when you save Python files)
#   2. the Expo dev server, in this window, with the app pointed at this PC's current IP
#
# Run from the repo root:
#   .\dev.ps1
# If Windows says running scripts is disabled, use this instead:
#   powershell -ExecutionPolicy Bypass -File .\dev.ps1
#
# Then scan the QR code with Expo Go (phone on the same Wi-Fi as this PC).
# Stop with Ctrl+C here, and close the server window.

$ErrorActionPreference = 'Stop'
$port = 5000
$root = $PSScriptRoot

# --- Find this PC's IP on the local network (the adapter that has internet access) ---
$network = Get-NetIPConfiguration |
    Where-Object { $_.IPv4DefaultGateway -and $_.NetAdapter.Status -eq 'Up' } |
    Select-Object -First 1

if (-not $network) {
    Write-Host "Couldn't find an active network connection. Is the PC on Wi-Fi?" -ForegroundColor Red
    exit 1
}

$ip = $network.IPv4Address.IPAddress | Select-Object -First 1
$apiUrl = "http://${ip}:$port"
Write-Host "PC address: $apiUrl ($($network.InterfaceAlias))" -ForegroundColor Cyan

# --- Warnings for the usual reasons the phone can't connect (they don't stop the script) ---
$category = (Get-NetConnectionProfile -InterfaceIndex $network.InterfaceIndex).NetworkCategory
if ($category -eq 'Public') {
    Write-Host "Warning: this Wi-Fi is set to Public, so Windows may block the phone." -ForegroundColor Yellow
    Write-Host "  Fix: Settings > Network & internet > Wi-Fi > (your network) > Private network" -ForegroundColor Yellow
}

if (-not (Get-NetFirewallRule -DisplayName 'BuyIn API' -ErrorAction SilentlyContinue)) {
    Write-Host "Warning: no 'BuyIn API' firewall rule. Run this once in an ADMIN PowerShell:" -ForegroundColor Yellow
    Write-Host "  New-NetFirewallRule -DisplayName 'BuyIn API' -Direction Inbound -Protocol TCP -LocalPort $port -Action Allow -Profile Private" -ForegroundColor Yellow
}

# --- Start the Python server in a new window, unless it's already running ---
$listening = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($listening) {
    if ($listening.LocalAddress -contains '0.0.0.0') {
        Write-Host "Server already running on port $port, reusing it." -ForegroundColor Green
    } else {
        Write-Host "Something is already on port $port but only listening on localhost, so the phone can't reach it." -ForegroundColor Red
        Write-Host "Stop it (close that terminal or press Ctrl+C in it) and run this script again." -ForegroundColor Red
        exit 1
    }
} else {
    python -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('fastapi') and importlib.util.find_spec('uvicorn') else 1)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing server dependencies (first run only)..." -ForegroundColor Green
        python -m pip install -r "$root\server\requirements.txt"
    }
    Write-Host "Starting the Python server in a new window..." -ForegroundColor Green
    $serverCommand = "Set-Location '$root\server'; python -m uvicorn main:app --host 0.0.0.0 --port $port --reload"
    Start-Process powershell -ArgumentList '-NoExit', '-Command', $serverCommand
}

# --- Start Expo in this window ---
Set-Location "$root\mobile"
if (-not (Test-Path 'node_modules')) {
    Write-Host "Installing app dependencies (first run only)..." -ForegroundColor Green
    npm install
}

$env:EXPO_PUBLIC_API_URL = $apiUrl
Write-Host "Starting Expo. Scan the QR code with Expo Go." -ForegroundColor Green
npx expo start --clear
