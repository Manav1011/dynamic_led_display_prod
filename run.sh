#!/bin/bash

# Check if anything is running on port 8000
if lsof -i :8000; then
    # If a process is using port 8000, terminate it
    echo "Terminating process on port 8000"
    lsof -t -i:8000 | xargs sudo kill -9
fi
export DJANGO_SETTINGS_MODULE=dynamic_led_display_prod.settings;
cd /home/manav1011/Documents/dynamic_led_display_prod;
source venv/bin/activate;
cd dynamic_led_display_prod;
daphne -b 0.0.0.0 -p 8000 dynamic_led_display_prod.asgi:application;
# python producer/producer/rs485producerasync2.py;