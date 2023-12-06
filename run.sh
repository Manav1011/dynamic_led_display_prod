#!/bin/bash

# Check if anything is running on port 8000
if lsof -i :8000; then
    # If a process is using port 8000, terminate it
    echo "Terminating process on port 8000"
    lsof -t -i:8000 | xargs sudo kill -9
fi

# Navigate to your project directory
cd /home/manav1011/Documents/dynamic_led_display_prod

# Activate virtual environment
source venv/bin/activate

# Navigate to the Django project directory
cd dynamic_led_display_prod

# Run the Django development server on 0.0.0.0:8000 in the background
python manage.py runserver 0.0.0.0:8000
# xdg-open http://192.168.29.18:8000;