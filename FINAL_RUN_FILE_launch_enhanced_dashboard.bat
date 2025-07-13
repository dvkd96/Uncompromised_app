@echo off
echo 🌾 STARTING UNCOMPROMIZED SMART FARMER DASHBOARD
echo =====================================================

cd "c:\Users\Dnyaneshwari\Desktop\simp\New\crop-management-system"

echo ✅ Enhanced Features Active:
echo    📊 Complete crop_suitability.csv integration
echo    📅 Enhanced sowing/harvesting month logic  
echo    🛠️ All 246 maintenance steps accessible
echo    🌾 Scientific soil-crop matching
echo    � Smart Crop Rotation Planning with 5 scientific rules
echo    🌿 Advanced Intercropping recommendations
echo    �🔍 Automatic CSV file detection
echo    📝 Sample data fallback if files missing
echo.

echo 🔍 Testing CSV file loading first...
python test_loading.py

echo.
echo 🚀 Starting Uncompromized Smart Farmer Dashboard...
python ultimate_dashboard.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Error occurred. Check if Python is installed.
    pause
)
