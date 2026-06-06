from app import app_factory
from app.shared.config import config_factory
import os
from dotenv import load_dotenv

load_dotenv()

config = os.getenv("CONFIG")

app = app_factory(config_factory(config))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5200, debug=True)
