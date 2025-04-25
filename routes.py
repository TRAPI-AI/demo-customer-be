from flask import Flask

def initialize_routes(app: Flask):
    @app.route('/')
    def home():
        return "Welcome to the API"

    # Add more routes as needed
