# Entry point for the backend application

from search import app

if __name__ == "__main__":
    app.run(port=5000, debug=True)
