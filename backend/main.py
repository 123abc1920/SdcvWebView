from app import create_app
import time
import threading
import webbrowser
import os
import sys
from app.shared.consts import PORT
from waitress import serve

app = create_app()


def open_browser():
    time.sleep(3)
    webbrowser.open(f"http://127.0.0.1:{PORT}")


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        print("=" * 50)
        print(f" {os.getenv('APP_NAME', 'SDCV API')} successfully started")
        print("A tab will now automatically open in your browser....")
        print(f"If it didn't open, go to: http://127.0.0.1:{PORT}")
        print("-" * 50)
        print("DO NOT CLOSE THIS WINDOW while you are working with the program.")
        print("=" * 50)

        threading.Thread(target=open_browser, daemon=True).start()

        serve(app, host="127.0.0.1", port=PORT)
    else:
        app.run(host="127.0.0.1", port=PORT, debug=True)
