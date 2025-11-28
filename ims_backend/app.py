# app.py
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from db import crud
import os
import sys

app = Flask(__name__)
# More permissive CORS for development
CORS(app, origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:3000"])

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route("/api/test")
def test_connection():
    """Test endpoint to verify server and database are working"""
    try:
        conn = crud.connect()
        conn.close()
        return jsonify({
            "status": "success", 
            "message": "Flask server and database are connected",
            "server": "running",
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Database connection failed: {str(e)}",
            "server": "running",
            "database": "disconnected"
        }), 500

@app.route("/")
def home():
    return """
    <h1>Inventory Management System API</h1>
    <p>Flask server is running!</p>
    <ul>
        <li><a href="/api/test">Test API & Database</a></li>
        <li><a href="/api/products">List Products</a></li>
    </ul>
    """

# ... keep your existing /api/products routes here ...

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 3000))  # Changed to 3000
    debug = os.getenv("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
    
    print(f" Starting Flask server on port {port}...")
    print(f" Debug mode: {debug}")
    print(f" API URL: http://127.0.0.1:{port}/api/products")
    print(f" Test URL: http://127.0.0.1:{port}/api/test")
    
    try:
        app.run(host="0.0.0.0", port=port, debug=debug)
    except Exception as e:
        print(f" Failed to start server: {e}")
        print(" Try using a different port: FLASK_PORT=3000 python app.py")