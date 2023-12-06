@echo off

REM Navigate to your project directory
cd D:\dynamic_led_prod

REM Activate virtual environment (modify the path if needed)
call venv2\Scripts\activate

REM Navigate to the Django project directory
cd dynamic_led_display_prod

REM Run the Django development server on 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000