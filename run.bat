@echo off

REM process 1
REM Navigate to your project directory
set DJANGO_SETTINGS_MODULE=dynamic_led_display_prod.settings
cd C:\Users\Administrator\weather_monitoring_system\dynamic_led_display_prod

REM Activate virtual environment (modify the path if needed)
call .\venv\Scripts\activate

REM Navigate to the Django project directory
cd dynamic_led_display_prod

REM Run the Django development server on 0.0.0.0:8000
start daphne -b 0.0.0.0 -p 8000 dynamic_led_display_prod.asgi:application

REM Process 2
start python C:\Users\Administrator\weather_monitoring_system\dynamic_led_display_prod\producer\producer\rs485producerasync2.py