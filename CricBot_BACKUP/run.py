import subprocess
import time
import os

def run_all_commands():
    # Start Rasa server
    rasa_process = subprocess.Popen(
        ["rasa", "run", "--enable-api", "--cors", "*", "--debug"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("✅ Rasa server started")

    # Start Rasa actions server
    actions_process = subprocess.Popen(
        ["rasa", "run", "actions"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("✅ Rasa actions server started")

    # Start frontend (npm start)
    frontend_process = subprocess.Popen(
        ["npm", "start"],
        cwd="/Users/sharatrk/Desktop/CricBot/frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("✅ Frontend server started")

    # Start Flask script
    flask_process = subprocess.Popen(
        ["/Users/sharatrk/Desktop/CricBot/CricBot_env/bin/python", "/Users/sharatrk/Desktop/CricBot/cricinfo/Flask_Connect.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("✅ Flask script started")

    # Keep the script running so subprocesses don’t terminate
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping all processes...")
        rasa_process.terminate()
        actions_process.terminate()
        frontend_process.terminate()
        flask_process.terminate()

if __name__ == "__main__":
    run_all_commands()
