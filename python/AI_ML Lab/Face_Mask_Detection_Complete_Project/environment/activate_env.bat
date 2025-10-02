@echo off
echo.
echo =========================================
echo  Face Detection Environment Activator
echo =========================================
echo.

cd /d "C:\Users\Prana\OneDrive\Desktop\coding\python\AI_ML Lab\Face_Mask_Detection_Project"

echo Activating virtual environment...
call face_detection_env\Scripts\activate

echo.
echo Environment activated successfully!
echo.
echo Available commands:
echo   python face_mask_detection.py    - Run main system
echo   python demo_face_detection.py    - Run demo
echo   python setup_face_detection.py   - Run setup
echo   deactivate                       - Exit environment
echo.
echo Happy coding! ^_^
echo.

cmd /k