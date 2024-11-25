# run.py
from app import app  # Import the app from app.py

if __name__ == "__main__":
    app.run(port=5000, debug=True)
