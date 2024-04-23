# reading arguments
param(
    [switch]$build = $false
)

# check if -Build is passed as argument
if ($build -eq $true) {
    Write-Output "Building frontend..."
    # run frontend/start.ps1
    Set-Location frontend
    npm run build
    Set-Location ..
}

# run backend/start.ps1
Set-Location backend
.\start.ps1