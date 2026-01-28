from server.app import run_flask
import threading
import time

def start_flask():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

def startup():
    start_flask()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    startup()
