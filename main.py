from flask import Flask
from providers import new_provider
from routes import initialize_routes

app = Flask(__name__)

# Initialize routes
initialize_routes(app)

# Register new provider
new_provider.initialize(app)

if __name__ == "__main__":
    app.run()