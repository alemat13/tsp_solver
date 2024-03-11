# reading arguments
param(
    [switch]$build = $false
)

# check if -Build is passed as argument
if ($build -eq $true) {
    echo "Building frontend..."
    # run frontend/start.ps1
    cd frontend
    npm run build
    cd ..
}

# run backend/start.ps1
cd backend
.\start.ps1