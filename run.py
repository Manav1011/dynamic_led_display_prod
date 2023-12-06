import subprocess
import psutil
import os

# Function to check if a process is running on a specific port
def is_process_running(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
            return True
    return False

# Function to terminate a process running on a specific port
def terminate_process(port):
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if port in proc.info['cmdline'] and proc.info['pid'] != os.getpid():
            proc.terminate()

# Check if anything is running on port 8000
if is_process_running(8000):
    print("Terminating process on port 8000")
    terminate_process(8000)

# Navigate to your project directory
project_directory = "/home/manav1011/Documents/dynamic_led_display_prod"
os.chdir(project_directory)

# Activate virtual environment
venv_activate = os.path.join("venv", "bin", "activate")
subprocess.run(f"source {venv_activate} && python manage.py runserver 0.0.0.0:8000", shell=True, check=True, executable="/bin/bash")
    