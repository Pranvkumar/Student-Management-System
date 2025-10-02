# Face Detection Environment Activator (PowerShell)
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Face Detection Environment Activator" -ForegroundColor Cyan  
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "C:\Users\Prana\OneDrive\Desktop\coding\python\AI_ML Lab\Face_Mask_Detection_Project"

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\face_detection_env\Scripts\Activate.ps1

Write-Host ""
Write-Host "Environment activated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor White
Write-Host "  python face_mask_detection.py    - Run main system" -ForegroundColor Gray
Write-Host "  python demo_face_detection.py    - Run demo" -ForegroundColor Gray  
Write-Host "  python setup_face_detection.py   - Run setup" -ForegroundColor Gray
Write-Host "  deactivate                       - Exit environment" -ForegroundColor Gray
Write-Host ""
Write-Host "Happy coding! ^_^" -ForegroundColor Magenta
Write-Host ""