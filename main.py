from flask import Flask
from providers.new_provider import NewProvider
from utils.normalization import normalize_data

app = Flask(__name__)

# Register new provider
new_provider = NewProvider()

# Middleware registration
@app.before_request
def before_request():
    # Example middleware logic
    pass

# Error handler registration
@app.errorhandler(Exception)
def handle_exception(e):
    # Example error handling logic
    return str(e), 500

# Initialize new components
new_provider.initialize()

if __name__ == "__main__":
    app.run(debug=True)
